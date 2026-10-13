"""착공·인허가 통계(trend.html) 자동 갱신 — GitHub Actions에서 매일 실행.

1. 세움터 「인허가정보집계」 목록(로그인 불필요)에서 최신 월별 시군구 파일 월(M)과 연도별 확정치 목록을 확인
2. 국토부 통계누리에 M월 시도 통계가 나왔는지 확인
3. 새 달이 나왔거나(DATA 마지막 달 < M) 새 확정치 연도가 올라왔으면:
   - 통계누리에서 M월까지 60개월 시도 통계(DATA)를 다시 받음
   - 세움터에서 기간 안의 연도는 확정치 zip, 확정치가 없는 연도는 월별 잠정치 파일을 받아 시·군·구(SUB) 구성
   - 시·군·구 합이 시도 통계와 맞는지 검사(어긋나면 파일을 고치지 않고 실패로 종료)
   - trend.html의 데이터 줄과 기간 문구를 바꿈
4. 바뀐 게 없으면 아무것도 하지 않음

  python auto_update.py            # 필요할 때만 갱신
  python auto_update.py --force    # 새 달이 없어도 다시 만듦(검증용)
  python auto_update.py --check    # 접속 확인만(세움터 목록·파일정보, 통계누리)
"""
import argparse
import http.cookiejar
import io
import json
import re
import sys
import urllib.request
import zipfile
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import import_seumter as seum          # noqa: E402  세움터 엑셀 읽기(read_monthly, district, ranges, corr)
import update_trend as ut              # noqa: E402  통계누리 조회(fetch_molit, month_range)

TREND = Path(__file__).resolve().parent.parent / 'trend.html'
EAIS = 'https://www.eais.go.kr'
KST = timezone(timedelta(hours=9))
TOLERANCE = 0.005          # 시·군·구 합 vs 시도 통계 허용 오차(0.5%)

_jar = http.cookiejar.CookieJar()
_op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(_jar))


def _open(req, timeout=120):
    # 세움터는 첫 요청에 쿠키를 주며 307로 같은 주소를 다시 부르게 함 — 쿠키를 받은 뒤 한 번 더 요청
    for _ in range(3):
        try:
            return _op.open(req, timeout=timeout)
        except urllib.error.HTTPError as e:
            if e.code != 307:
                raise
    raise RuntimeError(f'세움터 응답 오류: {req.full_url}')


def eais_list():
    body = json.dumps({'pageNum': 0, 'pageSize': 500, 'archStatSeqno': 0, 'condition': None,
                       'statYearStart': '', 'statYearEnd': '', 'statGbCd': '01', 'statGbNm': '인허가'}).encode()
    req = urllib.request.Request(EAIS + '/awp/AWPAEC01R01', data=body, method='POST',
                                 headers={'Content-Type': 'application/json;charset=UTF-8', 'UntClsfCd': '1000'})
    items = json.loads(_open(req).read())['pageDataList']['content']
    monthly, final = {}, {}
    for x in items:
        if not x.get('fileGrpId'):
            continue
        s = x['subjt']
        if '시군구별' in s and '잠정' in s:
            monthly[f"{int(x['statYear']):04d}-{int(x['statMon']):02d}"] = x['fileGrpId']
        elif re.search(r'월별_인허가현황\(확정치\)', s):
            final[int(x['statYear'])] = x['fileGrpId']
    return monthly, final


def eais_files(grp):
    req = urllib.request.Request(EAIS + '/cba/CBAAZD01R01?grpId=' + grp, headers={'UntClsfCd': '1000'})
    return json.loads(_open(req).read())['ds_Comtnfile']


def eais_download(file_id):
    req = urllib.request.Request(EAIS + '/cba/CBAAZD01E01?fileId=' + file_id, headers={'UntClsfCd': '1000'})
    return _open(req, timeout=600).read()


def molit_has(month):
    """통계누리에 그 달 시도 통계가 나왔는지"""
    try:
        d = ut.fetch_molit([month])
        return d['series']['부산']['start_area'][0] is not None
    except SystemExit:
        return False


def read_zip_bytes(data):
    out = defaultdict(float)
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        for info in sorted(zf.infolist(), key=lambda i: i.filename):
            if '시군구별_용도별' in info.filename and info.filename.lower().endswith(('.xls', '.xlsx')):
                for k, v in seum.read_monthly(info.filename, zf.read(info)).items():
                    out[k] += v
    return out


def build_sub(months, monthly, final, order):
    """기간(months) 시·군·구 값: 확정치 zip이 있는 해는 그것, 없는 해는 월별 잠정치"""
    vals = {}
    years = sorted({int(m[:4]) for m in months})
    final_years = []
    for y in years:
        if y in final:
            files = eais_files(final[y])
            print(f'  {y}년 확정치 zip 받는 중 ({files[0]["orignlFileNm"]}, {files[0]["fileSize"]:,}B)')
            part = read_zip_bytes(eais_download(files[0]['fileId']))
            final_years.append(y)
        else:
            part = {}
            for m in [m for m in months if m.startswith(str(y))]:
                if m not in monthly:
                    sys.exit(f'세움터에 {m} 월별 파일이 없습니다 — 갱신 중단')
                f = eais_files(monthly[m])[0]
                part.update(seum.read_monthly(f['orignlFileNm'], eais_download(f['fileId'])))
        vals.update({k: v for k, v in part.items() if k[3] in months})
    n = len(months)
    col = {'허가': 1, '착공': 2}
    sub = {}
    for sd in order:
        names = list(order[sd])
        found = sorted({d for (k, s, d, m) in vals if s == sd} - set(names))
        unknown = [d for d in found if d != seum.DIRECT]
        if unknown:
            print(f'  확인 필요 — {sd}에 처음 보는 지역명 {unknown} (목록 끝에 추가)')
        names = [x for x in names if x != seum.DIRECT] + unknown + [seum.DIRECT]
        rows = []
        for d in names:
            r = [d, [0] * n, [0] * n]
            for kind, c in col.items():
                for i, m in enumerate(months):
                    r[c][i] = round(vals.get((kind, sd, d, m), 0))
            rows.append(r)
        sub[sd] = rows
    covered = defaultdict(set)
    for kind, sd, d, m in vals:
        covered[kind].add(m)
    return sub, {k: seum.ranges(v) for k, v in covered.items()}, final_years


def keep_backdata(sub, sub_old, old_months, months, ranges):
    """SUB_SRC['착공_백데이터'] 구간의 착공은 사업계획 백데이터 값을 그대로 둠(세움터 확정치로 덮어쓰지 않음).
    반환: 고정한 달 집합"""
    frozen = {m for a, b in ranges for m in months if a <= m <= b and m in old_months}
    if not frozen:
        return frozen
    for sd in sub:
        old = {r[0]: r for r in sub_old.get(sd, [])}
        rows = {r[0]: r for r in sub[sd]}
        for name in old:
            if name not in rows:                      # 백데이터에만 있던 항목도 유지
                r = [name, [0] * len(months), [0] * len(months)]
                sub[sd].insert(len(sub[sd]) - 1, r)
                rows[name] = r
        for name, r in rows.items():
            for i, m in enumerate(months):
                if m in frozen:
                    r[2][i] = old[name][2][old_months.index(m)] if name in old else 0
    print(f'  착공 {min(frozen)}~{max(frozen)}은 사업계획 백데이터 값 유지')
    return frozen


def validate(sub, data, skip_start=frozenset()):
    bad, valid = [], {}
    n = len(data['months'])
    for sd in data['regions']:
        tp = [sum(r[1][i] for r in sub[sd]) for i in range(n)]
        ts = [sum(r[2][i] for r in sub[sd]) for i in range(n)]
        op, os_ = data['series'][sd]['permit_area'], data['series'][sd]['start_area']
        for i, m in enumerate(data['months']):
            for a, b, k in ((tp[i], op[i], '허가'), (ts[i], os_[i], '착공')):
                if k == '착공' and m in skip_start:      # 백데이터(잠정치)로 고정한 달은 확정치와 다를 수 있음
                    continue
                if abs(a - b) > max(50, TOLERANCE * b):
                    bad.append(f'{sd} {m} {k}: 시군구합 {a:,.0f} / 시도 {b:,.0f}')
        valid[sd] = [round(sum(tp) / sum(op), 2), round(seum.corr(tp, op), 2),
                     round(sum(ts) / sum(os_), 2), round(seum.corr(ts, os_), 2)]
    return bad, valid


def molit_provisional(months):
    """통계누리 응답에서 'p)'(잠정) 표시된 달"""
    s, e = months[0].replace('-', ''), months[-1].replace('-', '')
    req = urllib.request.Request(ut.MOLIT.format(form=2202, style=838, s=s, e=e), headers=ut.UA)
    rows = json.load(urllib.request.urlopen(req, timeout=300))['data']
    return sorted({r['0'][:7] for r in rows if 'p' in r['0']})


def update_texts(html, months, prov):
    first, last = months[0], months[-1]
    today = datetime.now(KST).strftime('%Y-%m-%d')
    dot = lambda m: m.replace('-', '.')
    html = re.sub(r'조회기간 \d{4}\.\d{2}~\d{4}\.\d{2} \(60개월\)', f'조회기간 {dot(first)}~{dot(last)} (60개월)', html)
    html = re.sub(r'조회기간 \d{4}-\d{2}~\d{4}-\d{2}, 조회일 \d{4}-\d{2}-\d{2}', f'조회기간 {first}~{last}, 조회일 {today}', html)
    if prov:
        html = re.sub(r"\d{4}-\d{2}~\d{4}-\d{2} 자료는 원 통계에서 '잠정치'로 표기되며",
                      f"{prov[0]}~{prov[-1]} 자료는 원 통계에서 '잠정치'로 표기되며", html)
    win = int(re.search(r'const CUM_WIN = (\d+);', html).group(1))
    lo = ut.month_range(last.replace('-', ''), win)[0]
    html = re.sub(r'\(예: \d{4}-\d{2} → \d{4}-\d{2}~\d{4}-\d{2}\)', f'(예: {last} → {lo}~{last})', html)
    html = re.sub(r'데이터 시작\(\d{4}-\d{2}\)부터 (\d+)개월이 채워지는 \d{4}-\d{2}부터',
                  lambda m: f'데이터 시작({first})부터 {m.group(1)}개월이 채워지는 {months[int(m.group(1)) - 1]}부터', html)
    return html


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()

    html = TREND.read_text(encoding='utf-8')
    data_old = json.loads(re.search(r'const DATA =(\{.*?\});\n', html).group(1))
    sub_old = json.loads(re.search(r'const SUB = (\{.*?\});\n', html).group(1))
    src_old = json.loads(re.search(r'const SUB_SRC = (\{.*?\});\n', html).group(1))

    monthly, final = eais_list()
    latest = max(monthly)
    print(f'세움터: 월별 잠정치 최신 {latest}, 확정치 연도 {sorted(final)}')
    if a.check:
        f = eais_files(monthly[latest])[0]
        print(f'  파일정보 OK: {f["orignlFileNm"]} {f["fileSize"]:,}B')
        print(f'  통계누리 {latest}: {"있음" if molit_has(latest) else "없음"}')
        return

    target = latest
    for _ in range(3):                                 # 통계누리가 아직 그 달을 안 냈으면 한 달씩 앞으로
        if molit_has(target):
            break
        print(f'통계누리에 {target}이 아직 없음')
        target = ut.month_range(target.replace('-', ''), 2)[0]
    else:
        sys.exit('통계누리에서 최근 3개월 자료를 찾지 못했습니다')
    months = ut.month_range(target.replace('-', ''))
    old_final = src_old.get('확정', 0)
    new_final = max([y for y in final if int(months[0][:4]) <= y <= int(months[-1][:4])], default=0)
    if not a.force and target <= data_old['months'][-1] and new_final <= old_final:
        print(f'변경 없음 (현재 {data_old["months"][-1]}, 확정치 {old_final}년까지)')
        return
    print(f'갱신: {months[0]} ~ {target} (확정치 {new_final}년까지)')

    data = ut.fetch_molit(months)
    order = {sd: [r[0] for r in sub_old[sd]] for sd in data['regions']}
    sub, src, final_years = build_sub(months, monthly, final, order)
    src['확정'] = max(final_years, default=0)
    frozen = keep_backdata(sub, sub_old, data_old['months'], months, src_old.get('착공_백데이터', []))
    if frozen:
        src['착공_백데이터'] = src_old['착공_백데이터']
    bad, valid = validate(sub, data, skip_start=frozen)
    if bad:
        print('시·군·구 합이 시도 통계와 맞지 않아 중단합니다:')
        print('\n'.join('  ' + b for b in bad[:30]))
        sys.exit(1)
    print('검증 통과 — 시·군·구 합 = 시도 통계 (', json.dumps(valid, ensure_ascii=False), ')')

    dump = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':'))
    html = re.sub(r'const DATA =\{.*?\};\n', lambda _: f'const DATA ={dump(data)};\n', html, count=1)
    html = re.sub(r'const SUB = \{.*?\};\n', lambda _: f'const SUB = {dump(sub)};\n', html, count=1)
    html = re.sub(r'const SUB_VALID = \{.*?\};\n', lambda _: f'const SUB_VALID = {dump(valid)};\n', html, count=1)
    html = re.sub(r'const SUB_SRC = \{.*?\};\n', lambda _: f'const SUB_SRC = {dump(src)};\n', html, count=1)
    html = update_texts(html, months, molit_provisional(months))
    TREND.write_text(html, encoding='utf-8', newline='')
    print(f'{TREND.name} 갱신 완료')


if __name__ == '__main__':
    main()
