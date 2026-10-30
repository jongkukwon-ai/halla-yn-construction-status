"""업종 관련 뉴스 카카오톡 아침 발송 — GitHub Actions(kakao.yml)에서 매일 07:30 KST 실행.

news-data.js(발송 작업이 07:00에 먼저 갱신)에서 어제·오늘 날짜 기사를 골라
카카오 메시지 API 「친구에게 보내기」로 지정된 직원들에게 보냅니다(목록형 메시지: 패널별 대표 기사 3건 + 「뉴스 전체 보기」 버튼).

필요한 GitHub Secrets (값은 저장소 Settings → Secrets and variables → Actions에 직접 입력, 파일에 쓰지 않음)
  KAKAO_REST_API_KEY      카카오 앱 REST API 키
  KAKAO_REFRESH_TOKEN     보내는 사람(담당자) 계정의 리프레시 토큰 — kakao_login.py로 발급
  KAKAO_CLIENT_SECRET     클라이언트 시크릿(카카오 앱 → 플랫폼 키 → REST API 키, 새 앱은 기본으로 켜져 있음)
  KAKAO_RECIPIENTS        (선택) 받을 사람 카톡 닉네임 쉼표 목록. 비우면 앱에 동의한 친구 전원
  GH_PAT                  (선택) 리프레시 토큰이 새로 발급될 때 KAKAO_REFRESH_TOKEN을 자동 교체할 GitHub 토큰
                          (없으면 약 2개월마다 kakao_login.py로 다시 발급해 넣어야 함)

  python .github/scripts/send_kakao_news.py --dry-run     # 보낼 메시지만 출력(키 불필요)
"""
import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NEWS = ROOT / 'news-data.js'
SITE = 'https://jongkukwon-ai.github.io/halla-yn-construction-status/'
NEWS_PAGE = SITE + 'news/index.html'
ICON = SITE + 'assets/icon-192.png'
KST = timezone(timedelta(hours=9))
PANELS = [('NEWS_CONSTRUCTION', '영남 건설'), ('NEWS_CEMENT', '레미콘·시멘트'), ('NEWS_OTHER', '그 외 지역')]
ITEM = re.compile(r'\{\s*title:\s*"((?:[^"\\]|\\.)*)",\s*source:\s*"((?:[^"\\]|\\.)*)",\s*date:\s*"([0-9-]+)"')
DAYS = '월화수목금토일'


def read_news():
    text = NEWS.read_text(encoding='utf-8')
    out = {}
    for name, _ in PANELS:
        blk = text[text.index('const ' + name):]
        blk = blk[blk.index('['):blk.index('];')]
        out[name] = [{'title': json.loads(f'"{m[1]}"'), 'source': json.loads(f'"{m[2]}"'), 'date': m[3]}
                     for m in ITEM.finditer(blk)]
    return out


def build_message(news, today):
    """어제·오늘 기사 중 패널별 최신 1건씩(최대 3건) → 카카오 목록형 템플릿"""
    since = (today - timedelta(days=1)).isoformat()
    link = {'web_url': NEWS_PAGE, 'mobile_web_url': NEWS_PAGE}
    contents, total = [], 0
    for name, label in PANELS:
        fresh = [x for x in news[name] if x['date'] >= since]
        total += len(fresh)
        if fresh:
            x = fresh[0]
            title = x['title'] if len(x['title']) <= 60 else x['title'][:58] + '…'
            contents.append({'title': title, 'description': f"[{label}] {x['source']} · {x['date'][5:].replace('-', '/')}",
                             'image_url': ICON, 'image_width': 192, 'image_height': 192, 'link': link})
    if not contents:
        return None, 0
    if len(contents) == 1:                       # 목록형은 2건 이상이어야 해서 1건이면 같은 패널 다음 기사로 채움
        for name, label in PANELS:
            fresh = [x for x in news[name] if x['date'] >= since]
            if len(fresh) > 1:
                x = fresh[1]
                contents.append({'title': x['title'][:60], 'description': f"[{label}] {x['source']}",
                                 'image_url': ICON, 'image_width': 192, 'image_height': 192, 'link': link})
                break
    if len(contents) < 2:
        return None, total
    template = {
        'object_type': 'list',
        'header_title': f'업종 관련 뉴스 · {today.month}/{today.day}({DAYS[today.weekday()]})',
        'header_link': link,
        'contents': contents[:3],
        'buttons': [{'title': f'뉴스 전체 보기 ({total}건)', 'link': link}],
    }
    return template, total


# ── 카카오 API ──
def call(url, data=None, token=None, method='POST'):
    headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
    if token:
        headers['Authorization'] = 'Bearer ' + token
    body = urllib.parse.urlencode(data).encode() if data is not None else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method if body or method == 'GET' else 'POST')
    try:
        return json.loads(urllib.request.urlopen(req, timeout=30).read())
    except urllib.error.HTTPError as e:
        detail = e.read().decode('utf-8', 'replace')
        raise RuntimeError(f'카카오 API 오류 {e.code} {url.split("?")[0]}: {detail[:300]}') from None


def access_token():
    data = {'grant_type': 'refresh_token', 'client_id': os.environ['KAKAO_REST_API_KEY'],
            'refresh_token': os.environ['KAKAO_REFRESH_TOKEN']}
    if os.environ.get('KAKAO_CLIENT_SECRET'):
        data['client_secret'] = os.environ['KAKAO_CLIENT_SECRET']
    r = call('https://kauth.kakao.com/oauth/token', data)
    if r.get('refresh_token'):                    # 만료 1개월 전부터 새 리프레시 토큰이 함께 옴
        days = int(r.get('refresh_token_expires_in', 0)) // 86400
        if not update_secret(r['refresh_token']):
            print(f'::warning::카카오 리프레시 토큰이 새로 발급됨(유효 {days}일). GH_PAT가 없어 자동 교체하지 못함 — '
                  '기존 토큰이 만료되기 전에 kakao_login.py로 다시 발급해 KAKAO_REFRESH_TOKEN에 넣으세요.')
    return r['access_token']


def update_secret(value):
    """GH_PAT가 있으면 KAKAO_REFRESH_TOKEN 시크릿을 새 값으로 교체(PyNaCl 필요)"""
    pat, repo = os.environ.get('GH_PAT'), os.environ.get('GITHUB_REPOSITORY')
    if not pat or not repo:
        return False
    from nacl import encoding, public                       # pip install pynacl (워크플로에서 설치)
    hdr = {'Authorization': f'Bearer {pat}', 'Accept': 'application/vnd.github+json'}
    key = json.loads(urllib.request.urlopen(urllib.request.Request(
        f'https://api.github.com/repos/{repo}/actions/secrets/public-key', headers=hdr), timeout=30).read())
    box = public.SealedBox(public.PublicKey(key['key'].encode(), encoding.Base64Encoder()))
    enc = base64.b64encode(box.encrypt(value.encode())).decode()
    req = urllib.request.Request(f'https://api.github.com/repos/{repo}/actions/secrets/KAKAO_REFRESH_TOKEN', method='PUT',
                                 data=json.dumps({'encrypted_value': enc, 'key_id': key['key_id']}).encode(),
                                 headers={**hdr, 'Content-Type': 'application/json'})
    urllib.request.urlopen(req, timeout=30).read()
    print('카카오 리프레시 토큰을 새 값으로 자동 교체함')
    return True


def recipients(token):
    """앱에 동의한 카톡 친구 → KAKAO_RECIPIENTS(닉네임) 지정 시 그 사람만"""
    friends, offset = [], 0
    while True:
        r = call(f'https://kapi.kakao.com/v1/api/talk/friends?limit=100&offset={offset}', token=token, method='GET')
        friends += r.get('elements', [])
        if not r.get('after_url'):
            break
        offset += 100
    want = [w.strip() for w in os.environ.get('KAKAO_RECIPIENTS', '').split(',') if w.strip()]
    if want:
        picked = [f for f in friends if f.get('profile_nickname') in want]
        missing = sorted(set(want) - {f.get('profile_nickname') for f in picked})
        if missing:
            print(f'::warning::받을 사람 중 친구 목록에 없는 닉네임 {len(missing)}명 — 카톡 친구가 아니거나 앱 동의 전입니다.')
        friends = picked
    return [f['uuid'] for f in friends]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true', help='보낼 메시지만 출력')
    a = ap.parse_args()
    today = datetime.now(KST).date()
    template, total = build_message(read_news(), today)
    if not template:
        print(f'어제·오늘 기사가 부족해 보내지 않음(새 기사 {total}건)')
        return
    if a.dry_run:
        print(json.dumps(template, ensure_ascii=False, indent=1))
        return
    if not os.environ.get('KAKAO_REST_API_KEY') or not os.environ.get('KAKAO_REFRESH_TOKEN'):
        print('카카오 키가 아직 설정되지 않아 건너뜀(KAKAO_REST_API_KEY, KAKAO_REFRESH_TOKEN)')
        return
    token = access_token()
    payload = json.dumps(template, ensure_ascii=False)
    call('https://kapi.kakao.com/v2/api/talk/memo/default/send', {'template_object': payload}, token=token)   # 담당자 본인에게 먼저
    try:
        uuids = recipients(token)
    except RuntimeError as e:                         # 심사 전·친구목록 동의 전이면 친구 발송만 건너뜀
        print(f'::warning::친구에게 보내기를 아직 쓸 수 없어 나에게만 보냄 — 카카오 심사 승인·친구목록 동의 후 kakao_login.py를 다시 실행하세요. ({str(e)[:120]})')
        print(f'::notice::발송 완료: 나에게 1건 (새 기사 {total}건)')
        return
    sent = 0
    for i in range(0, len(uuids), 5):                 # 한 번에 최대 5명
        r = call('https://kapi.kakao.com/v1/api/talk/friends/message/default/send',
                 {'receiver_uuids': json.dumps(uuids[i:i + 5]), 'template_object': payload}, token=token)
        sent += len(r.get('successful_receiver_uuids', []))
    print(f'::notice::발송 완료: 친구 {sent}/{len(uuids)}명 + 나에게 1건 (새 기사 {total}건)')
    if uuids and sent < len(uuids):
        sys.exit(f'일부 발송 실패: {len(uuids) - sent}명')


if __name__ == '__main__':
    main()
