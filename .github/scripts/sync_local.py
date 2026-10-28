"""로컬(PC) 영남지사 폴더를 GitHub 최신 상태로 맞추기 — Windows 작업 스케줄러가 매시간 실행.

PC의 로컬 서버(127.0.0.1:8899)는 이 폴더 파일을 그대로 보여 주는데, 날씨·뉴스·통계는 GitHub에서만 자동 갱신된다.
  1) 가능하면 전체를 최신으로(fast-forward) — 사람이 고친 파일과 겹치지 않을 때
  2) 안 되면 자동 갱신 자료(날씨·뉴스·통계)만 최신으로 — 그 파일을 사람이 고치는 중이면 건드리지 않음
아직 저장소에 올리지 않은 다른 변경(로그인 기능 등)은 절대 바꾸지 않는다. 결과는 .git/sync_local.log에 남김.

  pyw .github/scripts/sync_local.py      # 창 없이 실행(작업 스케줄러용)
  py  .github/scripts/sync_local.py      # 결과를 화면에 보기
"""
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ['weather-data.js', 'news-data.js', 'construction/trend.html']     # GitHub Actions가 자동 갱신하는 파일
GIT = shutil.which('git') or r'C:\Program Files\Git\cmd\git.exe'
LOG = ROOT / '.git' / 'sync_local.log'
NO_WINDOW = getattr(subprocess, 'CREATE_NO_WINDOW', 0)


def git(*args):
    r = subprocess.run([GIT, *args], cwd=ROOT, capture_output=True, text=True, encoding='utf-8',
                       errors='replace', creationflags=NO_WINDOW)
    return r.returncode, (r.stdout + r.stderr).strip()


def main():
    code, out = git('fetch', '-q', 'origin', 'main')
    if code:
        return f'받기 실패(인터넷 확인): {out[:200]}'
    if git('merge-base', '--is-ancestor', 'origin/main', 'HEAD')[0] == 0:
        return '이미 최신'
    code, out = git('merge', '--ff-only', '-q', 'origin/main')
    if code == 0:
        return '전체 최신으로 갱신'
    done, kept = [], []
    for f in DATA:
        if git('diff', '--quiet', '--', f)[0]:              # 사람이 고치는 중(저장소에 안 올린 수정)이면 그대로 둠
            kept.append(f)
            continue
        if git('diff', '--quiet', 'origin/main', '--', f)[0]:
            git('checkout', 'origin/main', '--', f)
            done.append(f)
    msg = '자료만 갱신: ' + (', '.join(done) or '바뀐 것 없음')
    if kept:
        msg += f' / 수정 중이라 건너뜀: {", ".join(kept)}'
    return msg + ' (전체 갱신은 다른 변경과 겹쳐 보류)'


if __name__ == '__main__':
    try:
        result = main()
    except Exception as e:                                  # 작업 스케줄러에서 조용히 실패하지 않게 기록
        result = f'오류: {e}'
    line = f'{datetime.now():%Y-%m-%d %H:%M} {result}'
    print(line)
    try:
        old = LOG.read_text(encoding='utf-8').splitlines()[-300:] if LOG.exists() else []
        LOG.write_text('\n'.join(old + [line]) + '\n', encoding='utf-8')
    except OSError:
        pass
