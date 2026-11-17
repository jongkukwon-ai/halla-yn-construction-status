"""아파트 착공현황(construction/index.html RAW)의 착공 월을 정해진 순서로 채운다 — 2026-11-17 사용자 지시.

  1순위 건축HUB : 국토부 건축HUB 「주택인허가 기본개요」(실제착공일, 없으면 착공(예정)일) → 없으면 「건축인허가 기본개요」 신축(실제착공일)
                  건축HUB에 나오면 그 날짜를 그대로 씀(세움터와 대조하지 않음). 착공면적 = 건축HUB 연면적.
  2순위 세움터  : 건축HUB에 착공일이 없고, 착공이 「미확인」·「(추정)」인 현장만 — 분양(입주자모집) 무렵 시·군·구 착공 면적이
                  이 현장 연면적 이상인 달이 딱 한 번이면 「YYYY.MM(추정)」
  3순위 매뉴얼  : 위 둘 다 없으면 사람이 넣은 값을 그대로 둠

현장 ↔ 건축HUB 사업장 짝은 start_keys.json에 저장(처음엔 주소·세대수로 자동으로 찾고, 틀린 짝은 "hub": false 로 막음).
결과 근거는 construction/index.html 의 `const START_SRC = {...};` 한 줄에 기록 → 화면 착공 칸 옆 HUB/세움터/수동 표시.

  python construction/tools/start_dates.py --housing-zip 주택.zip --permit-zip 건축.zip [--dry-run] [--report 보고.md]
  python construction/tools/start_dates.py --auto      # GitHub Actions: 건축HUB·세움터에 새 달이 나왔을 때만 받아서 실행
원자료(zip)는 저장소에 넣지 않는다(실행 폴더의 임시 폴더 사용).
"""
import argparse
import io
import json
import re
import sys
import tempfile
import zipfile
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PAGE = ROOT / 'construction' / 'index.html'
TREND = ROOT / 'construction' / 'trend.html'
KEYS = HERE / 'start_keys.json'
REGIONS = ROOT / 'weather' / 'data' / 'regions.json'
KST = timezone(timedelta(hours=9))
SIDO = {'부산': '부산광역시', '울산': '울산광역시', '대구': '대구광역시', '경남': '경상남도', '경북': '경상북도'}
ROW = re.compile(r'^(\s*)\[(\d+),"([^"]*)","([^"]*)","([^"]*)","([^"]*)","([^"]*)","([^"]*)",(\w+|null),(\w+|null),'
                 r'"([^"]*)","([^"]*)","([^"]*)","(.*)",(true|false)\](,?)\s*$')
ADDR = re.compile(r'([가-힣]+(?:동|리|가)(?:\d+가)?)\s*((?:산)?\d+(?:-\d+)?)(?=번지|\s|,|\.|\)|$| 외| 일원)')
TOKENS_SKIP = {'아파트', '공동주택', '신축공사', '주상복합', '단지', '신축', '공사', '사업', '정비사업', '재개발', '재건축'}


def today():
    return datetime.now(KST).strftime('%Y%m%d')


def d8(s):
    return f'{s[:4]}-{s[4:6]}-{s[6:8]}'


def lines(zip_path):
    z = zipfile.ZipFile(zip_path)
    name = next(n for n in z.namelist() if not n.endswith('/'))
    raw = z.open(name)
    head = raw.read(65536); raw.close()
    enc = 'utf-8'
    try:
        head.decode('utf-8')
    except UnicodeDecodeError as e:
        if e.reason != 'unexpected end of data':   # 끝에서 글자가 잘린 것뿐이면 UTF-8
            enc = 'cp949'
    return io.TextIOWrapper(z.open(name), encoding=enc, errors='ignore')


def code_map():
    d = json.loads(REGIONS.read_text(encoding='utf-8'))
    m = {}
    for code, sido, si, gu, *_ in d['regions']:
        if si:
            m[(sido, f'{si} {gu}'.strip())] = code[:5]
            m.setdefault((sido, si), code[:5])
    return m


def sgg_code(cmap, sido, sgg):
    sd = SIDO.get(sido, sido)
    for k in (sgg, sgg.replace('창원 ', '창원시 '), sgg.replace(' ', '')):
        if (sd, k) in cmap:
            return cmap[(sd, k)]
    return next((v for (a, b), v in cmap.items() if a == sd and b.replace(' ', '') == sgg.replace('창원', '창원시').replace(' ', '')), None)


def load_rows():
    html = PAGE.read_text(encoding='utf-8')
    rows = {}
    for line in html.split('\n'):
        m = ROW.match(line)
        if m:
            rows[int(m.group(2))] = m
    return html, rows


# ── 건축HUB 읽기 ───────────────────────────────────────────────
def read_housing(path, codes):
    """주택인허가 기본개요(29필드): [1]대지위치 [2]사업명 [3]시군구 [16]연면적 [17]세대수 [23]사업승인일 [24]착공예정일 [25]실제착공일 [26]준공예정일 [28]처리일"""
    out = defaultdict(list)
    for line in lines(path):
        f = line.rstrip('\n').split('|')
        if len(f) > 28 and f[3] in codes and f[17].strip() not in ('', '0'):
            out[f[3]].append(f)
    return out


def read_permit(path, codes):
    """건축인허가 기본개요(41필드) 신축 공동주택: [1]대지위치 [2]건물명 [3]시군구 [20]건축구분 [24]연면적 [37]실제착공일 [38]허가일, 세대수는 '공동주택' 다음 칸"""
    out = defaultdict(list)
    for line in lines(path):
        if '공동주택' not in line:
            continue
        p = line.rstrip('\n').split('|')
        if len(p) < 39 or p[3] not in codes or p[20].strip() != '신축':
            continue
        try:
            i = p.index('공동주택', 25)
            hh = int(p[i + 1])
        except (ValueError, IndexError):
            continue
        if hh >= 30:
            out[p[3]].append(p + [str(hh)])           # 맨 끝에 세대수 덧붙임
    return out


def name_tokens(s):
    return {t for t in re.split(r'[\s()·,\-]+', s) if len(t) >= 2 and t not in TOKENS_SKIP}


def bunji_hit(addr_text, dong, bun):
    a = addr_text.replace(' ', '')
    return dong in a and re.search(r'(?<![\d-])' + re.escape(bun) + r'번지', a) is not None


def auto_match(m, code, housing, permit):
    """주소(비고의 동·번지)·세대수·이름으로 건축HUB 사업장을 찾음 → (종류, 레코드, 점수) 또는 None"""
    name, hh, note = m.group(3), m.group(9), m.group(14)
    hh = int(hh) if hh not in ('null', '') else None
    addrs = ADDR.findall(note) + ADDR.findall(name)
    toks = name_tokens(name)
    best = None
    for f in housing.get(code, []):
        try:
            fh = int(float(f[17]))
        except ValueError:
            continue
        exact = any(bunji_hit(f[1], d, b) for d, b in addrs)
        near = hh and fh and 0.45 <= hh / fh <= 2.2
        same = hh is not None and fh == hh
        recent = (f[23] or '0')[:4] >= '2015' or (f[24] or '0')[:4] >= '2019'
        tokhit = bool(toks & name_tokens(f[2]))
        if exact and (same or near) and recent:
            score = 10 + same * 3 + tokhit
        elif same and recent and (tokhit or not addrs):
            score = 6 + tokhit
        else:
            continue
        cand = ('주택인허가', f, score)
        if not best or (score, f[28]) > (best[2], best[1][28]):
            best = cand
    if best and best[2] >= 10:
        return best
    for p in permit.get(code, []):
        ph = int(p[-1])
        exact = any(bunji_hit(p[1], d, b) for d, b in addrs)
        if exact and hh and 0.45 <= hh / ph <= 2.2 and (p[38] or '0')[:4] >= '2018':
            cand = ('건축인허가', p, 9 + (ph == hh) * 3)
            if not best or cand[2] > best[2]:
                best = cand
    if best and best[2] >= 9:
        return best
    if best and best[0] == '주택인허가' and best[2] >= 6:
        # 주소가 없고 세대수만 같은 경우: 그 시·군·구에서 같은 세대수 최근 사업이 하나뿐일 때만
        same = [f for f in housing.get(code, []) if f[17].split('.')[0] == str(hh) and ((f[23] or '0')[:4] >= '2015')]
        if len({(f[1], f[2]) for f in same}) == 1:
            return best
    return None


def by_key(key, code, housing, permit):
    kind = key.get('hub')
    pool = housing.get(code, []) if kind == '주택인허가' else permit.get(code, [])
    hits = [f for f in pool if key['addr'] in f[1] and (not key.get('biz') or key['biz'] in f[2])
            and (not key.get('hh') or (f[17] if kind == '주택인허가' else f[-1]).split('.')[0] == str(key['hh']))]
    if not hits:
        return None
    hits.sort(key=lambda f: f[28] if kind == '주택인허가' else (f[38] or ''), reverse=True)
    return hits[0]


# ── 세움터(2순위) ──────────────────────────────────────────────
def load_sub():
    html = TREND.read_text(encoding='utf-8')
    data = json.loads(re.search(r'const DATA =(\{.*?\});\n', html).group(1))
    sub = json.loads(re.search(r'const SUB = (\{.*?\});\n', html).group(1))
    return data['months'], sub


def sale_month(m):
    for pat in (r'입주자모집공고 (\d{4})-(\d{2})', r'\((\d{4})\.(\d{2})', r'(\d{4})\.(\d{1,2}) 청약', r'(\d{4})\.(\d{1,2})\.\d{1,2}~?\S* (?:청약|계약)'):
        t = re.search(pat, m.group(13) + ' ' + m.group(14))
        if t:
            return f'{t.group(1)}-{int(t.group(2)):02d}'
    return None


def seumter_guess(m, months, sub):
    sido, sgg, area = m.group(4), m.group(5), m.group(10)
    hh = m.group(9)
    est = int(area) if area not in ('null', '') else (int(hh) * 140 if hh not in ('null', '') else None)
    ann = sale_month(m)
    if not est or not ann or sido not in sub:
        return None
    key = '창원시' if sgg.startswith('창원') else sgg
    row = next((r for r in sub[sido] if r[0] == key), None)
    if not row:
        return None
    y, mo = int(ann[:4]), int(ann[5:])
    lo = f'{y - 1}-{mo:02d}'
    hits = [(mm, row[2][i]) for i, mm in enumerate(months) if lo <= mm <= ann and row[2][i] >= 0.95 * est]
    if len(hits) != 1:
        return None
    mm, v = hits[0]
    return mm, v, est, ann, key


# ── 실행 ──────────────────────────────────────────────────────
def run(housing_zip, permit_zip, dry=False, report=None, refs=None):
    html, rows = load_rows()
    cmap = code_map()
    codes = {sgg_code(cmap, m.group(4), m.group(5)) for m in rows.values()} - {None}
    housing = read_housing(housing_zip, codes)
    permit = read_permit(permit_zip, codes)
    months, sub = load_sub()
    keys = json.loads(KEYS.read_text(encoding='utf-8')) if KEYS.exists() else {}
    now = today()
    src, changes, newkeys = {}, [], {}
    lines_out = html.split('\n')
    index = {int(ROW.match(l).group(2)): i for i, l in enumerate(lines_out) if ROW.match(l)}
    for no, m in sorted(rows.items()):
        g = list(m.groups())                 # 0 들여쓰기 1 No 2 단지명 3 광역 4 시군구 5 건설사 6 착공 7 준공 8 세대 9 착공면적 10 유형 11 상태 12 분양 13 비고 14 isNew 15 쉼표
        code = sgg_code(cmap, g[3], g[4])
        key = keys.get(str(no))
        rec = kind = None
        if key and key.get('hub') is False:
            pass                             # 건축HUB 짝을 쓰지 않음(틀린 짝 막기)
        elif key:
            rec = by_key(key, code, housing, permit); kind = key['hub']
        else:
            hit = auto_match(m, code, housing, permit)
            if hit:
                kind, rec, score = hit
                addr = re.search(r'([가-힣]+(?:동|리|가|읍|면)(?:\d+가)?\s*(?:산)?[\d-]*번지|[가-힣]+(?:동|리|가|읍|면)\s+블록)', rec[1])
                newkeys[str(no)] = {'hub': kind, 'addr': (addr.group(1) if addr else rec[1].split(' ', 2)[-1]),
                                    'biz': rec[2][:30] if rec[2] else '', 'hh': int(float(rec[17] if kind == '주택인허가' else rec[-1])), 'auto': score}
        old = (g[6], g[7], g[9], g[11])
        if rec is not None:
            if kind == '주택인허가':
                dt, label = (rec[25], '실제착공일') if rec[25].strip() else (rec[24], '착공(예정)일')
                area, done = round(float(rec[16] or 0)), rec[26]
            else:
                dt, label, area, done = rec[37], '실제착공일', round(float(rec[24] or 0)), ''
            dt = dt.strip()
            if len(dt) >= 8 and dt[:2] in ('19', '20'):
                future = dt[:8] > now
                g[6] = f'{dt[:4]}.{dt[4:6]}' + ('(예정)' if future else '')
                if area:
                    g[9] = str(area)
                if not future and g[11] == '착공임박':
                    g[11] = '공사중'
                if future and g[11] == '공사중':
                    g[11] = '착공임박'
                if '미확인' in g[7] and len(done) >= 6 and done[:8] > now:
                    g[7] = f'{done[:4]}.{done[4:6]}'
                src[str(no)] = ['HUB', f'건축HUB {kind} {label} {d8(dt)}' + (f' · 연면적 {area:,}㎡' if area else '')]
            else:
                src[str(no)] = ['수동', f'건축HUB {kind}에 사업은 있으나 착공일이 아직 없음']
        if str(no) not in src or src[str(no)][0] == '수동':
            if ('미확인' in g[6] or '(추정)' in g[6]):
                guess = seumter_guess(m, months, sub)
                if guess:
                    mm, v, est, ann, kname = guess
                    g[6] = f'{mm.replace("-", ".")}(추정)'
                    src[str(no)] = ["세움터", f"세움터 {mm.replace('-', '.')} {g[3]} {kname} 착공 {v / 1e4:.1f}만㎡ ≥ 이 현장 연면적 약 {est / 1e4:.1f}만㎡ — 분양({ann}) 전 1년 중 유일"]
        if str(no) not in src:
            src[str(no)] = ['수동', '건축HUB·세움터로 정하지 못해 직접 입력한 값']
        if (g[6], g[7], g[9], g[11]) != old:
            changes.append((no, g[2], old, (g[6], g[7], g[9], g[11]), src[str(no)][0]))
            lines_out[index[no]] = (f'{g[0]}[{no},"{g[2]}","{g[3]}","{g[4]}","{g[5]}","{g[6]}","{g[7]}",{g[8]},{g[9]},"{g[10]}","{g[11]}","{g[12]}","{g[13]}",{g[14]}]{g[15]}')
    meta = {'갱신': f'{now[:4]}-{now[4:6]}-{now[6:]}', **(refs or {}), '세움터': months[-1]}
    blob = 'const START_SRC = ' + json.dumps({'기준': meta, 'r': src}, ensure_ascii=False, separators=(',', ':')) + ';'
    out = '\n'.join(lines_out)
    if 'const START_SRC = ' in out:
        out = re.sub(r'const START_SRC = \{.*?\};', lambda _: blob, out, count=1)
    else:
        out = out.replace('\n];\n', '\n];\n// 착공 월 근거(construction/tools/start_dates.py가 자동 기록): HUB=건축HUB · 세움터=세움터 착공 면적 추정 · 수동=직접 입력\n' + blob + '\n', 1)
    from collections import Counter
    cnt = Counter(v[0] for v in src.values())
    msg = [f'착공 근거: 건축HUB {cnt["HUB"]} · 세움터 {cnt["세움터"]} · 수동 {cnt["수동"]} / 바뀐 현장 {len(changes)}곳 / 새로 찾은 건축HUB 짝 {len(newkeys)}곳']
    for no, nm, a, b, s in changes:
        msg.append(f'- No.{no} {nm}: 착공 {a[0]}→{b[0]}, 준공 {a[1]}→{b[1]}, 면적 {a[2]}→{b[2]}, 상태 {a[3]}→{b[3]} [{s}] {src[str(no)][1]}')
    for no, k in newkeys.items():
        msg.append(f'  새 짝 No.{no}: {k}')
    print('\n'.join(msg[:1]))
    if report:
        Path(report).write_text('\n'.join(msg) + '\n', encoding='utf-8')
    if not dry:
        PAGE.write_text(out, encoding='utf-8', newline='')
        if newkeys:
            keys.update(newkeys)
            KEYS.write_text(json.dumps(dict(sorted(keys.items(), key=lambda kv: int(kv[0]))), ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    return changes, newkeys


def auto(force=False):
    """새 달이 나왔을 때만: 건축HUB 기본개요 기준월 또는 세움터 마지막 달이 START_SRC 기준과 다르면 받아서 실행"""
    sys.path.insert(0, str(HERE))
    import update_trend as ut
    html = PAGE.read_text(encoding='utf-8')
    m = re.search(r'const START_SRC = (\{.*?\});', html)
    meta = json.loads(m.group(1))['기준'] if m else {}
    op = ut.hub_opener()
    fid_p, ref_p, _ = ut.find_hub_file(op, '01')
    fid_h, ref_h, _ = ut.find_hub_file(op, '02')
    months, _ = load_sub()
    if not force and meta.get('건축인허가') == ref_p and meta.get('주택인허가') == ref_h and meta.get('세움터') == months[-1]:
        print(f'새 자료 없음(건축HUB {ref_h}·{ref_p}, 세움터 {months[-1]})')
        return
    tmp = Path(tempfile.mkdtemp(prefix='hub_'))
    permit_zip, housing_zip = ut.download_hub(tmp)
    run(housing_zip, permit_zip, refs={'주택인허가': ref_h, '건축인허가': ref_p})


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--housing-zip')
    ap.add_argument('--permit-zip')
    ap.add_argument('--ref', default='', help='건축HUB 기준월(YYYY-MM)')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--report')
    ap.add_argument('--auto', action='store_true')
    ap.add_argument('--force', action='store_true', help='--auto 에서 새 자료가 없어도 실행')
    a = ap.parse_args()
    if a.auto:
        auto(a.force)
    elif a.housing_zip and a.permit_zip:
        run(a.housing_zip, a.permit_zip, a.dry_run, a.report, {'주택인허가': a.ref, '건축인허가': a.ref} if a.ref else None)
    else:
        sys.exit(__doc__)
