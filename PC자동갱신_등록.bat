@echo off
chcp 65001 >nul
echo.
echo  [영남지사] PC 화면 날씨·뉴스 자동 갱신 등록
echo  - 매시 25분과 PC 켤 때, GitHub의 최신 날씨·뉴스·통계를 이 폴더로 받아 옵니다.
echo  - 아직 저장소에 올리지 않은 다른 작업(로그인 기능 등)은 건드리지 않습니다.
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0.github\scripts\register_sync_task.ps1"
echo.
echo  위에 OK 가 보이면 등록 완료입니다. 아무 키나 누르면 창이 닫힙니다.
pause >nul
