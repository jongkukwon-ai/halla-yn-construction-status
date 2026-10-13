"""세움터 시군구별 집계 → trend.html의 시·군·구 데이터(SUB)에 반영.

세움터 「인허가정보집계」에서 받은 공식 시·군·구 수치로, 자체 집계(update_trend.py)한 값을 덮어쓴다.
덮어쓴 달은 SUB_SRC에 기록되어 화면 안내문에 '세움터 집계'로 표시된다.

입력 세 가지 (여러 개 섞어서 줄 수 있음, 같은 달이 겹치면 뒤에 준 파일이 이김)
  1) 세움터 월별 파일  : 「시군구별_용도별_건축허가_착공_준공_현황(YYYY년MM월).xlsx/.xls」 → 그 달 허가·착공
  2) 연도별 확정치 zip : 「YYYY년_월별_인허가현황(확정치).zip」 (안의 시군구별 파일 12개) → 1년치 허가·착공
  3) 착공 백데이터 파일 : 시트 '데이터'(연월·구분·시도_현재·시군구_현재·…·연면적_㎡) → 여러 달 착공

사용법 (openpyxl 필요, .xls는 xlrd 필요: pip install openpyxl xlrd)
  python import_seumter.py <백데이터.xlsx> <월별파일1.xlsx> [<월별파일2.xlsx> ...]
  python import_seumter.py ... --dry-run

순서: 매달 update_trend.py로 기간(DATA)을 새 달까지 민 뒤, 이 스크립트에 백데이터와 그 뒤 월별 파일을 모두 넘긴다
(update_trend.py는 SUB를 원자료로 새로 만들기 때문에 세움터 값을 다시 덮어써야 함).
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import openpyxl

TREND = Path(__file__).resolve().parent.parent / 'trend.html'
SIDO = {'부산광역시': '부산', '울산광역시': '울산', '대구광역시': '대구', '경상남도': '경남', '경상북도': '경북'}
DIRECT = '시·도 직접'   # 시군구 칸이 빈 행 = 시·도가 직접 처리한 건(대단지 주택 등)


def district(name):
    if not name or name in ('시도 직접', '소계'):
        return DIRECT if name != '소계' else None
    name = str(name).replace(' ', '')
    m = re.match(r'(창원시|포항시)', name)          # 일반구는 시 단위로 합침(사이트 기준)
    return m.group(1) if m else name


def sheets(name, data):
    """xlsx(openpyxl)·xls(xlrd, 2024년 이전 확정치 파일) 공통: {시트명: 행 리스트}"""
    import io
    if name.lower().endswith('.xls'):
        import xlrd   # pip install xlrd
        wb = xlrd.open_workbook(file_contents=data)
        return {s.name: [s.row_values(r) for r in range(s.nrows)] for s in wb.sheets()}
    wb = openpyxl.load_workbook(io.BytesIO(data), read_only=True, data_only=True)
    return {ws.title: [list(r) for r in ws.iter_rows(values_only=True)] for ws in wb.worksheets}


def read_raw(name, data):
    """세움터 시군구별 파일 → {('허가'|'착공', 시도 원래 이름, 시군구 원래 표기(빈칸은 None), 'YYYY-MM'): ㎡} (전국)"""
    sh = sheets(name, data)
    text = ' '.join(str(c) for r in sh['목차'] for c in r if c)
    m = re.search(r'(\d{4})\.(\d{2})\.01\s*~', text) or re.search(r'(\d{4})년\s*(\d{2})월', Path(name).name)
    if not m:
        sys.exit(f'{name}: 기준 월을 찾지 못했습니다.')
    month = f'{m.group(1)}-{m.group(2)}'
    out = defaultdict(float)
    totals = {}
    for title, rows in sh.items():
        kind = '허가' if '허가' in title else '착공' if '착공' in title else None
        if not kind or not title.endswith('_01'):       # _01 시트의 3번째 열이 총계
            continue
        for r in rows:
            if not r or not isinstance(r[0], str) or not isinstance(r[2], (int, float)):
                continue
            if r[0] not in NAT_SIDO:
                if r[0] not in ('총계', '합계', '전국'):
                    print(f'  확인 필요 — {Path(name).name}: 처음 보는 시도 이름 {r[0]!r} (건너뜀)')
                continue
            if r[1] == '소계':
                totals[(kind, r[0])] = r[2]
                continue
            out[(kind, r[0], r[1] if r[1] not in ('', None) else None, month)] += r[2]
    for (kind, sd), v in totals.items():                  # 시도 소계와 시·군·구 합이 맞는지 확인
        s = sum(x for (k, a, _, _m), x in out.items() if k == kind and a == sd)
        if abs(s - v) > 1:
            print(f'  경고 {Path(name).name} {month} {kind} {sd}: 소계 {v:,.0f} ≠ 시군구 합 {s:,.0f}')
    basis = re.search(r'자료기준일\s*:\s*([\d.]+)', text)
    print(f'  {Path(name).name}: {month} 허가·착공 (자료기준일 {basis.group(1) if basis else "?"})')
    return out


def to_yn(raw):
    """원래 표기 → 영남권 키 {(종류, 시도, 구군, 월): ㎡}"""
    out = defaultdict(float)
    for (kind, sido, name, month), v in raw.items():
        if sido not in SIDO:
            continue
        sd, d = SIDO[sido], district(name)
        if sd == '경북' and d == '군위군':                # 2023.7 대구 편입 — 사이트는 현재 행정구역(대구)으로 둠
            sd = '대구'
        out[(kind, sd, d, month)] += v
    return out


def read_monthly(name, data):
    """세움터 월별 파일 → {('허가'|'착공', 시도, 구군, 'YYYY-MM'): ㎡} (영남권)"""
    return to_yn(read_raw(name, data))


# ── 전국: 시도는 현재 행정구역 16곳, 시·군·구는 사업계획 백데이터의 '비교단위'(기간 내내 같은 경계) ──
NAT_REGIONS = ['서울', '부산', '대구', '인천', '대전', '울산', '세종', '경기', '강원',
               '충북', '충남', '전북', '전남광주', '경북', '경남', '제주']
NAT_SIDO = {'서울특별시': '서울', '부산광역시': '부산', '대구광역시': '대구', '인천광역시': '인천',
            '광주광역시': '전남광주', '대전광역시': '대전', '울산광역시': '울산', '세종특별자치시': '세종',
            '경기도': '경기', '강원도': '강원', '강원특별자치도': '강원', '충청북도': '충북', '충청남도': '충남',
            '전라북도': '전북', '전북특별자치도': '전북', '전라남도': '전남광주', '전남광주통합특별시': '전남광주',
            '경상북도': '경북', '경상남도': '경남', '제주특별자치도': '제주'}
# 2026.7 인천 개편: 옛 중구·동구 → 제물포구·영종구, 옛 서구 → 서해구·검단구 (1:1 대응이 안 돼 권역으로 묶음)
INCHEON = {**dict.fromkeys(['중구', '동구', '제물포구', '영종구'], '중구·동구 권역(제물포구+영종구)'),
           **dict.fromkeys(['서구', '서해구', '검단구'], '서구 권역(서해구+검단구)')}


def nat_place(sido, name):
    """(시도 원래 이름, 시군구 원래 표기) → (현재 시도 약칭, 비교단위). 일반구는 시로, 경북 군위군은 대구로"""
    sd = NAT_SIDO[sido]
    name = '' if name is None else str(name).replace(' ', '')
    if name in ('', '시도직접'):
        return sd, DIRECT
    if sd == '경북' and name == '군위군':
        return '대구', name
    if sd == '인천' and name in INCHEON:
        return sd, INCHEON[name]
    m = re.match(r'(.+?시).+구$', name)
    return sd, (m.group(1) if m else name)


def to_nat(raw):
    out = defaultdict(float)
    for (kind, sido, name, month), v in raw.items():
        sd, d = nat_place(sido, name)
        out[(kind, sd, d, month)] += v
    return out


def read_zip(path):
    """연도별 확정치 zip — 안의 「시군구별_용도별…」 파일만 읽음 (원래 표기)"""
    import zipfile
    out = defaultdict(float)
    with zipfile.ZipFile(path) as zf:
        for info in sorted(zf.infolist(), key=lambda i: i.filename):
            if '시군구별_용도별' in info.filename and info.filename.lower().endswith(('.xls', '.xlsx')):
                for k, v in read_raw(info.filename, zf.read(info)).items():
                    out[k] += v
    return out


def read_backdata(path):
    """사업계획 백데이터(시트 '데이터') 착공 → 원래 표기(시도·시군구 열, 전국)"""
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    out = defaultdict(float)
    for r in wb['데이터'].iter_rows(min_row=2, values_only=True):
        if r[3] == '착공' and r[8] in NAT_SIDO and r[2]:
            out[('착공', r[8], None if r[9] == '시도 직접' else r[9], r[2])] += r[15] or 0
    months = sorted({k[3] for k in out})
    print(f'  {Path(path).name}: 착공 {months[0]} ~ {months[-1]}')
    return out


def ranges(months):
    """['2021-09','2021-10',…] → [['2021-09','2026-08'], …] (연속 구간)"""
    def idx(m): y, mm = map(int, m.split('-')); return y * 12 + mm
    out = []
    for m in sorted(months):
        if out and idx(m) == idx(out[-1][1]) + 1:
            out[-1][1] = m
        else:
            out.append([m, m])
    return out


def corr(a, b):
    n = len(a); ma, mb = sum(a) / n, sum(b) / n
    c = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    va = sum((x - ma) ** 2 for x in a) ** .5; vb = sum((y - mb) ** 2 for y in b) ** .5
    return c / (va * vb) if va and vb else 0.0


def build_nat_sub(vals, months, skip, old):
    """전국 시·군·구 표(영남 5개 시도는 SUB에 있으므로 뺌). old의 순서를 따르고 새 이름은 가나다순으로 뒤에, 시·도 직접은 맨 뒤"""
    n = len(months)
    sub = {}
    for sd in NAT_REGIONS:
        if sd in skip:
            continue
        names = {d for (k, s, d, m) in vals if s == sd and m in months}
        order = [x for x in (r[0] for r in old.get(sd, [])) if x != DIRECT]
        new = sorted(names - set(order) - {DIRECT})
        if old and new:
            print(f'  확인 필요 — {sd}에 처음 보는 지역명 {new} (목록 끝에 추가)')
        rows = []
        for d in order + new + ([DIRECT] if DIRECT in names or DIRECT in {r[0] for r in old.get(sd, [])} else []):
            rows.append([d] + [[round(vals.get((kind, sd, d, m), 0)) for m in months] for kind in ('허가', '착공')])
        sub[sd] = rows
    return sub


def sub_valid(sub, data):
    """[인허가 공식 대비 비율, 인허가 상관, 착공 비율, 착공 상관]"""
    n = len(data['months'])
    valid = {}
    for sd in sub:
        tp = [sum(r[1][i] for r in sub[sd]) for i in range(n)]
        ts = [sum(r[2][i] for r in sub[sd]) for i in range(n)]
        op, os_ = data['series'][sd]['permit_area'], data['series'][sd]['start_area']
        valid[sd] = [round(sum(tp) / sum(op), 2), round(corr(tp, op), 2), round(sum(ts) / sum(os_), 2), round(corr(ts, os_), 2)]
    return valid


def write_nat(html, nat, nat_sub, nat_valid):
    """NAT(시도 16곳 목록 + 영남 외 시도 통계), NAT_SUB, NAT_VALID 줄을 바꾸거나 SUB_VALID 뒤에 새로 넣음"""
    dump = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':'))
    nat = {'regions': nat['regions'], 'series': {sd: v for sd, v in nat['series'].items() if sd in nat_sub}}
    lines = {'NAT': dump(nat), 'NAT_SUB': dump(nat_sub), 'NAT_VALID': dump(nat_valid)}
    if 'const NAT = ' in html:
        for k, v in lines.items():
            html = re.sub(rf'const {k} = \{{.*?\}};\n', lambda _: f'const {k} = {v};\n', html, count=1)
        return html
    block = ('// 전국 조회: 시도는 현재 행정구역 16곳(광주·전남 → 전남광주, 군위 → 대구), 시·군·구는 일반구를 시로 묶은 비교단위.\n'
             '// 영남 5개 시도는 DATA·SUB를 그대로 쓰므로 여기엔 나머지 시도만 둠\n'
             + ''.join(f'const {k} = {v};\n' for k, v in lines.items()))
    m = re.search(r'const SUB_VALID = \{.*?\};\n', html)
    return html[:m.end()] + block + html[m.end():]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('files', nargs='+')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--national', action='store_true', help='전국 조회용 NAT·NAT_SUB·NAT_VALID도 만듦(통계누리 접속)')
    a = ap.parse_args()

    html = TREND.read_text(encoding='utf-8')
    data = json.loads(re.search(r'const DATA =(\{.*?\});\n', html).group(1))
    sub = json.loads(re.search(r'const SUB = (\{.*?\});\n', html).group(1))
    months = data['months']
    n = len(months)

    # 파일 순서대로 읽고, 같은 종류·같은 달이 겹치면 뒤에 준 파일 값으로 통째로 바꿈
    vals = {}
    for f in a.files:
        p = Path(f)
        if p.suffix.lower() == '.zip':
            part = read_zip(p)
        elif p.suffix.lower() == '.xlsx' and '데이터' in openpyxl.load_workbook(p, read_only=True).sheetnames:
            part = read_backdata(p)
        else:
            part = read_raw(p.name, p.read_bytes())
        months_in = {(k[0], k[3]) for k in part}
        for key in [k for k in vals if (k[0], k[3]) in months_in]:
            del vals[key]
        vals.update(part)
    raw, vals = vals, to_yn(vals)

    covered = defaultdict(set)                        # 종류별로 세움터 값으로 바꾼 달
    for kind, sd, dist, m in vals:
        if m in months:
            covered[kind].add(m)

    col = {'허가': 1, '착공': 2}
    for sd in data['regions']:
        rows = {r[0]: r for r in sub[sd]}
        names = {d for (k, s, d, m) in vals if s == sd and m in months}
        new = sorted(names - set(rows))
        if [d for d in new if d != DIRECT]:
            print(f'  확인 필요 — {sd}에 기존 목록에 없는 이름: {[d for d in new if d != DIRECT]}')
        for d in new:                                  # 시·도 직접 등 새 항목
            rows[d] = [d, [0] * n, [0] * n]
            sub[sd].append(rows[d])
        for kind, ms in covered.items():
            for m in ms:
                i = months.index(m)
                for r in sub[sd]:
                    r[col[kind]][i] = round(vals.get((kind, sd, r[0], m), 0))
        # 시·도 직접은 맨 뒤로
        sub[sd].sort(key=lambda r: r[0] == DIRECT)

    src = {k: ranges(v) for k, v in covered.items()}
    old_src = re.search(r'const SUB_SRC = (\{.*?\});\n', html)
    for k, v in (json.loads(old_src.group(1)) if old_src else {}).items():
        if k not in src:                               # 확정·착공_백데이터 같은 표시용 키는 유지
            src[k] = v
    valid = {}
    for sd in data['regions']:
        tp = [sum(r[1][i] for r in sub[sd]) for i in range(n)]
        ts = [sum(r[2][i] for r in sub[sd]) for i in range(n)]
        op, os_ = data['series'][sd]['permit_area'], data['series'][sd]['start_area']
        valid[sd] = [round(sum(tp) / sum(op), 2), round(corr(tp, op), 2), round(sum(ts) / sum(os_), 2), round(corr(ts, os_), 2)]
    print('세움터 반영 구간:', json.dumps(src, ensure_ascii=False))
    print('시도 합계 대비 [허가 비율, 상관, 착공 비율, 상관]:', json.dumps(valid, ensure_ascii=False))
    if a.national:
        import update_trend as ut
        nat = ut.fetch_molit(months, national=True)
        old = re.search(r'const NAT_SUB = (\{.*?\});\n', html)
        nat_sub = build_nat_sub(to_nat(raw), months, data['regions'], json.loads(old.group(1)) if old else {})
        nat_valid = sub_valid(nat_sub, nat)
        print('전국(영남 외) 시도 합계 대비:', json.dumps(nat_valid, ensure_ascii=False))
    if a.dry_run:
        return
    dump = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':'))
    html = re.sub(r'const SUB = \{.*?\};\n', lambda _: f'const SUB = {dump(sub)};\n', html, count=1)
    html = re.sub(r'const SUB_VALID = \{.*?\};\n', lambda _: f'const SUB_VALID = {dump(valid)};\n', html, count=1)
    if 'const SUB_SRC' in html:
        html = re.sub(r'const SUB_SRC = \{.*?\};\n', lambda _: f'const SUB_SRC = {dump(src)};\n', html, count=1)
    else:
        html = html.replace('const SUB_VALID = ', f'// 세움터 시군구 집계로 바꾼 달(종류별 연속 구간). 나머지 달은 건축HUB 원자료 자체 집계\nconst SUB_SRC = {dump(src)};\nconst SUB_VALID = ', 1)
    if a.national:
        html = write_nat(html, nat, nat_sub, nat_valid)
    TREND.write_text(html, encoding='utf-8', newline='')
    print(f'{TREND} 갱신 완료')


if __name__ == '__main__':
    main()
