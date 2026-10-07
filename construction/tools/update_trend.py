"""착공·인허가 통계(construction/trend.html) 데이터 갱신 스크립트.

하는 일
  1. 국토부 통계누리에서 시도별 착공·허가 60개월치를 받아 DATA를 만든다.
  2. 건축HUB 대용량 원자료(건축인허가·주택인허가 기본개요 zip)로 시·군·구 월별 연면적(SUB)을 집계한다.
  3. 원자료 합계를 시도 공식 통계와 비교해 검증 수치(SUB_VALID)를 만든다.
  4. trend.html 안의 const DATA / SUB / SUB_VALID 세 줄만 교체한다.

사용법 (Python 3.9+, 표준 라이브러리만 사용)
  python update_trend.py --end 202608 --permit-zip 건축.zip --housing-zip 주택.zip
  python update_trend.py --end 202608 --download            # 원자료 zip도 받아서 진행 (약 450MB)
  python update_trend.py --end 202608 ... --dry-run          # 파일은 고치지 않고 결과만 출력

자세한 규칙과 주의사항은 같은 폴더의 README.md 참고.
"""
import argparse
import io
import json
import re
import sys
import urllib.parse
import urllib.request
import zipfile
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

TREND = Path(__file__).resolve().parent.parent / 'trend.html'
REGIONS = ['부산', '울산', '대구', '경남', '경북']
SIDO_NAME = {'부산광역시': '부산', '울산광역시': '울산', '대구광역시': '대구', '경상남도': '경남', '경상북도': '경북'}
CODE_PREFIX = {'26': '부산', '27': '대구', '31': '울산', '47': '경북', '48': '경남'}
MOLIT = 'https://stat.molit.go.kr/portal/stat/data.do?formId={form}&styleNum={style}&apprYn=Y&startDate={s}&endDate={e}'
MOLIT_FORMS = {'start': (2202, 838), 'permit': (2200, 839)}  # 시도별 건축착공현황 / 건축허가현황
HUB_LIST = 'https://www.hub.go.kr/portal/opn/lps/idx-lgcpt-pvsn-srvc-list.do'
HUB_DOWN = 'https://www.hub.go.kr/cmm/fms/fileOpnDown.do'
UA = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://stat.molit.go.kr/'}


def month_range(end, n=60):
    y, m = int(end[:4]), int(end[4:6])
    out = []
    for _ in range(n):
        out.append(f'{y:04d}-{m:02d}')
        m -= 1
        if m == 0:
            y, m = y - 1, 12
    return out[::-1]


# ── 1. 시도 공식 통계 ──
def fetch_molit(months):
    s, e = months[0].replace('-', ''), months[-1].replace('-', '')
    vals = {}
    for kind, (form, style) in MOLIT_FORMS.items():
        req = urllib.request.Request(MOLIT.format(form=form, style=style, s=s, e=e), headers=UA)
        rows = json.load(urllib.request.urlopen(req, timeout=300))['data']
        for r in rows:
            # '계/계' = 모든 용도·구조 합계, 열 '9' = 합계
            if r['2'] != '계' or r['3'] != '계' or r['1'] not in SIDO_NAME:
                continue
            v = r['9'].replace(',', '')
            vals[(kind, SIDO_NAME[r['1']], r['0'][:7], r['4'])] = float(v) if v not in ('-', '') else 0.0
    missing = [m for m in months if ('start', '부산', m, '연면적') not in vals]
    if missing:
        sys.exit(f'국토부 통계에 아직 없는 월: {missing} — --end를 공표된 마지막 달로 지정하세요.')
    series = {}
    for r in REGIONS:
        series[r] = {
            'permit_count': [vals[('permit', r, m, '동수')] for m in months],
            'permit_area': [vals[('permit', r, m, '연면적')] for m in months],
            'start_count': [vals[('start', r, m, '동수')] for m in months],
            'start_area': [vals[('start', r, m, '연면적')] for m in months],
        }
    return {'months': months, 'regions': REGIONS, 'series': series}


# ── 2. 건축HUB 원자료 ──
def hub_opener():
    import http.cookiejar
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))


def find_hub_file(opener, code):
    """대용량 제공 서비스 목록(01=건축인허가, 02=주택인허가)에서 '기본개요' 파일 ID·기준월·CSRF 토큰을 찾는다."""
    for page in range(1, 4):
        body = urllib.parse.urlencode({'opnLgcptTaskSeCd': code, 'pageIndex': page}).encode()
        html = opener.open(HUB_LIST, body, timeout=60).read().decode('utf-8', 'ignore')
        csrf = re.search(r'name="_csrf" value="([^"]+)"', html).group(1)
        for m in re.finditer(r"fnDownloadPop\('\d+','\d+','(OPN\d+)'\)", html):
            # 다운로드 버튼 바로 앞의 제목이 이 버튼의 파일 이름
            text = re.sub(r'<[^>]+>', ' ', html[max(0, m.start() - 1500):m.start()])
            titles = re.findall(r'([가-힣]+)\s*\((\d{4})년\s*(\d{2})월\)', text)
            if titles and titles[-1][0] == '기본개요':
                return m.group(1), f'{titles[-1][1]}-{titles[-1][2]}', csrf
    sys.exit(f'건축HUB 목록에서 기본개요 파일을 찾지 못했습니다(구분 {code}).')


def download_hub(dest):
    """'기본개요' 최신 파일 두 개(건축 약 440MB, 주택 약 7.5MB)를 받는다."""
    opener = hub_opener()
    paths = {}
    for code, label in (('01', 'permit'), ('02', 'housing')):
        fid, ref, csrf = find_hub_file(opener, code)
        out = Path(dest) / f'{label}_basis_{ref}.zip'
        print(f'  다운로드: {label} 기본개요 ({ref}분) → {out}')
        body = urllib.parse.urlencode({'srvrFileNm': fid, '_csrf': csrf}).encode()
        with opener.open(HUB_DOWN, body, timeout=3600) as resp, open(out, 'wb') as f:
            while chunk := resp.read(1 << 20):
                f.write(chunk)
        paths[label] = out
    return paths['permit'], paths['housing']


def ym(d):
    d = d.strip()
    return f'{d[:4]}-{d[4:6]}' if len(d) >= 6 and d[:6].isdigit() and d[:8] <= '20991231' else None


def open_txt(zip_path):
    zf = zipfile.ZipFile(zip_path)
    return io.TextIOWrapper(zf.open(zf.namelist()[0]), encoding='utf-8', errors='ignore')


def aggregate_hub(permit_zip, housing_zip):
    """시군구코드별 월 연면적. 반환: permit[(코드,월)], start[(코드,월)], 코드→이름 빈도, 마지막 기록일"""
    permit, start = defaultdict(float), defaultdict(float)
    names = defaultdict(Counter)
    last = ''
    today = date.today().strftime('%Y%m%d')

    # 건축인허가 기본개요(41필드): [1]대지위치 [3]시군구코드 [20]건축구분명 [24]연면적 [37]실제착공일 [38]허가일
    # 규칙: 신축만 (증축·대수선·용도변경은 '건물 전체 연면적'이 들어 있어 공식 통계의 10~28배로 부풂)
    for line in open_txt(permit_zip):
        p = line.rstrip('\n').split('|')
        if len(p) < 39 or p[3][:2] not in CODE_PREFIX or p[20].strip() != '신축':
            continue
        try:
            area = float(p[24] or 0)
        except ValueError:
            continue
        t = p[1].split()
        if len(t) > 1:
            names[p[3]][t[1]] += 1
        if (m := ym(p[38])):
            permit[(p[3], m)] += area
            if p[38].strip()[:8] <= today:  # 원자료에 미래 날짜 오기가 섞여 있음
                last = max(last, p[38].strip()[:8])
        if (m := ym(p[37])):
            start[(p[3], m)] += area

    # 주택인허가 기본개요(29필드): [1]대지위치 [3]시군구 [4]법정동 [6]본번 [7]부번 [15]동수 [16]연면적 [17]세대수 [23]사업승인일 [25]실제착공일
    # 규칙: 세대·동이 있고 세대당 10~1,000㎡인 행만. 필지·세대수·면적(100㎡ 단위)이 같으면 한 사업(변경 기록 중복).
    #       승인월 = 묶음 첫 기록의 승인일, 착공월 = 묶음 안에서 실제 착공일이 적힌 기록. 착공예정일은 쓰지 않음.
    groups = defaultdict(list)
    for line in open_txt(housing_zip):
        p = line.rstrip('\n').split('|')
        if len(p) < 26 or p[3][:2] not in CODE_PREFIX:
            continue
        try:
            area, hh, dong = float(p[16] or 0), int(float(p[17] or 0)), int(float(p[15] or 0))
        except ValueError:
            continue
        if hh <= 0 or dong <= 0 or not (10 <= area / hh <= 1000):
            continue
        t = p[1].split()
        if len(t) > 1:
            names[p[3]][t[1]] += 1
        groups[(p[3], p[4], p[6], p[7], hh, round(area / 100))].append((area, p[23], p[25]))
    for key, recs in groups.items():
        area, appr, _ = recs[0]
        if (m := ym(appr)):
            permit[(key[0], m)] += area
        rec = next((r for r in recs if r[2].strip()), None)
        if rec and (m := ym(rec[2])):
            start[(key[0], m)] += rec[0]
    return permit, start, names, last


def build_sub(permit, start, names, months, district_order):
    """시·군·구 단위로 묶는다. 이름은 대지위치 두 번째 낱말(광역시는 구·군, 도는 시·군 — 창원시·포항시의 구는 자동으로 시로 합쳐짐)."""
    code_name = {c: cnt.most_common(1)[0][0] for c, cnt in names.items() if cnt}
    by_name = defaultdict(list)
    for c, n in code_name.items():
        by_name[(CODE_PREFIX[c[:2]], n)].append(c)
    sub = {}
    for sd in REGIONS:
        rows = []
        for name in district_order[sd]:
            cs = by_name.get((sd, name), [])
            rows.append([name,
                         [round(sum(permit.get((c, m), 0) for c in cs)) for m in months],
                         [round(sum(start.get((c, m), 0) for c in cs)) for m in months]])
        sub[sd] = rows
        extra = sorted({n for (s, n) in by_name if s == sd} - set(district_order[sd]))
        if extra:
            print(f'  참고: {sd}에 기존 목록에 없는 지역명 {extra} — 행정구역 변경이면 trend.html의 SUB 목록 순서를 확인하세요.')
    return sub


def corr(a, b):
    n = len(a)
    ma, mb = sum(a) / n, sum(b) / n
    cov = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    va = sum((x - ma) ** 2 for x in a) ** .5
    vb = sum((y - mb) ** 2 for y in b) ** .5
    return cov / (va * vb) if va and vb else 0.0


def validate(sub, data):
    """[인허가 공식 대비 비율, 인허가 월별 상관, 착공 비율, 착공 상관]"""
    out = {}
    for sd in REGIONS:
        n = len(data['months'])
        tp = [sum(r[1][i] for r in sub[sd]) for i in range(n)]
        ts = [sum(r[2][i] for r in sub[sd]) for i in range(n)]
        op, os_ = data['series'][sd]['permit_area'], data['series'][sd]['start_area']
        out[sd] = [round(sum(tp) / sum(op), 2), round(corr(tp, op), 2), round(sum(ts) / sum(os_), 2), round(corr(ts, os_), 2)]
    return out


def main():
    ap = argparse.ArgumentParser(description='trend.html 데이터 갱신')
    ap.add_argument('--end', required=True, help='마지막 월 YYYYMM (국토부 통계가 공표된 달)')
    ap.add_argument('--permit-zip', help='건축인허가 기본개요 zip')
    ap.add_argument('--housing-zip', help='주택인허가 기본개요 zip')
    ap.add_argument('--download', action='store_true', help='건축HUB에서 최신 기본개요 zip 두 개를 받음(약 450MB)')
    ap.add_argument('--workdir', default='.', help='다운로드 저장 폴더')
    ap.add_argument('--dry-run', action='store_true', help='trend.html은 고치지 않음')
    a = ap.parse_args()

    html = TREND.read_text(encoding='utf-8')
    old_sub = json.loads(re.search(r'const SUB = (\{.*?\});\n', html).group(1))
    district_order = {sd: [r[0] for r in old_sub[sd]] for sd in REGIONS}

    months = month_range(a.end)
    print(f'1) 국토부 통계 {months[0]} ~ {months[-1]}')
    data = fetch_molit(months)

    if a.download:
        permit_zip, housing_zip = download_hub(a.workdir)
    elif a.permit_zip and a.housing_zip:
        permit_zip, housing_zip = a.permit_zip, a.housing_zip
    else:
        sys.exit('--permit-zip/--housing-zip 을 주거나 --download 를 쓰세요.')

    print('2) 건축HUB 원자료 집계 (몇 분 걸림)')
    permit, start, names, last = aggregate_hub(permit_zip, housing_zip)
    print(f'   원자료 마지막 허가일: {last}')
    if last[:6] < a.end:
        print(f'   경고: 원자료가 {a.end[:4]}-{a.end[4:]}까지 다 들어 있지 않습니다. 시·군·구 최근 달 값이 작게 나옵니다.')
    sub = build_sub(permit, start, names, months, district_order)

    valid = validate(sub, data)
    print('3) 검증 [인허가 비율, 상관, 착공 비율, 상관]:', json.dumps(valid, ensure_ascii=False))
    for sd in REGIONS:
        r = [f'{m}:{sum(x[1][i] for x in sub[sd]) / (data["series"][sd]["permit_area"][i] or 1):.2f}'
             for i, m in list(enumerate(months))[-3:]]
        print(f'   {sd} 최근 3개월 인허가 비율(원자료/공식): {r}')

    if a.dry_run:
        print('dry-run: trend.html은 그대로 둡니다.')
        return
    dump = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':'))
    html, n1 = re.subn(r'const DATA =\{.*?\};\n', lambda _: f'const DATA ={dump(data)};\n', html, count=1)
    html, n2 = re.subn(r'const SUB = \{.*?\};\n', lambda _: f'const SUB = {dump(sub)};\n', html, count=1)
    html, n3 = re.subn(r'const SUB_VALID = \{.*?\};\n', lambda _: f'const SUB_VALID = {dump(valid)};\n', html, count=1)
    if (n1, n2, n3) != (1, 1, 1):
        sys.exit('trend.html에서 DATA/SUB/SUB_VALID 줄을 찾지 못했습니다.')
    TREND.write_text(html, encoding='utf-8', newline='')
    print(f'4) {TREND} 갱신 완료.')
    print('   직접 고칠 문구: 헤더 "조회기간", 하단 출처의 조회기간·조회일·잠정치 구간·검증 비율 범위, 누적 조회 예시 월 (README 참고)')


if __name__ == '__main__':
    main()
