"""착공현황(아파트) 누락 점검 — 청약홈 분양공고 ↔ 사이트 목록 대조. GitHub Actions에서 매주 실행.

1. 한국부동산원 청약홈 「APT 분양정보」 공개 목록(로그인·인증키 불필요)에서
   영남 5개 시도의 입주자모집공고를 조회 가능한 첫 달부터 이번 달까지 모두 받고, 공고마다 상세(위치·공급규모·입주예정월)를 읽음
2. construction/index.html의 RAW(아파트 목록)와 단지명·주소로 대조
   (이름이 달라 자동 대조가 안 되는 단지는 applyhome_alias.json에 '청약홈 단지명 → 사이트 No' 또는 제외 사유로 적어 둠)
3. 사이트 포함 기준(공급 100세대 이상, 입주예정월이 아직 안 지남)에 맞는데 사이트에 없는 단지를 보고서(마크다운)로 출력

  python applyhome_check.py --out report.md --json candidates.json
  종료 코드: 0 = 누락 없음, 10 = 누락 후보 있음, 1 = 조회 실패(청약홈 화면 구조 변경 등)
"""
import argparse
import html as H
import http.cookiejar
import io
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT.parent / 'index.html'
ALIAS = ROOT / 'applyhome_alias.json'
BASE = 'https://www.applyhome.co.kr'
LIST = BASE + '/ai/aia/selectAPTLttotPblancListView.do'
DETAIL = BASE + '/ai/aia/selectAPTLttotPblancDetail.do'
AREAS = ['부산', '울산', '대구', '경남', '경북']
SIDO = {'부산광역시': '부산', '울산광역시': '울산', '대구광역시': '대구', '경상남도': '경남', '경상북도': '경북'}
KST = timezone(timedelta(hours=9))
MIN_UNITS = 100

_op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
_HDR = {'User-Agent': 'Mozilla/5.0', 'Referer': LIST,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}


def _post(url, data):
    body = urllib.parse.urlencode(data).encode()
    for k in range(4):
        try:
            return _op.open(urllib.request.Request(url, data=body, headers=_HDR), timeout=60).read().decode('utf-8', 'replace')
        except Exception as e:                          # 일시 오류는 잠깐 쉬고 다시
            print(f'  재시도({k + 1}) {e}', file=sys.stderr)
            time.sleep(5 * (k + 1))
    raise RuntimeError(f'청약홈 응답 없음: {url}')


def _text(s):
    return re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()


def _rows(page):
    out = []
    for m in re.finditer(r'<tr data-pbno="(\d+)" data-hmno="(\d+)" data-honm="([^"]*)">(.*?)</tr>', page, re.S):
        tds = [_text(t) for t in re.findall(r'<td[^>]*>(.*?)</td>', m.group(4), re.S)]
        out.append({'pbno': m.group(1), 'hmno': m.group(2), 'name': H.unescape(m.group(3)),
                    'area': tds[0], 'kind': tds[1], 'builder': tds[4], 'notice': tds[6]})
    return out


def _detail(r):
    t = _text(_post(DETAIL, {'houseManageNo': r['hmno'], 'pblancNo': r['pbno']}))
    g = lambda pat: (re.search(pat, t) or [None, None])[1]
    r['addr'] = g(r'공급위치 (.*?) 공급규모')
    r['units'] = int((g(r'공급규모 ([\d,]+)세대') or '0').replace(',', ''))
    r['movein'] = g(r'입주예정월 : (\d{4}\.\d{2})') or ''
    r['union'] = '주택조합' in t
    return r


def month_windows(first, last):
    """'YYYYMM' 두 값 사이를 12개월(청약홈 최대 조회 기간) 단위로 자름"""
    def add(ym, n):
        y, m = divmod(int(ym[:4]) * 12 + int(ym[4:]) - 1 + n, 12)
        return f'{y:04d}{m + 1:02d}'
    out, s = [], first
    while s <= last:
        e = min(add(s, 11), last)
        out.append((s, e))
        s = add(e, 1)
    return out


def fetch():
    first_page = _op.open(urllib.request.Request(LIST, headers={'User-Agent': 'Mozilla/5.0'}), timeout=60).read().decode('utf-8', 'replace')
    months = re.findall(r'<option value="(\d{6})"', first_page[first_page.find('name="beginPd"'):][:20000])
    if not months:
        raise RuntimeError('청약홈 조회 기간 목록을 찾지 못함(화면 구조 변경?)')
    first, last = min(months), max(months)
    found = {}
    for area in AREAS:
        for b, e in month_windows(first, last):
            page = 1
            while True:
                rs = _rows(_post(LIST, {'beginPd': b, 'endPd': e, 'suplyAreaCode': area, 'pageIndex': page}))
                for r in rs:
                    found[r['pbno']] = r
                if len(rs) < 10:
                    break
                page += 1
                time.sleep(0.3)
    if len(found) < 50:
        raise RuntimeError(f'공고가 {len(found)}건뿐 — 청약홈 화면 구조가 바뀌었을 수 있음')
    for r in found.values():
        _detail(r)
        time.sleep(0.25)
    return list(found.values()), first, last


# ── 사이트 목록과 대조 ──
def _norm(s):
    s = re.sub(r'\(.*?\)|\[.*?\]', '', s or '')
    s = s.replace('SK VIEW', 'SK뷰').replace('SKVIEW', 'SK뷰').replace('VIEW', '뷰')
    for w in ['아파트', '주상복합', '공공분양주택', '단지', '블록', ' ', '·', '-', '_', ',', '.']:
        s = s.replace(w, '')
    return s.lower()


def _builder(s):
    return re.sub(r'\(주\)|㈜|주식회사|\s', '', s or '')[:2]


def site_rows():
    h = SITE.read_text(encoding='utf-8')
    seg = h[h.index('const RAW = ['):h.index('const RAW_SOC')]
    rows = []
    for line in seg.splitlines():
        line = line.strip().rstrip(',')
        if line.startswith('[') and len(line) > 5:
            try:
                rows.append(json.loads(line))
            except ValueError:
                pass
    if len(rows) < 50:
        raise RuntimeError(f'사이트 RAW를 {len(rows)}건만 읽음')
    return rows


def compare(notices, rows, alias):
    site = [(r, _norm(r[1]), _norm(' '.join(str(x) for x in (r[1], r[3], r[4], r[12])))) for r in rows]
    nos = {r[0] for r in rows}
    groups = defaultdict(list)                                  # 같은 단지의 본공고·취소분·무순위 묶음
    for a in notices:
        groups[(a['area'], re.sub(r'\(.*?\)', '', a['name']).strip())].append(a)
    out = []
    for (area, name), lst in groups.items():
        main = [x for x in lst if not re.search(r'취소|무순위|잔여', x['name'])] or lst
        a = min(main, key=lambda x: x['notice'])
        units = sum(x['units'] for x in main)
        movein = max(x['movein'] for x in lst)
        item = {'area': area, 'name': name, 'notice': a['notice'], 'addr': a['addr'], 'units': units,
                'movein': movein, 'builder': a['builder'], 'union': any(x['union'] for x in lst), 'site_no': None, 'note': None}
        al = alias.get(name)
        if isinstance(al, int) and al in nos:
            item['site_no'] = al
        elif isinstance(al, str):
            item['note'] = al
        else:
            n = _norm(name)
            for r, rn, full in site:
                if n and (n in full or rn in n):
                    item['site_no'] = r[0]; break
            if item['site_no'] is None:                          # 이름이 달라도 같은 동·같은 시공사면 같은 단지로 봄
                dongs = [d for d in re.findall(r'(\S+(?:동|읍|면|리|가))(?=\s|\d)', a['addr'] or '') if not d.endswith('시')]
                for r, rn, full in site:
                    if any(d in full for d in dongs) and _builder(a['builder']) and _builder(a['builder']) in _builder(r[4]) + str(r[4]):
                        item['site_no'] = r[0]; break
        out.append(item)
    return out


def report(items, first, last, now):
    this_month = now.strftime('%Y.%m')
    live = [x for x in items if x['movein'] > this_month]                    # 아직 입주 전
    miss = sorted([x for x in live if x['site_no'] is None and not x['note'] and x['units'] >= MIN_UNITS],
                  key=lambda x: (x['area'], x['notice']))
    small = sorted([x for x in live if x['site_no'] is None and not x['note'] and 30 <= x['units'] < MIN_UNITS],
                   key=lambda x: (x['area'], x['notice']))
    noted = [x for x in live if x['note']]
    L = [f'청약홈 「APT 분양정보」 영남 5개 시도 입주자모집공고 {first[:4]}.{first[4:]}~{last[:4]}.{last[4:]} '
         f'({sum(1 for _ in items)}개 단지)를 사이트 아파트 목록과 대조한 결과입니다. 점검일 {now:%Y-%m-%d}.', '']
    L.append(f'### 사이트에 없는 단지 — 공급 {MIN_UNITS}세대 이상, 입주 전 ({len(miss)}건)')
    if miss:
        L += ['| 지역 | 단지명 | 위치 | 공급 | 모집공고 | 입주예정 | 시공사 |', '|---|---|---|---|---|---|---|']
        L += [f"| {x['area']} | {x['name']}{' (주택조합)' if x['union'] else ''} | {x['addr']} | {x['units']:,} | {x['notice']} | {x['movein']} | {x['builder']} |" for x in miss]
    else:
        L.append('없음')
    L += ['', f'### 공급 30~{MIN_UNITS - 1}세대 — 재개발·조합 단지면 총세대수가 {MIN_UNITS}세대 이상일 수 있어 확인 필요 ({len(small)}건)']
    L += [f"- {x['area']} {x['name']} · {x['addr']} · 공급 {x['units']} · 공고 {x['notice']} · 입주 {x['movein']}" for x in small] or ['없음']
    if noted:
        L += ['', '### 확인 후 제외해 둔 단지 (applyhome_alias.json)']
        L += [f"- {x['area']} {x['name']} — {x['note']}" for x in noted]
    L += ['', '사이트에 추가할 단지는 construction/index.html의 RAW에 넣고, 이름이 달라 자동 대조가 안 되는 단지는 '
          'construction/tools/applyhome_alias.json에 `"청약홈 단지명": 사이트 No`(이미 있음) 또는 `"청약홈 단지명": "제외 사유"`로 적으면 다음 점검부터 빠집니다.']
    return '\n'.join(L), miss, small


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default='applyhome_report.md')
    ap.add_argument('--json', default='applyhome_candidates.json')
    a = ap.parse_args()
    now = datetime.now(KST)
    try:
        notices, first, last = fetch()
        rows = site_rows()
    except Exception as e:
        print(f'조회 실패: {e}', file=sys.stderr)
        sys.exit(1)
    alias = json.loads(ALIAS.read_text(encoding='utf-8')) if ALIAS.exists() else {}
    alias = {k: v for k, v in alias.items() if not k.startswith('_')}
    items = compare(notices, rows, alias)
    text, miss, small = report(items, first, last, now)
    Path(a.out).write_text(text, encoding='utf-8')
    Path(a.json).write_text(json.dumps({'checked': now.isoformat(), 'missing': miss, 'small': small}, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'공고 {len(notices)}건, 단지 {len(items)}개, 사이트 {len(rows)}건 — 누락 후보 {len(miss)}건, 확인 필요 {len(small)}건')
    sys.exit(10 if miss else 0)


if __name__ == '__main__':
    main()
