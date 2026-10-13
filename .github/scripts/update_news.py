"""업종 관련 뉴스(news-data.js) 매일 자동 갱신 — GitHub Actions에서 실행.

Google 뉴스 RSS(기계 수집용 공개 피드)를 검색어별로 받아
영남 건설 / 레미콘·시멘트 / 그 외 지역 3개 패널로 나누고,
기존 기사 중 30일 이내인 것과 합쳐 패널마다 최신순 최대 20건을 남긴다.
표준 라이브러리만 사용한다.
"""
import io
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'news-data.js'
KST = timezone(timedelta(hours=9))
TODAY = datetime.now(KST).date()
KEEP_DAYS = 30      # 화면이 최근 30일만 보여줌
FRESH_DAYS = 14     # 새로 받을 기사 범위
PER_PANEL = 20
PER_SOURCE = 2      # 한 패널에 같은 언론사 최대 건수(새 기사 기준)

QUERIES = {
    'C': ['부산 재개발', '부산 재건축', '부산 분양', '부산 착공', '부산 시공사 선정', '울산 분양', '울산 재개발',
          '대구 재건축', '대구 분양', '창원 재개발', '김해 분양', '양산 아파트', '경남 아파트 분양',
          '경북 아파트 분양', '포항 분양', '구미 아파트', '경산 아파트', '거제 진주 아파트'],
    'M': ['시멘트', '레미콘', '쌍용C&E', '한라시멘트', '아세아시멘트', '한일시멘트', '삼표시멘트', '성신양회',
          '레미콘 업계', '시멘트 업계'],
    'O': ['서울 재건축 시공사', '서울 재개발', '수도권 분양', '인천 재개발', '경기 재건축', '충청 아파트 분양',
          '광주 재개발', '대전 아파트 분양', '세종 아파트', '강원 아파트 분양', '전북 아파트'],
}
YN = r'부산|울산|대구|경남|경북|창원|김해|양산|거제|진주|통영|사천|밀양|포항|구미|경산|경주|김천|안동|영주|상주|칠곡|기장|해운대|동래|사하|금정|연제|사상|달서|수성구|울주|영남'
TOPIC = r'재개발|재건축|분양|착공|시공사|수주|아파트|청약|입주|정비|건설|공사|준공|기공|공급|주택|단지'
CEMENT = r'시멘트|레미콘|C&E|성신양회|삼표|유진기업|골재|슬래그'
# 시멘트 패널은 '시멘트'가 비유·사건 기사에도 나와서 업계 맥락 단어가 같이 있어야 함
CEMENT_CTX = r'업계|업체|협상|단가|가격|수급|공장|생산|출하|탄소|배출권|실적|영업이익|배당|주주|투자|설비|국감|국정감사|협회|조합|파업|운송|타결|인상|품질|건설|아파트|LH|현장|시멘트사|레미콘사|C&E|성신양회|유진기업'
JUNK = (r'부고|인사\]|\[인사|포토|날씨|운세|오늘의|광고|채용|게시판|봉사|환경정화|붕괴|화재|사망|숨져|추락|시신|살해|혈관'
        r'|특징주|주가|상한가|관련주|테마|% ?↑|%\s*상승|%\s*하락|거래 \d|국힘|민주당|우클릭|규모, 동향|예측|투자분석|\(왼쪽\)|\(오른쪽\)|인도네시아|베트남')
BLOCK_SOURCES = {'IndexBox', 'Vietnam.vn', 'VOI.ID', '인벤', '톱스타뉴스', '주달'}


def fetch(query):
    url = 'https://news.google.com/rss/search?' + urllib.parse.urlencode(
        {'q': f'{query} when:{FRESH_DAYS}d', 'hl': 'ko', 'gl': 'KR', 'ceid': 'KR:ko'})
    req = urllib.request.Request(url, headers={'User-Agent': 'halla-yn-news-bot/1.0 (+GitHub Actions)'})
    root = ET.fromstring(urllib.request.urlopen(req, timeout=30).read())
    for it in root.findall('.//item'):
        src = (it.findtext('source') or '').strip()
        title = (it.findtext('title') or '').strip()
        if src and title.endswith(' - ' + src):
            title = title[: -len(' - ' + src)].strip()
        src = re.sub(r'\s+-\s+.*$', '', src).replace('​', '').strip()   # "울산매일 - 울산최초…" → "울산매일"
        try:
            date = parsedate_to_datetime(it.findtext('pubDate')).astimezone(KST).date()
        except (TypeError, ValueError):
            continue
        yield {'title': title, 'source': src, 'date': date.isoformat(), 'url': it.findtext('link') or ''}


def toks(t):
    return set(re.findall(r'[가-힣A-Za-z0-9]{2,}', t))


def similar(a, b):
    A, B = toks(a), toks(b)
    return len(A & B) / max(1, len(A | B)) > 0.3


def junk(x):
    return bool(re.search(JUNK, x['title'])) or x['source'] in BLOCK_SOURCES


def belongs(panel, x):
    title = x['title']
    if junk(x):
        return False
    if panel == 'M':
        return bool(re.search(CEMENT, title)) and bool(re.search(CEMENT_CTX, title))
    if re.search(CEMENT, title) or not re.search(TOPIC, title):
        return False
    return bool(re.search(YN, title)) if panel == 'C' else not re.search(YN, title)


ITEM = re.compile(r'\{\s*title:\s*"((?:[^"\\]|\\.)*)",\s*source:\s*"((?:[^"\\]|\\.)*)",\s*date:\s*"([0-9-]+)",\s*url:\s*"((?:[^"\\]|\\.)*)"\s*\}')


def read_existing(text, name):
    blk = text[text.index('const ' + name):]
    blk = blk[blk.index('['):blk.index('];') + 1]
    return [{'title': json.loads('"' + m[1] + '"'), 'source': json.loads('"' + m[2] + '"'),
             'date': m[3], 'url': json.loads('"' + m[4] + '"')} for m in ITEM.finditer(blk)]


def main():
    text = DATA.read_text(encoding='utf-8')
    names = {'C': 'NEWS_CONSTRUCTION', 'M': 'NEWS_CEMENT', 'O': 'NEWS_OTHER'}
    old = {k: read_existing(text, v) for k, v in names.items()}

    fetched = {k: [] for k in QUERIES}
    ok = 0
    for panel, queries in QUERIES.items():
        for q in queries:
            try:
                items = list(fetch(q))
                ok += 1
            except Exception as e:   # 한 검색어 실패는 건너뜀
                print(f'  검색 실패 "{q}": {e}')
                continue
            fetched[panel] += [x for x in items if belongs(panel, x)]
            time.sleep(1)
    if ok == 0:
        sys.exit('Google 뉴스 RSS를 하나도 받지 못했습니다 — news-data.js는 그대로 둡니다.')

    cutoff = (TODAY - timedelta(days=KEEP_DAYS)).isoformat()
    result = {}
    for k in names:
        new = sorted(fetched[k], key=lambda x: x['date'], reverse=True)
        picked, per_src = [], {}
        for x in new:                                  # 새 기사: 같은 사건·같은 언론사 과다 방지
            if per_src.get(x['source'], 0) >= PER_SOURCE or any(similar(x['title'], y['title']) for y in picked):
                continue
            picked.append(x)
            per_src[x['source']] = per_src.get(x['source'], 0) + 1
        merged = []
        kept = [o for o in old[k] if o['date'] >= cutoff and not junk(o)]   # 기존 기사도 같은 기준으로 걸러냄
        for x in sorted(picked + kept, key=lambda x: x['date'], reverse=True):
            if x['date'] > TODAY.isoformat() or any(similar(x['title'], y['title']) for y in merged):
                continue
            merged.append(x)
            if len(merged) >= PER_PANEL:
                break
        result[k] = merged
        print(f'{names[k]}: 새 후보 {len(picked)}건 → 최종 {len(merged)}건 (최신 {merged[0]["date"] if merged else "-"})')

    def js(arr):
        return '\n'.join('  { title:%s, source:%s, date:"%s", url:%s },' % (
            json.dumps(x['title'], ensure_ascii=False), json.dumps(x['source'], ensure_ascii=False),
            x['date'], json.dumps(x['url'])) for x in arr)

    head = text[:text.index('const NEWS_UPDATED')]
    head = head.replace('매일 자동 갱신됩니다 (Claude 예약 작업).', '매일 자동 갱신됩니다 (GitHub Actions — .github/scripts/update_news.py).')
    body = (f'const NEWS_UPDATED = "{TODAY.isoformat()}";\n\n'
            '// 패널 1 — 영남지역 건설·부동산 뉴스\nconst NEWS_CONSTRUCTION = [\n' + js(result['C']) + '\n];\n\n'
            '// 패널 2 — 레미콘·시멘트 업계 뉴스 (전국)\nconst NEWS_CEMENT = [\n' + js(result['M']) + '\n];\n\n'
            '// 패널 3 — 그 외 지역 건설·부동산 뉴스\nconst NEWS_OTHER = [\n' + js(result['O']) + '\n];\n')
    DATA.write_text(head + body, encoding='utf-8', newline='')


if __name__ == '__main__':
    main()
