"""영업소 권역 날씨(weather-data.js) 갱신 — GitHub Actions(weather.yml)에서 매시간 실행(예보 내용이 바뀔 때만 커밋).

기상청 단기예보(공공데이터포털 「기상청_단기예보 ((구)_동네예보) 조회서비스」 getVilageFcst)에서
영업소별 대표 도시의 오늘~글피(최대 4일) 최저·최고기온, 하늘상태, 비·눈(강수형태), 강수확률을 하루 단위로 요약한다.

날씨 화면(weather/index.html)용 자료도 함께 만든다(weather/data/):
  forecast.json        시간대별 예보(같은 getVilageFcst 응답 — 추가 호출 없음)
  obs-YYYY-MM.json     매시간 관측(초단기실황 getUltraSrtNcst, 같은 서비스) — 3시간마다 지난 24시간 빈 칸을 채워 쌓음
  daily-YYYY.json      지난 날씨 일자료(「기상청_지상(종관, ASOS) 일자료 조회서비스」, 2021-01-01부터 어제까지)
                       → 공공데이터포털에서 이 서비스를 따로 「활용신청」해야 함. 안 했으면 경고만 남기고 건너뜀.

필요한 GitHub Secret: DATA_GO_KR_KEY (공공데이터포털 일반 인증키 — Decoding/Encoding 어느 쪽이든 됨)
공공데이터포털에서 위 서비스를 「활용신청」해 두어야 한다(자동 승인). 키가 없으면 아무것도 바꾸지 않고 끝낸다.

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
ASOS_STN = {'부산': 159, '울산': 152, '경남동부': 155, '경남서부': 192, '경북동부': 138, '경북서부': 143}
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
    prev_hourly = load_json(DATA_DIR / 'forecast.json').get('regions', {})
    out, failed, streak, hourly = [], [], 0, {}
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
            hourly[name] = hourly_rows(items, now)
            streak = 0
        except RuntimeError as e:
            print(f'::warning::{name}: {e}')       # GitHub 주석(로그인 없이 확인 가능)으로 원인 남김
            if name not in prev:
                raise SystemExit(f'{name}: 예보를 받지 못했고 오늘 자 직전 자료도 없어 갱신하지 않음')
            out.append(prev[name])              # 이 권역만 직전 예보 유지
            if name in prev_hourly:
                hourly[name] = [r for r in prev_hourly[name] if r[0] >= now.strftime('%Y%m%d%H')]
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
    write_rows(DATA_DIR / 'forecast.json',
               {'source': '기상청 단기예보', 'base': data['base'], 'fields': HOURLY_FIELDS,
                'cities': {n: c for n, c, _, _ in REGIONS}},
               {n: {r[0]: r[1:] for r in rows} for n, rows in hourly.items()}, as_list=True)
    print(f'날씨 갱신: {data["base"]} 발표, {len(out)}개 권역 × {len(out[0]["days"])}일'
          + (f' (직전 예보 유지: {", ".join(failed)})' if failed else ''))


# ── 날씨 화면(weather/index.html)용 자료 ─────────────────────────────────────────
HOURLY_FIELDS = ['시각', '기온', '하늘', '강수형태', '강수확률', '강수량', '습도', '풍속', '적설']
OBS_FIELDS = ['기온', '1시간강수량', '습도', '풍속', '강수형태', '풍향']
DAILY_FIELDS = ['평균기온', '최저기온', '최고기온', '강수량', '평균습도', '평균풍속', '최심적설']


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


def write_rows(path, meta, regions, as_list=False):
    """{권역: {열쇠: 값 목록}} → 한 줄에 한 시각(하루)씩 쓴 JSON (git에서 바뀐 줄만 보이게)"""
    path.parent.mkdir(parents=True, exist_ok=True)
    dump = lambda v: json.dumps(v, ensure_ascii=False, separators=(',', ':'))
    parts = []
    for name in sorted(regions, key=lambda n: [r[0] for r in REGIONS].index(n) if n in [r[0] for r in REGIONS] else 99):
        rows = regions[name]
        if as_list:
            body = ',\n'.join(f'   {dump([k, *rows[k]])}' for k in sorted(rows))
            parts.append(f'  {dump(name)}: [\n{body}\n  ]')
        else:
            body = ',\n'.join(f'   {dump(k)}: {dump(rows[k])}' for k in sorted(rows))
            parts.append(f'  {dump(name)}: {{\n{body}\n  }}')
    head = ',\n'.join(f' {dump(k)}: {dump(v)}' for k, v in meta.items())
    path.write_text('{\n' + head + ',\n "regions": {\n' + ',\n'.join(parts) + '\n }\n}\n', encoding='utf-8', newline='\n')


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


def update_obs(key, now):
    """매시간 관측(초단기실황) 쌓기"""
    latest = (now - timedelta(minutes=45)).replace(minute=0, second=0, microsecond=0)   # 정시 관측은 약 40분 뒤 제공
    window = [latest - timedelta(hours=h) for h in range(23, -1, -1)]                   # 지난 24시간까지 받을 수 있음
    files = {}
    for h in window:
        ym = h.strftime('%Y-%m')
        if ym not in files:
            files[ym] = {n: dict(v) for n, v in load_json(DATA_DIR / f'obs-{ym}.json').get('regions', {}).items()}
    have = lambda name, h: h.strftime('%Y%m%d%H') in files[h.strftime('%Y-%m')].get(name, {})
    recent = [latest - timedelta(hours=h) for h in range(OBS_EVERY_HOURS)]
    if all(any(have(n, h) for h in recent) for n, *_ in REGIONS):
        print(f'관측: 최근 {OBS_EVERY_HOURS}시간 안 자료가 이미 있어 이번엔 건너뜀')
        return
    added, misses = 0, 0
    for name, city, nx, ny in REGIONS:
        for h in window:
            if have(name, h):
                continue
            try:
                items = fetch(key, nx, ny, h.strftime('%Y%m%d'), h.strftime('%H00'), api=NCST_API, rows=20, tries=2)
            except NoData:
                continue
            except RuntimeError as e:
                misses += 1
                if misses >= 6:
                    print(f'::warning::관측 자료 받기가 계속 실패해 중단: {e}')
                    break
                continue
            v = {i['category']: i.get('obsrValue') for i in items}
            if 'T1H' not in v:
                continue
            pty = num(v.get('PTY'))
            files[h.strftime('%Y-%m')].setdefault(name, {})[h.strftime('%Y%m%d%H')] = [
                num(v.get('T1H')), num(v.get('RN1')), num(v.get('REH')), num(v.get('WSD')),
                0 if pty is None else int(pty), num(v.get('VEC'))]
            added += 1
            time.sleep(0.15)
        else:
            continue
        break
    if added:
        for ym, regions in files.items():
            if regions:
                write_rows(DATA_DIR / f'obs-{ym}.json',
                           {'source': '기상청 초단기실황(매시 정시, 영업소 대표 도시 격자)', 'fields': OBS_FIELDS}, regions)
    print(f'관측: {added}개 시각 추가')


def update_daily(key, now):
    """지난 날씨 일자료(ASOS) 채우기"""
    yday = (now - timedelta(days=1 if now.hour >= 12 else 2)).date()   # 어제 자료는 낮에 올라옴 — 오전엔 그제까지만 요청
    years = range(int(ASOS_START[:4]), yday.year + 1)
    files = {y: {n: dict(v) for n, v in load_json(DATA_DIR / f'daily-{y}.json').get('regions', {}).items()} for y in years}
    added = 0
    for name, stn in ASOS_STN.items():
        last = max((d for y in years for d in files[y].get(name, {})), default=None)
        start = (datetime.strptime(last, '%Y-%m-%d').date() + timedelta(days=1)) if last else datetime.strptime(ASOS_START, '%Y-%m-%d').date()
        if start > yday:
            continue
        page = 1
        while True:
            try:
                items = call(ASOS_API, {'serviceKey': key, 'pageNo': page, 'numOfRows': 999, 'dataType': 'JSON',
                                        'dataCd': 'ASOS', 'dateCd': 'DAY', 'startDt': start.strftime('%Y%m%d'),
                                        'endDt': yday.strftime('%Y%m%d'), 'stnIds': stn}, tries=2)
            except NoData:
                break
            except RuntimeError as e:
                print(f'::warning::지난 날씨(ASOS 일자료) {name}: {e} — 공공데이터포털에서 「기상청_지상(종관, ASOS) 일자료 조회서비스」 활용신청이 필요할 수 있음')
                if 'JSON' in str(e):
                    return                      # 활용신청 전 — 다른 권역도 같은 결과라 바로 끝냄
                break
            for it in items:
                d = it.get('tm', '')[:10]
                if len(d) != 10:
                    continue
                files[int(d[:4])].setdefault(name, {})[d] = [num(it.get(k)) for k in
                                                              ('avgTa', 'minTa', 'maxTa', 'sumRn', 'avgRhm', 'avgWs', 'ddMes')]
                added += 1
            if len(items) < 999:
                break
            page += 1
            time.sleep(0.3)
    if added:
        for y, regions in files.items():
            if regions:
                write_rows(DATA_DIR / f'daily-{y}.json',
                           {'source': '기상청 종관기상관측(ASOS) 일자료', 'fields': DAILY_FIELDS,
                            'stations': {n: s for n, s in ASOS_STN.items()}}, regions)
    print(f'지난 날씨(ASOS): {added}일 추가')


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
        for job in (update_obs, update_daily):
            try:
                job(service_key(), datetime.now(KST))
            except Exception as e:              # noqa: BLE001 — 화면 예보 갱신을 막지 않게
                print(f'::warning::{job.__doc__}: {type(e).__name__}: {e}')
    if err:
        soft_fail(err)
