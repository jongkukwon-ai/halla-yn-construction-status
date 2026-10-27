"""카카오 로그인 도우미 — 담당자 본인 PC에서 실행.

1) 담당자(보내는 사람) 리프레시 토큰 발급
   브라우저로 카카오 로그인·동의 화면을 열고, 돌아온 인가 코드로 토큰을 받아 리프레시 토큰을 화면에 보여 줍니다.
   보여 준 값은 GitHub 저장소 Settings → Secrets and variables → Actions → KAKAO_REFRESH_TOKEN 에 직접 붙여 넣으세요.
   (이 값은 파일로 저장하지 않으며, 채팅·메일로 보내지 마세요.)

2) 직원(받는 사람) 연결 — --member
   카카오 심사 전에는 앱 멤버로 초대·수락한 직원만 받을 수 있고, 그 직원도 앱에 한 번 로그인해 「친구 목록·메시지」에 동의해야
   친구 목록에 나타납니다. 직원이 담당자 PC 앞에서 휴대폰 카카오톡으로 QR을 찍어 로그인·동의하면 연결만 하고 끝냅니다.
   직원의 토큰은 화면에 보여 주지도, 저장하지도 않습니다(연결 확인 뒤 바로 로그아웃 처리). 여러 명을 연달아 할 수 있습니다.

사전 준비: 카카오 앱 → 앱 → 플랫폼 키 → REST API 키 → 카카오 로그인 리다이렉트 URI에 http://localhost:8790/callback 등록

  py .github/scripts/kakao_login.py             # 담당자: 친구목록까지
  py .github/scripts/kakao_login.py --only-me   # 담당자: 나에게 보내기만
  py .github/scripts/kakao_login.py --member    # 직원 연결(QR 로그인·동의), 여러 명 연달아
"""
import getpass
import sys
import http.server
import json
import urllib.error
import urllib.parse
import urllib.request
import webbrowser

PORT = 8790
REDIRECT = f'http://localhost:{PORT}/callback'
SCOPES = 'talk_message,friends'


def authorize(key, scopes, force_login=False):
    """브라우저로 카카오 로그인·동의 → 인가 코드"""
    got = {}

    class H(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            if 'code' not in q and 'error' not in q:          # favicon 등 다른 요청은 무시
                self.send_response(204)
                self.end_headers()
                return
            got['code'] = (q.get('code') or [''])[0]
            got['error'] = (q.get('error_description') or q.get('error') or [''])[0]
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write('<h3>카카오 로그인 완료 — 이 창은 닫고 명령 창으로 돌아가세요.</h3>'.encode())

        def log_message(self, *a):
            pass

    srv = http.server.HTTPServer(('localhost', PORT), H)
    params = {'client_id': key, 'redirect_uri': REDIRECT, 'response_type': 'code', 'scope': scopes}
    if force_login:
        params['prompt'] = 'login'                            # 앞사람 로그인 상태와 관계없이 새로 로그인
    url = 'https://kauth.kakao.com/oauth/authorize?' + urllib.parse.urlencode(params)
    print('브라우저에서 카카오 로그인·동의를 진행하세요. 안 열리면 아래 주소를 직접 여세요.\n' + url)
    webbrowser.open(url)
    srv.timeout = 300
    try:
        while 'code' not in got:
            srv.handle_request()
    finally:
        srv.server_close()
    if not got['code']:
        raise RuntimeError(f'로그인·동의가 완료되지 않음: {got["error"]}')
    return got['code']


def token(key, secret, code):
    data = {'grant_type': 'authorization_code', 'client_id': key, 'redirect_uri': REDIRECT, 'code': code}
    if secret:
        data['client_secret'] = secret
    return api('https://kauth.kakao.com/oauth/token', data=data)


def api(url, data=None, bearer=None):
    headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
    if bearer:
        headers['Authorization'] = 'Bearer ' + bearer
    body = urllib.parse.urlencode(data).encode() if data is not None else None
    try:
        return json.loads(urllib.request.urlopen(urllib.request.Request(url, data=body, headers=headers), timeout=30).read())
    except urllib.error.HTTPError as e:
        detail = e.read().decode('utf-8', 'replace')
        raise RuntimeError(f'카카오 응답 오류 {e.code}: {detail[:200]}') from None


def ask_keys():
    key = getpass.getpass('카카오 앱 REST API 키(입력해도 화면에 안 보임): ').strip()
    secret = getpass.getpass('Client Secret(사용 안 하면 그냥 Enter): ').strip()
    return key, secret


def sender(only_me):
    scopes = 'talk_message' if only_me else SCOPES
    if only_me:
        print('「나에게만」 모드: 메시지 전송 권한만 받습니다(친구목록은 이 명령을 --only-me 없이 다시 실행).')
    key, secret = ask_keys()
    r = token(key, secret, authorize(key, scopes))
    days = int(r.get('refresh_token_expires_in', 0)) // 86400
    print('\n아래 값을 GitHub Secrets의 KAKAO_REFRESH_TOKEN에 붙여 넣으세요 (유효 약 %d일):\n' % days)
    print(r['refresh_token'])
    print('\n동의한 권한:', r.get('scope'))


def member():
    print('직원 연결 모드: 직원이 이 PC 앞에서 휴대폰 카카오톡으로 QR을 찍어 로그인·동의합니다.\n'
          '(직원은 먼저 카카오 앱 멤버 초대를 수락해 두어야 합니다. 직원의 토큰은 보여 주지도 저장하지도 않습니다.)\n')
    key, secret = ask_keys()
    done = 0
    while True:
        input('\n직원이 준비되면 Enter — 로그인 화면에서 「QR코드 로그인」을 고르고 직원 휴대폰 카카오톡으로 찍게 하세요 ')
        try:
            r = token(key, secret, authorize(key, SCOPES, force_login=True))
            scopes = set((r.get('scope') or '').split())
            api('https://kapi.kakao.com/v2/user/me', bearer=r['access_token'])     # 앱 연결 확정(카카오 권장: 최초 1회 호출)
            try:
                api('https://kapi.kakao.com/v1/user/logout', data={}, bearer=r['access_token'])   # 받은 토큰은 바로 무효화
            except RuntimeError:
                pass
            if {'talk_message', 'friends'} <= scopes:
                done += 1
                print(f'✅ 연결 완료 ({done}명째) — 친구 목록·메시지 동의 확인')
            else:
                print(f'⚠️ 연결은 됐지만 동의가 빠짐(동의한 항목: {" ".join(sorted(scopes)) or "없음"}) — '
                      '이 직원은 다시 진행해 「친구 목록」「메시지 전송」 모두 동의해야 합니다.')
        except RuntimeError as e:
            print(f'❌ 실패: {e}\n   (멤버 초대를 수락하지 않았거나 동의를 취소한 경우일 수 있습니다)')
        if input('다음 직원도 할까요? (Enter = 예, n = 끝) ').strip().lower().startswith('n'):
            break
    print(f'\n끝. 이번에 연결한 직원 {done}명. 친구 목록에는 10분쯤 뒤부터 반영됩니다.')


if __name__ == '__main__':
    if '--member' in sys.argv:
        member()
    else:
        sender('--only-me' in sys.argv)
