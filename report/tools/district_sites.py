"""건설 동향 리포트용 — 착공이 크게 늘거나 준 시·군·구와 그 원인 현장 찾기.

  python report/tools/district_sites.py 2026-09                 # 결과를 화면에 출력
  python report/tools/district_sites.py 2026-09 --out 분석.md   # 마크다운 파일로도 저장
  옵션: --min 5   (증감 기준, 만㎡. 기본 5만㎡)
        --workdir <폴더>  (내려받은 원자료를 둘 곳. 기본: 운영체제 임시 폴더 — 저장소에 두지 말 것)

하는 일
1. construction/trend.html의 시·군·구 착공(SUB, 세움터 공식 집계)에서 그 달이
   전월 또는 전년 같은 달보다 --min 이상 늘거나 준 시·군·구를 찾는다.
2. 세움터 「시군구별·용도별 건축착공 현황」(그 달 파일, 로그인 불필요)에서 그 시·군·구의
   용도별 착공 면적을 본다. 아파트 관련 = 공동주택의 아파트 + 부대시설 + 복리시설.
3. 건축HUB 「주택인허가 기본개요」(공개 파일 약 7.5MB, 로그인 불필요)에서 같은 시·군·구의
   공동주택 사업 중 착공예정일·처리일이 그 달 앞뒤인 사업장을 모아, 연면적 합이
   아파트 관련 착공 면적과 맞는(오차 1% 이내) 조합을 찾는다. ㎡ 단위로 맞으면 '확인',
   비슷한 후보만 있으면 '후보'로 표시한다.
4. 사업장을 construction/index.html 착공현황 목록(RAW)과 시·군·구·세대수로 연결한다.

주의
- 건축HUB 주택 원자료는 공동주택(주택법 사업승인)만 있다. 공장·창고 등 다른 용도가 크면
  '아파트 외 용도'로만 알려 준다(건축인허가 원자료 440MB는 받지 않음).
- 결과는 사실 확인용 자료다. 리포트에는 '확인'된 현장만 단지명으로 적고, '후보'는 적지 않는다.
- 표준 라이브러리 + openpyxl(세움터 엑셀 읽기)만 쓴다.
"""
import argparse
import io
import itertools
import json
import re
import sys
import tempfile
import urllib.parse
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'construction' / 'tools'))
import auto_update as au          # noqa: E402  세움터 목록·다운로드
import import_seumter as seum     # noqa: E402  시도 이름표, 시·군·구 이름 정리
import update_trend as ut         # noqa: E402  건축HUB 다운로드

APT_COLS = ('아파트', '부대시설', '복리시설')    # 공동주택 중 아파트 단지에 딸린 용도


def load_const(html, name):
    m = re.search(r'const ' + name + r'\s*=\s*', html)
    return json.JSONDecoder().raw_decode(html[m.end():])[0]


def shift(month, k):
    y, m = map(int, month.split('-'))
    i = y * 12 + m - 1 + k
    return f'{i // 12:04d}-{i % 12 + 1:02d}'


def changes(month, min_area):
    """trend.html SUB에서 크게 변한 시·군·구 [(시도, 시군구, 당월, 전월, 전년동월)]"""
    html = (ROOT / 'construction' / 'trend.html').read_text(encoding='utf-8')
    data, sub = load_const(html, 'DATA'), load_const(html, 'SUB')
    months = data['months']
    if month not in months:
        sys.exit(f'trend.html에 {month} 통계가 아직 없습니다(마지막 {months[-1]}).')
    i, ip = months.index(month), months.index(shift(month, -1))
    iy = months.index(shift(month, -12)) if shift(month, -12) in months else None
    out, totals = [], {}
    for sd, rows in sub.items():
        cur = sum(r[2][i] for r in rows)
        totals[sd] = (cur, sum(r[2][ip] for r in rows), sum(r[2][iy] for r in rows) if iy is not None else None)
        for name, _permit, start in rows:
            a, b, c = start[i], start[ip], start[iy] if iy is not None else None
            if abs(a - b) >= min_area or (c is not None and abs(a - c) >= min_area):
                out.append((sd, name, a, b, c))
    out.sort(key=lambda x: -max(abs(x[2] - x[3]), abs(x[2] - (x[4] or x[2]))))
    return out, totals


def seumter_uses(month, workdir):
    """세움터 그 달 파일 → {(시도, 시군구): {용도: ㎡}} (착공_01·_02 시트, 세부 용도 단위)"""
    monthly, _ = au.eais_list()
    if month not in monthly:
        return None
    f = au.eais_files(monthly[month])[0]
    path = Path(workdir) / f['orignlFileNm']
    if not path.exists():
        path.write_bytes(au.eais_download(f['fileId']))
    sheets = seum.sheets(path.name, path.read_bytes())
    out = {}
    for title, rows in sheets.items():
        if '착공' not in title:
            continue
        head = next(r for r in rows if r and r[0] is None and any(r[3:]))  # 세부 용도 이름 줄
        for r in rows:
            if not r or r[0] not in seum.SIDO or r[1] in ('소계', None, ''):
                continue
            key = (seum.SIDO[r[0]], seum.district(r[1]))
            d = out.setdefault(key, {})
            for col, v in enumerate(r[3:], start=3):
                if isinstance(v, (int, float)) and v and head[col]:
                    d[head[col]] = d.get(head[col], 0) + v
    return out


def housing_records(workdir):
    """건축HUB 주택인허가 기본개요 최신 파일 → 공동주택 사업 목록(중복 기록 정리)"""
    op = ut.hub_opener()
    fid, ref, csrf = ut.find_hub_file(op, '02')          # 최신 파일 기준월(이미 받은 달이면 다시 안 받음)
    path = Path(workdir) / f'housing_basis_{ref}.zip'
    if not path.exists():
        print(f'  건축HUB 주택인허가 기본개요({ref}분) 받는 중 → {path}', file=sys.stderr)
        body = urllib.parse.urlencode({'srvrFileNm': fid, '_csrf': csrf}).encode()
        with op.open(ut.HUB_DOWN, body, timeout=600) as resp, open(path, 'wb') as f:
            while chunk := resp.read(1 << 20):
                f.write(chunk)
    # 필드: [1]대지위치 [2]사업명 [3]시군구코드 [15]동수 [16]연면적 [17]세대수
    #       [23]사업승인일 [24]착공예정일 [25]실제착공일 [26]준공예정일 [28]처리(변경)일
    recs = {}
    for line in ut.open_txt(path):
        p = line.rstrip('\n').split('|')
        if len(p) < 29 or p[3][:2] not in ut.CODE_PREFIX:
            continue
        try:
            area, hh = float(p[16] or 0), int(float(p[17] or 0))
        except ValueError:
            continue
        if hh <= 0 or area <= 0:
            continue
        t = p[1].split()
        key = (p[1].strip(), hh, round(area))
        r = recs.setdefault(key, {'sido': ut.CODE_PREFIX[p[3][:2]], 'sgg': seum.district(t[1]) if len(t) > 1 else '',
                                   'addr': p[1].strip(), 'name': p[2].strip(), 'hh': hh, 'dong': p[15], 'area': area,
                                   'dates': set(), 'plan': '', 'done': ''})
        r['dates'].update(d[:6] for d in (p[24], p[25], p[28]) if d.strip())
        if p[24].strip() > r['plan']:
            r['plan'] = p[24].strip()
        r['done'] = p[26].strip() or r['done']
    return list(recs.values()), path.name


def match(target, cands, tol=0.01):
    """연면적 합이 target과 맞는 조합(작은 조합 우선)"""
    cands = sorted(cands, key=lambda r: -r['area'])[:14]
    best = None
    for n in range(1, min(4, len(cands)) + 1):
        for combo in itertools.combinations(cands, n):
            s = sum(r['area'] for r in combo)
            err = abs(s - target) / target if target else 1
            if err <= tol and (best is None or err < best[1]):
                best = (combo, err)
        if best:
            return best
    return None


def site_list():
    html = (ROOT / 'construction' / 'index.html').read_text(encoding='utf-8')
    rows = []
    for line in html.split('const RAW = [', 1)[1].split('\n];', 1)[0].splitlines():
        line = line.strip().rstrip(',')
        if line.startswith('['):
            rows.append(json.loads(line))
    return rows


def link(rec, raw):
    for r in raw:
        if r[2] == rec['sido'] and r[3] == rec['sgg'] and r[7] == rec['hh']:
            return f"착공현황 No.{r[0]} {r[1]} ({r[4]}, 상태 {r[10]})"
    return '착공현황 목록에 없음'


def man(v):
    return f'{v / 1e4:,.1f}만㎡'


def analyse(month, min_area, workdir):
    lines = [f'# {month} 착공 증감 시·군·구와 현장 (기준 {man(min_area)} 이상 변동)', '']
    found, totals = changes(month, min_area)
    for sd, (a, b, c) in totals.items():
        lines.append(f'- {sd} 착공 {man(a)} (전월 {man(b)}' + (f', 전년 동월 {man(c)})' if c is not None else ')'))
    lines.append('')
    if not found:
        lines.append('크게 변한 시·군·구가 없습니다.')
        return '\n'.join(lines)
    uses = seumter_uses(month, workdir) or {}
    recs, hub_name = housing_records(workdir)
    raw = site_list()
    near = {month.replace('-', ''), shift(month, -1).replace('-', ''), shift(month, 1).replace('-', '')}
    for sd, sgg, a, b, c in found:
        lines.append(f'## {sd} {sgg}: {month} 착공 {man(a)} (전월 {man(b)} → {a - b:+,.0f}㎡'
                     + (f', 전년 동월 {man(c)} → {a - c:+,.0f}㎡)' if c is not None else ')'))
        u = uses.get((sd, sgg), {})
        if not u:
            lines.append('- 세움터 용도별 자료 없음')
        else:
            apt = sum(u.get(k, 0) for k in APT_COLS)
            top = sorted(u.items(), key=lambda x: -x[1])[:5]
            lines.append(f'- 용도: ' + ', '.join(f'{k} {man(v)}' for k, v in top))
            lines.append(f'- 아파트 관련(아파트+부대+복리) {apt:,.0f}㎡ = 당월의 {apt / a * 100:.0f}%' if a else '')
            if a >= min_area and apt / a < 0.5:
                lines.append('- 아파트 외 용도 비중이 큼 — 공장·창고 등은 건축인허가 원자료로 따로 확인 필요')
            if apt >= 10000:
                cands = [r for r in recs if r['sido'] == sd and r['sgg'] == sgg and r['dates'] & near]
                m = match(apt, cands)
                mixed = [r for r in cands if apt < r['area'] <= a]   # 주상복합: 상가 등 다른 용도가 같이 잡힘
                if not m and mixed:
                    lines.append('- 아파트 관련 면적과 딱 맞는 사업장은 없고, 주상복합(상가 등 포함)일 수 있는 **후보**:')
                    for r in sorted(mixed, key=lambda r: -r['area'])[:3]:
                        lines.append(f"  - {r['addr']} 「{r['name'] or '사업명 없음'}」 {r['hh']:,}세대, 연면적 {r['area']:,.0f}㎡"
                                     f" (당월 착공 {a:,.0f}㎡ 이내), 착공예정 {r['plan'] or '-'} → {link(r, raw)}")
                elif m:
                    combo, err = m
                    lines.append(f'- **확인**(연면적 합 오차 {err * 100:.2f}%):')
                    for r in combo:
                        lines.append(f"  - {r['addr']} 「{r['name'] or '사업명 없음'}」 {r['hh']:,}세대·{r['dong']}개동, "
                                     f"연면적 {r['area']:,.0f}㎡, 착공예정 {r['plan'] or '-'}, 준공예정 {r['done'] or '-'} → {link(r, raw)}")
                else:
                    lines.append('- 면적이 맞는 조합 없음. 후보(그 달 앞뒤 기록, 큰 순):')
                    for r in sorted(cands, key=lambda r: -r['area'])[:5]:
                        lines.append(f"  - {r['addr']} 「{r['name'] or '사업명 없음'}」 {r['hh']:,}세대, {r['area']:,.0f}㎡ → {link(r, raw)}")
        if c is not None and c - a >= min_area:
            ly = shift(month, -12).replace('-', '')
            prev = sorted([r for r in recs if r['sido'] == sd and r['sgg'] == sgg and ly in r['dates']], key=lambda r: -r['area'])[:3]
            if prev:
                lines.append(f'- 전년 동월({shift(month, -12)}) 기록이 있는 큰 사업장(감소 이유 후보):')
                for r in prev:
                    lines.append(f"  - {r['addr']} 「{r['name'] or '사업명 없음'}」 {r['hh']:,}세대, {r['area']:,.0f}㎡")
        lines.append('')
    lines.append(f'자료: 국토교통부 세움터 시군구별·용도별 건축착공 현황({month}), 건축HUB {hub_name}')
    return '\n'.join(lines)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('month', help='통계 월 YYYY-MM')
    ap.add_argument('--min', type=float, default=5, help='증감 기준(만㎡)')
    ap.add_argument('--workdir', default=str(Path(tempfile.gettempdir()) / 'yn_district_sites'))
    ap.add_argument('--out')
    a = ap.parse_args()
    if not re.fullmatch(r'\d{4}-\d{2}', a.month):
        sys.exit('월은 YYYY-MM 형식으로 주세요.')
    Path(a.workdir).mkdir(parents=True, exist_ok=True)
    text = analyse(a.month, a.min * 1e4, a.workdir)
    print(text)
    if a.out:
        Path(a.out).write_text(text + '\n', encoding='utf-8')
