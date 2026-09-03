# -*- coding: utf-8 -*-
"""
영남지사 시스템 로컬 서버 (PWA 설치/실행용)
- 127.0.0.1(내 PC에서만 접속 가능)로 영남지사 폴더를 서빙합니다.
- pythonw.exe로 실행하면 콘솔 창 없이 백그라운드로 조용히 돌아갑니다.
"""

import http.server
import socketserver
import os

PORT = 8899
DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 영남지사 폴더


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, fmt, *args):
        pass  # 콘솔 로그 생략


class ReusableServer(socketserver.TCPServer):
    allow_reuse_address = True


def main():
    with ReusableServer(("127.0.0.1", PORT), QuietHandler) as httpd:
        httpd.serve_forever()


if __name__ == "__main__":
    main()
