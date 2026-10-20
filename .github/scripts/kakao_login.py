"""카카오 리프레시 토큰 발급 도우미 — 담당자(보내는 사람)가 본인 PC에서 한 번 실행.

브라우저로 카카오 로그인·동의 화면을 열고, 돌아온 인가 코드로 토큰을 받아 리프레시 토큰을 화면에 보여 줍니다.
보여 준 값은 GitHub 저장소 Settings → Secrets and variables → Actions → KAKAO_REFRESH_TOKEN 에 직접 붙여 넣으세요.
(이 값은 파일로 저장하지 않으며, 채팅·메일로 보내지 마세요.)

사전 준비: 카카오 앱 → 앱 → 플랫폼 키 → REST API 키 → 카카오 로그인 리다이렉트 URI에 http://localhost:8790/callback 등록

  py .github/scripts/kakao_login.py             # 친구목록까지 (카카오 심사 승인 후)
  py .github/scripts/kakao_login.py --only-me   # 심사 전: 나에게 보내기만
"""
import getpass
import sys
import http.server
import json
import urllib.parse
import urllib.request
import webbrowser

PORT = 8790
REDIRECT = f'http://localhost:{PORT}/callback'
SCOPES = 'talk_message,friends'


def main():
    only_me = '--only-me' in sys.argv
    scopes = 'talk_message' if only_me else SCOPES
    if only_me:
        print('「나에게만」 모드: 메시지 전송 권한만 받습니다(친구목록은 카카오 심사 승인 후 이 명령을 --only-me 없이 다시 실행).')
    key = getpass.getpass('카카오 앱 REST API 키(입력해도 화면에 안 보임): ').strip()
    secret = getpass.getpass('Client Secret(사용 안 하면 그냥 Enter): ').strip()
    got = {}

    class H(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            got['code'] = (q.get('code') or [''])[0]
            got['error'] = (q.get('error_description') or q.get('error') or [''])[0]
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write('<h3>카카오 로그인 완료 — 이 창은 닫고 명령 창으로 돌아가세요.</h3>'.encode())

        def log_message(self, *a):
            pass

    srv = http.server.HTTPServer(('localhost', PORT), H)
    url = 'https://kauth.kakao.com/oauth/authorize?' + urllib.parse.urlencode(
        {'client_id': key, 'redirect_uri': REDIRECT, 'response_type': 'code', 'scope': scopes})
    print('브라우저에서 카카오 로그인·동의를 진행하세요. 안 열리면 아래 주소를 직접 여세요.\n' + url)
    webbrowser.open(url)
    srv.timeout = 300
    while 'code' not in got:
        srv.handle_request()
    if not got['code']:
        raise SystemExit(f'로그인 실패: {got["error"]}')
    data = {'grant_type': 'authorization_code', 'client_id': key, 'redirect_uri': REDIRECT, 'code': got['code']}
    if secret:
        data['client_secret'] = secret
    r = json.loads(urllib.request.urlopen(urllib.request.Request(
        'https://kauth.kakao.com/oauth/token', data=urllib.parse.urlencode(data).encode(),
        headers={'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}), timeout=30).read())
    days = int(r.get('refresh_token_expires_in', 0)) // 86400
    print('\n아래 값을 GitHub Secrets의 KAKAO_REFRESH_TOKEN에 붙여 넣으세요 (유효 약 %d일):\n' % days)
    print(r['refresh_token'])
    print('\n동의한 권한:', r.get('scope'))


if __name__ == '__main__':
    main()
