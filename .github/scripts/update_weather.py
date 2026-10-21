"""영업소 권역 날씨(weather-data.js) 갱신 — GitHub Actions(weather.yml)에서 매시간 실행(예보 내용이 바뀔 때만 커밋).

기상청 단기예보(공공데이터포털 「기상청_단기예보 ((구)_동네예보) 조회서비스」 getVilageFcst)에서
영업소별 대표 도시의 오늘~글피(최대 4일) 최저·최고기온, 하늘상태, 비·눈(강수형태), 강수확률을 하루 단위로 요약한다.

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
# 영업소 → 대표 도시와 기상청 격자(nx, ny) — 시청 위치 기준(기상청 격자 변환식)
REGIONS = [('부산', '부산', 98, 76), ('울산', '울산', 102, 84), ('경남동부', '창원', 91, 77),
           ('경남서부', '진주', 81, 75), ('경북동부', '포항', 102, 94), ('경북서부', '대구', 89, 90)]   # 경북서부는 대구 날씨(사용자 지정)
BASE_TIMES = ['0200', '0500', '0800', '1100', '1400', '1700', '2000', '2300']   # 발표 시각(약 10분 뒤 제공)
DAYS = '월화수목금토일'


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


def fetch(key, nx, ny, base_date, base_time):
    q = urllib.parse.urlencode({'serviceKey': key, 'pageNo': 1, 'numOfRows': 1500, 'dataType': 'JSON',
                                'base_date': base_date, 'base_time': base_time, 'nx': nx, 'ny': ny})
    last = None
    for k in range(3):
        try:
            raw = urllib.request.urlopen(f'{API}?{q}', timeout=30).read()
            d = json.loads(raw)
            hdr = d['response']['header']
            if hdr.get('resultCode') != '00':
                raise RuntimeError(f"기상청 응답 {hdr.get('resultCode')} {hdr.get('resultMsg')}")
            return d['response']['body']['items']['item']
        except (urllib.error.URLError, ValueError, KeyError, RuntimeError) as e:
            # 오류 문구에 인증키가 섞이지 않게 원인만 남김(실행 기록이 공개됨)
            last = e.reason if isinstance(e, urllib.error.URLError) else e
            if isinstance(e, ValueError):
                last = '응답이 JSON이 아님(인증키 미등록·활용신청 전일 수 있음)'
            time.sleep(3 * (k + 1))
    raise RuntimeError(f'기상청 예보를 받지 못함: {last}')


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
    out = []
    for name, city, nx, ny in REGIONS:
        items = fetch(key, nx, ny, base_date, base_time)
        if first and first != (base_date, base_time):
            early = fetch(key, nx, ny, *first)
            seen = {(i['fcstDate'], i['fcstTime'], i['category']) for i in items}
            items = items + [i for i in early if (i['fcstDate'], i['fcstTime'], i['category']) not in seen]
        days = summarize(items, today)
        if not days:
            raise SystemExit(f'{name}: 예보 자료가 비어 있음')
        out.append({'office': name, 'city': city, 'days': days})
        time.sleep(0.5)
    data = {'updated': now.strftime('%Y-%m-%d %H:%M'),
            'base': f'{base_date[4:6]}/{base_date[6:]} {base_time[:2]}:{base_time[2:]}',
            'source': '기상청 단기예보', 'regions': out}
    OUT.write_text('// 영업소 권역 날씨 — .github/scripts/update_weather.py가 매시간 자동 갱신 (기상청 단기예보)\n'
                   'const WEATHER = ' + json.dumps(data, ensure_ascii=False, indent=1) + ';\n', encoding='utf-8', newline='\n')
    print(f'날씨 갱신: {data["base"]} 발표, {len(out)}개 권역 × {len(out[0]["days"])}일')


if __name__ == '__main__':
    main()
