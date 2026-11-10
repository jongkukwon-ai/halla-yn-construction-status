"""건설 동향 리포트(워드 .docx) → 웹 화면(report/index.html)용 자료로 변환.

  python report/tools/docx_to_issue.py <리포트.docx> <호수 YYYY-MM>
  예) python report/tools/docx_to_issue.py 영남권_건설동향_리포트_2026-11.docx 2026-11

만드는 것(report/issues/<호수>/):
  report.docx   원본 워드 파일(화면의 「워드 파일 받기」 버튼)
  figN.png      본문 그림
  content.js    본문(제목·요약·표·그림·뉴스·출처 링크)
그리고 report/issues.js(호수 목록, 최신순)를 다시 만든다. 화면은 기본으로 가장 최신 호를 보여 준다.

리포트 워드 파일은 같은 서식(영남권 건설 동향 리포트 양식)이어야 문단 종류를 알아본다.
표준 라이브러리만 사용한다.
"""
import json
import re
import shutil
import sys
import zipfile
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # report/
ISSUES = ROOT / 'issues'
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'


def text_of(xml):
    out = []
    for m in re.finditer(r'<w:t(?: [^>]*)?>([^<]*)</w:t>|<w:tab/>|<w:br/>', xml):
        out.append(unescape(m.group(1)) if m.group(1) is not None else ' ')
    return ''.join(out)


def runs_of(xml):
    """굵은 글자 구분이 필요한 요약 문단용 — [[글자, 굵게여부], ...]"""
    segs = []
    for r in re.finditer(r'<w:r>(.*?)</w:r>', xml, re.S):
        t = text_of(r.group(1))
        if not t:
            continue
        bold = bool(re.search(r'<w:b/>', r.group(1)))
        if segs and segs[-1][1] == bold:
            segs[-1][0] += t
        else:
            segs.append([t, bold])
    return segs


def top_blocks(body):
    """본문 최상위 문단·표를 순서대로 나눔"""
    parts, start, depth, tag = [], None, 0, None
    for m in re.finditer(r'<(/?)w:(p|tbl|sectPr)\b[^>]*?(/?)>', body):
        close, name, selfc = m.groups()
        if start is None:
            if not close:
                start, tag, depth = m.start(), name, 1
                if selfc:
                    parts.append((name, body[start:m.end()])); start = None
            continue
        if name != tag:
            continue
        depth += -1 if close else (0 if selfc else 1)
        if depth == 0:
            parts.append((tag, body[start:m.end()])); start = None
    return parts


def classify(p, rels, media_map):
    """문단 하나 → 블록(dict) 또는 None"""
    style = re.search(r'<w:pStyle w:val="([^"]+)"', p)
    style = style.group(1) if style else ''
    if '<w:drawing' in p:
        rid = re.search(r'r:embed="([^"]+)"', p).group(1)
        return {'t': 'img', 'src': media_map[rid]}
    txt = text_of(p).strip()
    if not txt:
        return None
    if '<w:hyperlink' in p:
        rid = re.search(r'<w:hyperlink[^>]*r:id="([^"]+)"', p).group(1)
        label = re.sub(r'^·\s*', '', txt.split('  ')[0]).strip()
        return {'t': 'link', 'label': label, 'url': rels[rid]}
    if style == 'Heading1':
        return {'t': 'h1', 'text': txt}
    if style == 'Heading2':
        return {'t': 'h2', 'text': txt}
    if style == 'ListParagraph':
        return {'t': 'li', 'runs': runs_of(p)}
    sz = re.search(r'<w:sz w:val="(\d+)"', p)
    sz = int(sz.group(1)) if sz else 20
    bold = '<w:b/>' in p
    if sz >= 40:
        return {'t': 'title', 'text': txt}
    if '<w:pBdr>' in p:
        return {'t': 'subtitle', 'text': txt}
    if sz == 18 and bold:
        return {'t': 'kicker', 'text': txt}
    if sz == 21 and bold:
        return {'t': 'ntitle', 'text': txt}
    if sz == 17:
        return {'t': 'caption' if 'w:val="center"' in p else 'label', 'text': txt}
    if sz <= 16:
        return {'t': 'source' if txt.startswith('출처:') else 'note', 'text': txt}
    return {'t': 'p', 'text': txt}


def table_of(t):
    rows = []
    for tr in re.findall(r'<w:tr\b.*?</w:tr>', t, re.S):
        rows.append([text_of(tc).strip() for tc in re.findall(r'<w:tc>.*?</w:tc>', tr, re.S)])
    return {'t': 'table', 'head': rows[0], 'rows': rows[1:]}


def convert(docx, issue):
    z = zipfile.ZipFile(docx)
    doc = z.read('word/document.xml').decode('utf-8')
    rel_xml = z.read('word/_rels/document.xml.rels').decode('utf-8')
    rels = {m.group(1): unescape(m.group(2)) for m in re.finditer(r'<Relationship Id="([^"]+)"[^>]*Target="([^"]+)"', rel_xml)}
    out = ISSUES / issue
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    shutil.copy(docx, out / 'report.docx')

    body = doc[doc.index('<w:body>') + 8:doc.index('</w:body>')]
    media_map, blocks = {}, []
    for rid in re.findall(r'r:embed="([^"]+)"', body):
        if rid not in media_map:
            name = f'fig{len(media_map) + 1}.png'
            (out / name).write_bytes(z.read('word/' + rels[rid]))
            media_map[rid] = name
    for kind, x in top_blocks(body):
        if kind == 'tbl':
            blocks.append(table_of(x))
        elif kind == 'p':
            b = classify(x, rels, media_map)
            if b:
                blocks.append(b)

    title = next((b['text'] for b in blocks if b['t'] == 'subtitle'), '')
    basis = re.search(r'\((\d{4}-\d{2}) 기준\)', title)
    y, m = issue.split('-')
    meta = {'id': issue, 'label': f'{y}년 {int(m)}월호', 'basis': basis.group(1) if basis else '', 'subtitle': title}
    (out / 'content.js').write_text(
        '// 건설 동향 리포트 본문 — report/tools/docx_to_issue.py가 워드 파일에서 자동 생성(직접 고치지 말 것)\n'
        f'(window.REPORT_CONTENT = window.REPORT_CONTENT || {{}})[{json.dumps(issue)}] = '
        + json.dumps({'meta': meta, 'blocks': blocks}, ensure_ascii=False, indent=0) + ';\n', encoding='utf-8')
    (out / 'meta.json').write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding='utf-8')
    return meta, len(blocks), len(media_map)


def write_index():
    metas = [json.loads(p.read_text(encoding='utf-8')) for p in ISSUES.glob('*/meta.json')]
    metas.sort(key=lambda m: m['id'], reverse=True)
    (ROOT / 'issues.js').write_text(
        '// 건설 동향 리포트 호수 목록(최신순) — report/tools/docx_to_issue.py가 자동 생성\n'
        'const REPORT_ISSUES = ' + json.dumps(metas, ensure_ascii=False, indent=1) + ';\n', encoding='utf-8')
    return [m['id'] for m in metas]


if __name__ == '__main__':
    if len(sys.argv) != 3 or not re.fullmatch(r'\d{4}-\d{2}', sys.argv[2]):
        sys.exit(__doc__)
    meta, nb, ni = convert(sys.argv[1], sys.argv[2])
    print(f'{meta["label"]} 변환: 블록 {nb}개, 그림 {ni}개 (통계 기준월 {meta["basis"] or "?"})')
    print('호수 목록:', ', '.join(write_index()))
