"""영업소 권역 날씨(weather-data.js) 갱신 — GitHub Actions(weather.yml)에서 매시간 실행(예보 내용이 바뀔 때만 커밋).

기상청 단기예보(공공데이터포털 「기상청_단기예보 ((구)_동네예보) 조회서비스」 getVilageFcst)에서
영업소별 대표 도시의 오늘~글피(최대 4일) 최저·최고기온, 하늘상태, 비·눈(강수형태), 강수확률을 하루 단위로 요약한다.

전국 날씨 화면(weather/index.html)용 자료도 함께 만든다(weather/data/, 지역 목록 regions.json 기준 — 격자 약 230곳):
  fc/{시도코드}.json             시간대별 예보(단기예보 새 발표가 나올 때만, 하루 8번 × 격자 수)
  obs/{YYYY-MM}/{시도코드}.json  매시간 관측(초단기실황 getUltraSrtNcst) — 3시간마다 지난 22시간 빈 칸 채움(하루 약 24 × 격자 수)
  daily/{지점번호}.json          지난 날씨 일자료(「기상청_지상(종관, ASOS) 일자료 조회서비스」, 2021-01-01부터 어제까지,
                                 2026-11-17 사용자 활용신청 완료). 실패해도 경고만 남기고 화면 예보 갱신은 계속.
  공공데이터포털 하루 호출 한도(기능별 1만 건) 안: 예보 약 1,840 · 관측 약 5,520 · ASOS 약 90건/일.

  python .github/scripts/update_weather.py
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'weather-data.js'
KST = timezone(timedelta(hours=9))
API = 'https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
NCST_API = 'https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
ASOS_API = 'https://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList'
DATA_DIR = ROOT / 'weather' / 'data'
# 영업소 → 대표 도시의 기상청 종관기상관측(ASOS) 지점 번호
ASOS_START = '2021-01-01'
OBS_EVERY_HOURS = 3     # 관측(실황)은 이 시간마다 한 번에 받음(지난 24시간까지 받을 수 있어 빠짐 없음, 커밋 수 줄이기)
# 영업소 → 대표 도시와 기상청 격자(nx, ny) — 시청 위치 기준(기상청 격자 변환식)
REGIONS = [('부산', '부산', 98, 76), ('울산', '울산', 102, 84), ('경남동부', '창원', 91, 77),
           ('경남서부', '진주', 81, 75), ('경북동부', '포항', 102, 94), ('경북서부', '대구', 89, 90)]   # 경북서부는 대구 날씨(사용자 지정)
BASE_TIMES = ['0200', '0500', '0800', '1100', '1400', '1700', '2000', '2300']   # 발표 시각(약 10분 뒤 제공)
DAYS = '월화수목금토일'
STALE_HOURS = 9     # 못 받았을 때 화면 예보가 발표된 지 이보다 오래면 실패로 알림(그 전엔 경고만)


def service_key():
    k = os.environ.get('DATA_GO_KR_KEY', '').strip()
    return urllib.parse.unquote(k) if '%' in k else k      # Encoding 키를 넣어도 한 번만 인코딩되게


def latest_base(now):
    """지금 받을 수 있는 가장 최근 발표(발표 15분 뒤부터 사용)"""
    t = now - timedelta(minutes=15)
    cands = [b for b in BASE_TIMES if t.strftime('%H%M') >= b]
    if cands:
        return t.strftime('%Y%m%d'), cands[-1]
    return (t - timedelta(days=1)).strftime('%Y%m%d'), '2300'


class NoData(RuntimeError):
    """해당 발표 자료가 아직 없음(기상청 resultCode 03)"""


def fetch(key, nx, ny, base_date, base_time, api=API, rows=1500, tries=4):
    return call(api, {'serviceKey': key, 'pageNo': 1, 'numOfRows': rows, 'dataType': 'JSON',
                      'base_date': base_date, 'base_time': base_time, 'nx': nx, 'ny': ny}, tries)


def call(api, params, tries=4):
    """기상청 공공데이터 API 호출 → item 목록"""
    q = urllib.parse.urlencode(params)
    last = None
    for k in range(tries):                      # GitHub 서버(해외)에서 기상청 응답이 가끔 끊겨 넉넉히 재시도
        try:
            raw = urllib.request.urlopen(f'{api}?{q}', timeout=20).read()
            d = json.loads(raw)
            hdr = d['response']['header']
            if hdr.get('resultCode') == '03':
                raise NoData(f'{base_date} {base_time} 발표 자료 없음')
            if hdr.get('resultCode') != '00':
                raise RuntimeError(f"기상청 응답 {hdr.get('resultCode')} {hdr.get('resultMsg')}")
            items = d['response']['body'].get('items') or {}
            return items.get('item', []) if isinstance(items, dict) else []
        except NoData:
            raise
        except (urllib.error.URLError, OSError, ValueError, KeyError, RuntimeError) as e:
            # 오류 문구에 인증키가 섞이지 않게 원인만 남김(실행 기록이 공개됨)
            if isinstance(e, urllib.error.HTTPError):
                last = f'HTTP {e.code}'
            elif isinstance(e, urllib.error.URLError):
                last = f'{type(e.reason).__name__}: {e.reason}'
            elif isinstance(e, OSError):
                last = f'{type(e).__name__}: {e}'
            else:
                last = e
            if isinstance(e, ValueError):
                last = '응답이 JSON이 아님(인증키 미등록·활용신청 전일 수 있음)'
            if k + 1 < tries:
                time.sleep(4 * (k + 1))
    raise RuntimeError(f'기상청 자료를 받지 못함: {last}')


def prev_base(base_date, base_time):
    """바로 앞 발표 시각(최신 발표가 아직 안 올라왔을 때 대신 사용)"""
    i = BASE_TIMES.index(base_time)
    if i:
        return base_date, BASE_TIMES[i - 1]
    d = datetime.strptime(base_date, '%Y%m%d') - timedelta(days=1)
    return d.strftime('%Y%m%d'), BASE_TIMES[-1]


def previous_regions(today):
    """지난번 weather-data.js의 권역 자료(오늘 날짜로 시작하는 것만) — 한 권역만 실패했을 때 그 권역은 직전 예보 유지"""
    try:
        t = OUT.read_text(encoding='utf-8')
        d = json.loads(t[t.index('{'):t.rindex('}') + 1])
        return {r['office']: r for r in d.get('regions', [])
                if r.get('days') and r['days'][0].get('date') == today.isoformat()}
    except (OSError, ValueError, KeyError, TypeError):
        return {}


def summarize(items, today):
    """시간별 예보 → 날짜별 {tmin, tmax, pop, sky, pty, icon}"""
    by = defaultdict(dict)                      # (날짜, 시각) → {분류: 값}
    for it in items:
        by[(it['fcstDate'], it['fcstTime'])][it['category']] = it['fcstValue']
    days = []
    for i in range(4):
        d = (today + timedelta(days=i)).strftime('%Y%m%d')
        hours = {t: v for (dd, t), v in by.items() if dd == d}
        if not hours:
            continue
        num = lambda v: float(v) if v not in (None, '', '-') else None
        tmps = [num(v.get('TMP')) for v in hours.values() if num(v.get('TMP')) is not None]
        tmn = next((num(v['TMN']) for v in hours.values() if 'TMN' in v), None)
        tmx = next((num(v['TMX']) for v in hours.values() if 'TMX' in v), None)
        tmin = tmn if tmn is not None else (min(tmps) if tmps else None)
        tmax = tmx if tmx is not None else (max(tmps) if tmps else None)
        pops = [int(num(v['POP'])) for v in hours.values() if num(v.get('POP')) is not None]
        ptys = {v.get('PTY') for v in hours.values()}
        if '3' in ptys:
            pty, icon = '눈', '❄️'
        elif '2' in ptys:
            pty, icon = '비/눈', '🌨️'
        elif '1' in ptys:
            pty, icon = '비', '🌧️'
        elif '4' in ptys:
            pty, icon = '소나기', '🌦️'
        else:
            pty = ''
            day_sky = [v.get('SKY') for t, v in hours.items() if '0600' <= t <= '1800' and v.get('SKY')] \
                or [v.get('SKY') for v in hours.values() if v.get('SKY')]
            s = Counter(day_sky).most_common(1)[0][0] if day_sky else '1'
            pty, icon = {'1': ('맑음', '☀️'), '3': ('구름많음', '⛅'), '4': ('흐림', '☁️')}.get(s, ('맑음', '☀️'))
        dt = today + timedelta(days=i)
        days.append({'date': dt.isoformat(), 'label': ['오늘', '내일', '모레', '글피'][i],
                     'dow': DAYS[dt.weekday()], 'tmin': None if tmin is None else round(tmin),
                     'tmax': None if tmax is None else round(tmax), 'pop': max(pops) if pops else None,
                     'wx': pty, 'icon': icon})
    return days


def main():
    key = service_key()
    if not key:
        print('DATA_GO_KR_KEY가 없어 날씨를 갱신하지 않음')
        return
    now = datetime.now(KST)
    today = now.date()
    base_date, base_time = latest_base(now)
    first = (today.strftime('%Y%m%d'), '0200') if now.strftime('%H%M') >= '0215' else None   # 오늘 0시~ 자료·최저기온용
    prev = previous_regions(today)
    out, failed, streak = [], [], 0
    for name, city, nx, ny in REGIONS:
        try:
            try:
                items = fetch(key, nx, ny, base_date, base_time)
            except NoData:                      # 최신 발표가 아직 안 올라옴 → 바로 앞 발표로
                base_date, base_time = prev_base(base_date, base_time)
                items = fetch(key, nx, ny, base_date, base_time)
            if first and first != (base_date, base_time):
                try:                            # 오늘 새벽 자료는 최저기온 보강용 — 못 받아도 진행
                    early = fetch(key, nx, ny, *first)
                    seen = {(i['fcstDate'], i['fcstTime'], i['category']) for i in items}
                    items = items + [i for i in early if (i['fcstDate'], i['fcstTime'], i['category']) not in seen]
                except RuntimeError as e:
                    print(f'{name}: 새벽 자료 생략 ({e})')
            days = summarize(items, today)
            if not days:
                raise RuntimeError('예보 자료가 비어 있음')
            out.append({'office': name, 'city': city, 'days': days})
            streak = 0
        except RuntimeError as e:
            print(f'::warning::{name}: {e}')       # GitHub 주석(로그인 없이 확인 가능)으로 원인 남김
            if name not in prev:
                raise SystemExit(f'{name}: 예보를 받지 못했고 오늘 자 직전 자료도 없어 갱신하지 않음')
            out.append(prev[name])              # 이 권역만 직전 예보 유지
            failed.append(name)
            streak += 1
            if streak >= 2 and len(failed) == len(out):
                raise SystemExit('기상청 응답이 계속 끊겨 이번 회차는 갱신하지 않음(다음 회차에 재시도)')
        time.sleep(0.5)
    if len(failed) == len(REGIONS):
        raise SystemExit('모든 권역 실패 — 갱신하지 않음')
    data = {'updated': now.strftime('%Y-%m-%d %H:%M'),
            'base': f'{base_date[4:6]}/{base_date[6:]} {base_time[:2]}:{base_time[2:]}',
            'source': '기상청 단기예보', 'regions': out}
    OUT.write_text('// 영업소 권역 날씨 — .github/scripts/update_weather.py가 매시간 자동 갱신 (기상청 단기예보)\n'
                   'const WEATHER = ' + json.dumps(data, ensure_ascii=False, indent=1) + ';\n', encoding='utf-8', newline='\n')
    print(f'날씨 갱신: {data["base"]} 발표, {len(out)}개 권역 × {len(out[0]["days"])}일'
          + (f' (직전 예보 유지: {", ".join(failed)})' if failed else ''))


# ── 전국 날씨 화면(weather/index.html)용 자료 ───────────────────────────────────────
# 지역 목록 weather/data/regions.json(weather/tools/build_regions.py가 기상청 격자표로 만듦) — 시·도/시·군·구/구마다 예보 격자·가까운 ASOS 지점
#   fc/{시도코드}.json            시간대별 예보(격자별) — 단기예보 새 발표가 나올 때만 받음(하루 8번)
#   obs/{YYYY-MM}/{시도코드}.json 매시간 관측(초단기실황, 격자별) — 3시간마다 지난 22시간 빈 칸을 채움
#   daily/{지점번호}.json         지난 날씨 일자료(ASOS) — 2021-01-01부터 어제까지
HOURLY_FIELDS = ['시각', '기온', '하늘', '강수형태', '강수확률', '강수량', '습도', '풍속', '적설']
DAY_FIELDS = ['날짜', '최저기온', '최고기온', '강수확률', '날씨', '아이콘']
OBS_FIELDS = ['기온', '1시간강수량', '습도', '풍속', '강수형태', '풍향']
DAILY_FIELDS = ['평균기온', '최저기온', '최고기온', '강수량', '평균습도', '평균풍속', '최심적설']
WORKERS = 6             # 기상청 동시 요청 수(너무 많으면 끊김)


def num(v):
    try:
        return None if v in (None, '', '-') else round(float(v), 1)
    except (TypeError, ValueError):
        return None


def load_json(path):
    try:
        return json.loads(Path(path).read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return {}


def dump(v):
    return json.dumps(v, ensure_ascii=False, separators=(',', ':'))


def write_json(path, meta, key, body):
    """meta + {key: {이름: 값}} — 한 줄에 한 항목(바뀐 줄만 git에 보이게). 값이 dict면 그 안도 한 줄에 하나."""
    path.parent.mkdir(parents=True, exist_ok=True)
    parts = []
    for k in sorted(body):
        v = body[k]
        if isinstance(v, dict):
            inner = ',\n'.join(f'   {dump(kk)}: {dump(v[kk])}' for kk in sorted(v))
            parts.append(f'  {dump(k)}: {{\n{inner}\n  }}')
        else:
            parts.append(f'  {dump(k)}: {dump(v)}')
    head = ''.join(f' {dump(k)}: {dump(v)},\n' for k, v in meta.items())
    path.write_text('{\n' + head + f' {dump(key)}: {{\n' + ',\n'.join(parts) + '\n }\n}\n', encoding='utf-8', newline='\n')


def nation():
    """regions.json → (격자 목록 {'nx,ny': (nx, ny)}, 시도코드별 격자 집합, ASOS 지점 {번호: 이름})"""
    d = load_json(DATA_DIR / 'regions.json')
    grids, by_sido = {}, defaultdict(set)
    for code, sido, si, gu, nx, ny, *_ in d.get('regions', []):
        g = f'{nx},{ny}'
        grids[g] = (nx, ny)
        by_sido[code[:2]].add(g)
    stns = {r[8] for r in d.get('regions', [])}
    return grids, by_sido, {s: d.get('stations', {}).get(str(s), str(s)) for s in stns}


def parallel(fn, jobs):
    """jobs를 WORKERS개씩 동시에 → [(job, 결과 또는 예외)]"""
    from concurrent.futures import ThreadPoolExecutor
    def run(j):
        try:
            return j, fn(j)
        except Exception as e:          # noqa: BLE001 — 한 건 실패는 그 건만 건너뜀
            return j, e
    with ThreadPoolExecutor(WORKERS) as ex:
        return list(ex.map(run, jobs))


def hourly_rows(items, now):
    """단기예보 응답 → 지금 시각부터 [YYYYMMDDHH, 기온, 하늘, 강수형태, 강수확률, 강수량, 습도, 풍속, 적설]"""
    by = defaultdict(dict)
    for it in items:
        by[it['fcstDate'] + it['fcstTime'][:2]][it['category']] = it['fcstValue']
    start = now.strftime('%Y%m%d%H')
    text = lambda v, none: '' if v in (None, '', none) else v
    rows = []
    for k in sorted(by):
        v = by[k]
        if k < start or 'TMP' not in v:
            continue
        rows.append([k, num(v.get('TMP')), int(v.get('SKY') or 0), int(v.get('PTY') or 0), int(num(v.get('POP')) or 0),
                     text(v.get('PCP'), '강수없음'), int(num(v.get('REH')) or 0), num(v.get('WSD')), text(v.get('SNO'), '적설없음')])
    return rows


def update_forecast(key, now):
    """전국 시간대별 예보(새 발표가 나왔을 때만)"""
    grids, by_sido, _ = nation()
    if not grids:
        print('지역 목록(regions.json)이 없어 전국 예보를 건너뜀')
        return
    base = latest_base(now)
    files = {sd: load_json(DATA_DIR / 'fc' / f'{sd}.json').get('grids', {}) for sd in by_sido}
    old = {g: v for f in files.values() for g, v in f.items()}
    tag = lambda b: f'{b[0]}{b[1]}'
    todo = [g for g in grids if old.get(g, {}).get('b') != tag(base)]
    if not todo:
        print(f'전국 예보: {base[0]} {base[1]} 발표 이미 받음')
        return
    today = now.date()

    def job(g):
        nx, ny = grids[g]
        b = base
        try:
            items = fetch(key, nx, ny, *b, tries=3)
        except NoData:
            b = prev_base(*b)
            if old.get(g, {}).get('b') == tag(b):
                return None                 # 최신 발표가 아직 없고 바로 앞 발표는 이미 있음
            items = fetch(key, nx, ny, *b, tries=3)
        days = [[d['date'], d['tmin'], d['tmax'], d['pop'], d['wx'], d['icon']] for d in summarize(items, today)]
        return {'b': tag(b), 'h': hourly_rows(items, now), 'd': days}

    res, fails = {}, 0
    for g, r in parallel(job, todo):
        if isinstance(r, Exception):
            fails += 1
        elif r:
            res[g] = r
    cut = now.strftime('%Y%m%d%H')
    for sd, gs in by_sido.items():
        body = {}
        for g in gs:
            v = res.get(g) or old.get(g)
            if not v:
                continue
            body[g] = {'b': v['b'], 'd': [x for x in v['d'] if x[0] >= today.isoformat()], 'h': [x for x in v['h'] if x[0] >= cut]}
        if body:
            write_json(DATA_DIR / 'fc' / f'{sd}.json',
                       {'source': '기상청 단기예보', 'fields': HOURLY_FIELDS, 'day_fields': DAY_FIELDS}, 'grids',
                       {g: v for g, v in body.items()})
    msg = f'전국 예보: {len(res)}/{len(todo)}개 격자 갱신({base[0]} {base[1]} 발표)'
    print(msg + (f' — {fails}곳 실패(직전 예보 유지, 다음 회차 재시도)' if fails else ''))
    if fails > len(todo) // 3:
        print(f'::warning::전국 예보 {fails}/{len(todo)}곳을 받지 못함')


def migrate_old(by_sido):
    """2026-11-17 첫 판(영업소 6곳) 자료 → 전국 형식으로 옮기고 지움"""
    office_grid = {name: f'{nx},{ny}' for name, _, nx, ny in REGIONS}
    stn_of = {'부산': 159, '울산': 152, '경남동부': 155, '경남서부': 192, '경북동부': 138, '경북서부': 143}
    for p in sorted(DATA_DIR.glob('obs-????-??.json')):
        ym = p.stem[4:]
        old = load_json(p).get('regions', {})
        for sd, gs in by_sido.items():
            path = DATA_DIR / 'obs' / ym / f'{sd}.json'
            cur = load_json(path).get('grids', {})
            moved = False
            for office, rows in old.items():
                g = office_grid.get(office)
                if g in gs:
                    cur.setdefault(g, {}).update({k: v for k, v in rows.items() if k not in cur.get(g, {})})
                    moved = True
            if moved:
                write_json(path, {'source': '기상청 초단기실황(매시 정시, 격자)', 'fields': OBS_FIELDS}, 'grids', cur)
        p.unlink()
        print(f'옛 관측 파일 옮김: {p.name}')
    old_daily = sorted(DATA_DIR.glob('daily-????.json'))
    if old_daily:
        days = defaultdict(dict)
        for p in old_daily:
            for office, rows in load_json(p).get('regions', {}).items():
                if office in stn_of:
                    days[stn_of[office]].update(rows)
        for stn, rows in days.items():
            path = DATA_DIR / 'daily' / f'{stn}.json'
            cur = load_json(path)
            merged = {**rows, **cur.get('days', {})}
            write_json(path, {'stn': stn, 'source': '기상청 종관기상관측(ASOS) 일자료', 'fields': DAILY_FIELDS}, 'days', merged)
        for p in old_daily:
            p.unlink()
        print(f'옛 일자료 파일 옮김: {len(old_daily)}개')
    old_fc = DATA_DIR / 'forecast.json'
    if old_fc.exists():
        old_fc.unlink()


def update_obs(key, now):
    """전국 매시간 관측(초단기실황) 쌓기"""
    grids, by_sido, _ = nation()
    if not grids:
        return
    migrate_old(by_sido)
    latest = (now - timedelta(minutes=45)).replace(minute=0, second=0, microsecond=0)   # 정시 관측은 약 40분 뒤 제공
    window = [latest - timedelta(hours=h) for h in range(21, -1, -1)]                   # 기상청은 지금부터 24시간 안 자료만 줌
    months = sorted({h.strftime('%Y-%m') for h in window})
    files = {(ym, sd): load_json(DATA_DIR / 'obs' / ym / f'{sd}.json').get('grids', {}) for ym in months for sd in by_sido}
    have = defaultdict(set)
    for (ym, sd), gs in files.items():
        for g, rows in gs.items():
            have[g].update(rows)
    recent = {(latest - timedelta(hours=h)).strftime('%Y%m%d%H') for h in range(OBS_EVERY_HOURS)}
    if all(have[g] & recent for g in grids):
        print(f'관측: 최근 {OBS_EVERY_HOURS}시간 안 자료가 이미 있어 이번엔 건너뜀')
        return
    keys = [h.strftime('%Y%m%d%H') for h in window]
    todo = []
    for g in grids:
        known = have[g] & set(keys)
        # 처음 쌓는 격자는 최근 몇 시간만(첫날 호출 수가 하루 한도를 넘지 않게), 이미 쌓던 격자는 지난 22시간 빈 칸 모두
        want = keys if known else keys[-OBS_EVERY_HOURS:]
        todo += [(g, k) for k in want if k not in have[g]]

    def job(t):
        g, k = t
        nx, ny = grids[g]
        try:
            items = fetch(key, nx, ny, k[:8], k[8:] + '00', api=NCST_API, rows=20, tries=2)
        except NoData:
            return None
        v = {i['category']: i.get('obsrValue') for i in items}
        if 'T1H' not in v:
            return None
        pty = num(v.get('PTY'))
        return [num(v.get('T1H')), num(v.get('RN1')), num(v.get('REH')), num(v.get('WSD')), 0 if pty is None else int(pty), num(v.get('VEC'))]

    got, fails = {}, 0
    for t, r in parallel(job, todo):
        if isinstance(r, Exception):
            fails += 1
        elif r:
            got[t] = r
    if got:
        for (g, k), row in got.items():
            ym = f'{k[:4]}-{k[4:6]}'
            for sd, gs in by_sido.items():
                if g in gs:
                    files[(ym, sd)].setdefault(g, {})[k] = row
        for (ym, sd), gs in files.items():
            if gs and any(k[:6] == ym.replace('-', '') for (g, k) in got if g in by_sido[sd]):
                write_json(DATA_DIR / 'obs' / ym / f'{sd}.json', {'source': '기상청 초단기실황(매시 정시, 격자)', 'fields': OBS_FIELDS}, 'grids', gs)
    print(f'관측: {len(got)}/{len(todo)}건 추가' + (f' ({fails}건 실패 — 다음 회차 재시도)' if fails else ''))
    if fails > max(30, len(todo) // 3):
        print(f'::warning::관측 {fails}/{len(todo)}건을 받지 못함')


def update_daily(key, now):
    """전국 지난 날씨 일자료(ASOS) 채우기"""
    _, _, stns = nation()
    if not stns:
        return
    yday = (now - timedelta(days=1 if now.hour >= 12 else 2)).date()   # 어제 자료는 낮에 올라옴 — 오전엔 그제까지만 요청
    start0 = datetime.strptime(ASOS_START, '%Y-%m-%d').date()
    todo = []
    for stn in sorted(stns):
        cur = load_json(DATA_DIR / 'daily' / f'{stn}.json').get('days', {})
        last = max(cur, default=None)
        start = (datetime.strptime(last, '%Y-%m-%d').date() + timedelta(days=1)) if last else start0
        if start <= yday:
            todo.append((stn, start))
    if not todo:
        print('지난 날씨(ASOS): 모두 최신')
        return
    # 활용신청 여부를 한 곳으로 먼저 확인
    try:
        call(ASOS_API, {'serviceKey': key, 'pageNo': 1, 'numOfRows': 1, 'dataType': 'JSON', 'dataCd': 'ASOS', 'dateCd': 'DAY',
                        'startDt': yday.strftime('%Y%m%d'), 'endDt': yday.strftime('%Y%m%d'), 'stnIds': todo[0][0]}, tries=2)
    except NoData:
        pass
    except RuntimeError as e:
        if any(s in str(e) for s in ('JSON', 'HTTP 403', 'HTTP 401')):
            print(f'::warning::지난 날씨(ASOS 일자료): {e} — 「기상청_지상(종관, ASOS) 일자료 조회서비스」 활용신청 확인 필요')
            return

    def job(t):
        stn, start = t
        rows, page, name = {}, 1, None
        while True:
            try:
                items = call(ASOS_API, {'serviceKey': key, 'pageNo': page, 'numOfRows': 999, 'dataType': 'JSON', 'dataCd': 'ASOS',
                                        'dateCd': 'DAY', 'startDt': start.strftime('%Y%m%d'), 'endDt': yday.strftime('%Y%m%d'),
                                        'stnIds': stn}, tries=3)
            except NoData:
                break
            for it in items:
                d = it.get('tm', '')[:10]
                if len(d) == 10:
                    rows[d] = [num(it.get(k)) for k in ('avgTa', 'minTa', 'maxTa', 'sumRn', 'avgRhm', 'avgWs', 'ddMes')]
                    name = name or it.get('stnNm')
            if len(items) < 999:
                break
            page += 1
        return rows, name

    added, fails = 0, []
    for (stn, _), r in parallel(job, todo):
        if isinstance(r, Exception):
            fails.append(stn)
            continue
        rows, api_name = r
        if not rows:
            continue
        path = DATA_DIR / 'daily' / f'{stn}.json'
        cur = load_json(path).get('days', {})
        cur.update(rows)
        write_json(path, {'stn': stn, 'name': stns[stn], 'source': '기상청 종관기상관측(ASOS) 일자료', 'fields': DAILY_FIELDS}, 'days', cur)
        added += len(rows)
        if api_name and api_name.replace('시', '').replace('군', '') != stns[stn].replace('시', '').replace('군', ''):
            print(f'::warning::ASOS {stn}: 지점 이름이 다름(목록 {stns[stn]}, 기상청 {api_name}) — build_regions.py 확인')
    print(f'지난 날씨(ASOS): {len(todo)}개 지점 중 {added}일 추가' + (f', 실패 {fails}' if fails else ''))


def data_age_hours(now):
    """화면에 걸린 weather-data.js 예보가 발표된 지 몇 시간 지났는지(읽을 수 없으면 None)"""
    try:
        t = OUT.read_text(encoding='utf-8')
        d = json.loads(t[t.index('{'):t.rindex('}') + 1])
        year = int(d['updated'][:4])
        base = datetime.strptime(f"{year} {d['base']}", '%Y %m/%d %H:%M').replace(tzinfo=KST)
        if base > now + timedelta(days=1):              # 연말·연초 경계
            base = base.replace(year=year - 1)
        return (now - base).total_seconds() / 3600
    except (OSError, ValueError, KeyError, TypeError):
        return None


def soft_fail(msg):
    """기상청이 GitHub 서버에 잠깐 응답하지 않는 일은 흔함 — 화면 예보가 아직 최근이면 경고만 남기고 성공으로 끝냄
    (실패 알림 메일 안 감). STALE_HOURS를 넘게 멈췄을 때만 실패로 알림."""
    age = data_age_hours(datetime.now(KST))
    if age is not None and age <= STALE_HOURS:
        print(f'::warning::{msg} — 화면은 {age:.0f}시간 전 발표 예보 유지(다음 회차에 재시도)')
        return
    sys.exit(f'{msg} — 화면 날씨가 ' + ('오래' if age is None else f'{age:.0f}시간째') + ' 갱신되지 않음')


if __name__ == '__main__':
    err = None
    try:
        main()
    except SystemExit as e:
        if e.code not in (None, 0):
            err = str(e.code)
    if service_key():                           # 예보가 실패해도 관측·지난 날씨는 따로 채움(실패해도 경고만)
        for job in (update_forecast, update_obs, update_daily):
            try:
                job(service_key(), datetime.now(KST))
            except Exception as e:              # noqa: BLE001 — 화면 예보 갱신을 막지 않게
                print(f'::warning::{job.__doc__}: {type(e).__name__}: {e}')
    if err:
        soft_fail(err)
