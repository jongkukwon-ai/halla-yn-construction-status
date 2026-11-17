"""전국 날씨 조회용 지역 목록(weather/data/regions.json) 만들기 — 지역이 바뀔 때만 손으로 실행.

원자료: 공공데이터포털 「기상청_단기예보 조회서비스」 참고문서 안의
        「기상청41_단기예보 조회서비스_오픈API활용가이드_격자_위경도(YYMM).xlsx」 (압축 파일째 넣어도 됨)
        → 원자료는 임시 폴더에 두고 저장소에는 넣지 않는다.

  python weather/tools/build_regions.py <참고문서.zip 또는 격자_위경도.xlsx>

결과: 시·도 / 시·군·구 / (일반구) 마다 행정구역코드·예보 격자(nx, ny)·위경도·가장 가까운 기상청 종관관측소(ASOS).
"""
import io
import json
import re
import sys
import zipfile
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'weather' / 'data' / 'regions.json'

# 기상청 종관기상관측(ASOS) 지점: 번호 → (이름, 위치로 삼을 지역(시·도, 시·군·구 앞부분 — 비우면 시·도 대표))
# 섬·고산 지점(백령도·울릉도)은 그 군에만 쓰고, 대관령·흑산도·고산·성산은 주변 지역 대표로 쓰지 않음.
ASOS = {
    90: ('속초', '강원', '속초시'), 93: ('북춘천', '강원', '춘천시'), 95: ('철원', '강원', '철원군'), 98: ('동두천', '경기', '동두천시'),
    99: ('파주', '경기', '파주시'), 101: ('춘천', '강원', '춘천시'), 102: ('백령도', '인천', '옹진군'), 104: ('북강릉', '강원', '강릉시'),
    105: ('강릉', '강원', '강릉시'), 106: ('동해', '강원', '동해시'), 108: ('서울', '서울', ''), 112: ('인천', '인천', ''),
    114: ('원주', '강원', '원주시'), 115: ('울릉도', '경상북도', '울릉군'), 119: ('수원', '경기', '수원시권선구'), 121: ('영월', '강원', '영월군'),
    127: ('충주', '충청북도', '충주시'), 129: ('서산', '충청남도', '서산시'), 130: ('울진', '경상북도', '울진군'), 131: ('청주', '충청북도', '청주시흥덕구'),
    133: ('대전', '대전', ''), 135: ('추풍령', '충청북도', '영동군'), 136: ('안동', '경상북도', '안동시'), 137: ('상주', '경상북도', '상주시'),
    138: ('포항', '경상북도', '포항시남구'), 140: ('군산', '전북', '군산시'), 143: ('대구', '대구', ''), 146: ('전주', '전북', '전주시덕진구'),
    152: ('울산', '울산', ''), 155: ('창원', '경상남도', '창원시성산구'), 156: ('광주', '전남광주', '북구'), 159: ('부산', '부산', ''),
    162: ('통영', '경상남도', '통영시'), 165: ('목포', '전남광주', '목포시'), 168: ('여수', '전남광주', '여수시'), 170: ('완도', '전남광주', '완도군'),
    172: ('고창', '전북', '고창군'), 174: ('순천', '전남광주', '순천시'), 177: ('홍성', '충청남도', '홍성군'), 184: ('제주', '제주', '제주시'),
    189: ('서귀포', '제주', '서귀포시'), 192: ('진주', '경상남도', '진주시'), 201: ('강화', '인천', '강화군'), 202: ('양평', '경기', '양평군'),
    203: ('이천', '경기', '이천시'), 211: ('인제', '강원', '인제군'), 212: ('홍천', '강원', '홍천군'), 216: ('태백', '강원', '태백시'),
    217: ('정선군', '강원', '정선군'), 221: ('제천', '충청북도', '제천시'), 226: ('보은', '충청북도', '보은군'), 232: ('천안', '충청남도', '천안시동남구'),
    235: ('보령', '충청남도', '보령시'), 236: ('부여', '충청남도', '부여군'), 238: ('금산', '충청남도', '금산군'), 239: ('세종', '세종', ''),
    243: ('부안', '전북', '부안군'), 244: ('임실', '전북', '임실군'), 245: ('정읍', '전북', '정읍시'), 247: ('남원', '전북', '남원시'),
    248: ('장수', '전북', '장수군'), 252: ('영광군', '전남광주', '영광군'), 253: ('김해시', '경상남도', '김해시'), 254: ('순창군', '전북', '순창군'),
    255: ('북창원', '경상남도', '창원시의창구'), 257: ('양산시', '경상남도', '양산시'), 258: ('보성군', '전남광주', '보성군'), 259: ('강진군', '전남광주', '강진군'),
    260: ('장흥', '전남광주', '장흥군'), 261: ('해남', '전남광주', '해남군'), 262: ('고흥', '전남광주', '고흥군'), 263: ('의령군', '경상남도', '의령군'),
    264: ('함양군', '경상남도', '함양군'), 266: ('광양시', '전남광주', '광양시'), 268: ('진도군', '전남광주', '진도군'), 271: ('봉화', '경상북도', '봉화군'),
    272: ('영주', '경상북도', '영주시'), 273: ('문경', '경상북도', '문경시'), 276: ('청송군', '경상북도', '청송군'), 277: ('영덕', '경상북도', '영덕군'),
    278: ('의성', '경상북도', '의성군'), 279: ('구미', '경상북도', '구미시'), 281: ('영천', '경상북도', '영천시'), 283: ('경주시', '경상북도', '경주시'),
    284: ('거창', '경상남도', '거창군'), 285: ('합천', '경상남도', '합천군'), 288: ('밀양', '경상남도', '밀양시'), 289: ('산청', '경상남도', '산청군'),
    294: ('거제', '경상남도', '거제시'), 295: ('남해', '경상남도', '남해군'),
}
OWN_ONLY = {102, 115}          # 이 지점은 자기 군에만 사용
SKIP = {'이어도'}               # 해상 관측 기지(행정구역 아님)
# 시·도 보여 줄 순서(목록에 없는 새 시·도는 뒤에 행정구역코드 순)
SIDO_ORDER = ['서울', '부산', '대구', '인천', '광주', '전남광주', '대전', '울산', '세종', '경기', '강원', '충청북도', '충청남도', '전북', '전라남도', '경상북도', '경상남도', '제주']


def read_rows(path):
    p = Path(path)
    if p.suffix.lower() == '.zip':
        z = zipfile.ZipFile(p)
        name = next(i for i in z.infolist() if i.filename.lower().endswith('.xlsx'))
        data = z.read(name)
    else:
        data = p.read_bytes()
    ws = openpyxl.load_workbook(io.BytesIO(data), read_only=True, data_only=True).worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    head = [str(h or '').strip() for h in rows[0]]
    col = {k: head.index(k) for k in ('행정구역코드', '1단계', '2단계', '3단계', '격자 X', '격자 Y', '경도(초/100)', '위도(초/100)')}
    for r in rows[1:]:
        g = lambda k: '' if r[col[k]] is None else str(r[col[k]]).strip()
        yield {k: g(k) for k in col}


def main(src):
    regions = []
    for r in read_rows(src):
        if r['3단계'] or not r['격자 X'] or r['1단계'] in SKIP:
            continue                                    # 읍·면·동은 넣지 않음(시·군·구 단위까지)
        sido, name = r['1단계'], r['2단계']
        si, gu = name, ''
        m = re.fullmatch(r'(.+?시)(.+구)', name)           # 「창원시의창구」 → 창원시 / 의창구 (도 아래 일반구)
        if m and not re.search(r'(특별시|광역시|특별자치시)$', sido):
            si, gu = m.group(1), m.group(2)
        regions.append({'code': r['행정구역코드'], 'sido': sido, 'si': si, 'gu': gu, 'name': name,
                        'nx': int(r['격자 X']), 'ny': int(r['격자 Y']),
                        'lon': round(float(r['경도(초/100)']), 4), 'lat': round(float(r['위도(초/100)']), 4)})
    # ASOS 지점 위치 = 기준 지역의 격자
    pos = {}
    for stn, (nm, sido_key, name_key) in ASOS.items():
        cand = [g for g in regions if g['sido'].startswith(sido_key)
                and ((not name_key and not g['si']) or (name_key and g['name'] == name_key))]
        if not cand:
            sys.exit(f'ASOS {stn} {nm}: 기준 지역({sido_key} {name_key})을 찾지 못함')
        pos[stn] = (cand[0]['nx'], cand[0]['ny'], cand[0]['code'])
    for g in regions:
        own = [s for s in OWN_ONLY if pos[s][2] == g['code']]
        pool = own or [s for s in pos if s not in OWN_ONLY]
        d2 = lambda s: (pos[s][0] - g['nx']) ** 2 + (pos[s][1] - g['ny']) ** 2
        best = min(pool, key=lambda s: (d2(s), s not in (101, 105)))   # 같은 거리면 춘천·강릉 본 지점 우선
        g['stn'] = best
        g['stn_km'] = round(d2(best) ** 0.5 * 5)                       # 격자 1칸 ≈ 5km
    sidos = []
    for g in regions:
        if g['sido'] not in sidos:
            sidos.append(g['sido'])
    rank = lambda sd: next((i for i, k in enumerate(SIDO_ORDER) if sd.startswith(k)), len(SIDO_ORDER))
    sidos.sort(key=lambda sd: (rank(sd), next(g['code'] for g in regions if g['sido'] == sd)))
    out = {'source': f'기상청 단기예보 격자·위경도표({Path(src).name})', 'fields': ['행정구역코드', '시도', '시군구', '구', '격자X', '격자Y', '경도', '위도', 'ASOS지점', '지점거리km'],
           'stations': {str(s): v[0] for s, v in ASOS.items()}, 'sidos': sidos,
           'regions': [[g['code'], g['sido'], g['si'], g['gu'], g['nx'], g['ny'], g['lon'], g['lat'], g['stn'], g['stn_km']] for g in regions]}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    body = ',\n'.join('  ' + json.dumps(r, ensure_ascii=False) for r in out.pop('regions'))
    head = ',\n'.join(f' {json.dumps(k, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)}' for k, v in out.items())
    OUT.write_text('{\n' + head + ',\n "regions": [\n' + body + '\n ]\n}\n', encoding='utf-8', newline='\n')
    grids = {(g['nx'], g['ny']) for g in regions}
    print(f'{len(regions)}개 지역(시·도 대표 포함), 예보 격자 {len(grids)}곳, 시·도 {len(sidos)}개 → {OUT}')
    far = sorted(regions, key=lambda g: -g['stn_km'])[:5]
    print('관측소가 가장 먼 지역:', [(g['sido'], g['name'], ASOS[g['stn']][0], g['stn_km']) for g in far])


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
