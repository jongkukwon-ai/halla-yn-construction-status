# Cloudflare 배포 안내 (영남지사 정보 조회 시스템)

회사 메일 인증코드로 로그인하는 비공개 사이트로 올리는 순서입니다.
계정·연락처 같은 개인정보는 저장소에 올리지 않고 Cloudflare D1 데이터베이스에만 둡니다.

## 구성

| 역할 | 담당 |
|---|---|
| 화면(HTML) | Cloudflare Pages — 이 저장소 그대로 배포 |
| 로그인 | Cloudflare Access — `@hallacement.co.kr` 메일로 받은 인증코드 |
| 누구인지·권한 확인, 계정관리 | `functions/_middleware.js` (로컬 `_server/serve.py`와 같은 API) |
| 계정·권한등급 저장 | D1 데이터베이스(바인딩 이름 `DB`), 표 구조는 `cloudflare/schema.sql` |

## 처음 한 번 설정

1. **Cloudflare 가입**(무료).
2. **Pages 프로젝트 만들기**: Workers & Pages → 만들기 → Pages → Git에 연결 → `halla-yn-construction-status` 선택
   - 프로덕션 브랜치 `main`, 빌드 명령 비움, 빌드 출력 디렉터리 `/`
3. **D1 데이터베이스 만들기**: 저장소 및 데이터베이스 → D1 → 만들기(이름 예: `yn-db`)
   - 콘솔 탭에 내 PC의 `_server/cloudflare_seed.sql` 내용을 붙여넣고 실행
     (파일이 없으면 `py _server/make_cloudflare_seed.py`로 만듦 — 이 파일은 저장소에 올리지 않음)
4. **Pages에 D1 연결**: Pages 프로젝트 → 설정 → 바인딩 → D1 추가 → 변수 이름 `DB`, 데이터베이스 `yn-db`
5. **Access 설정**: Zero Trust → (팀 이름 정하기, 예: `halla-yn`) → Access → 애플리케이션 → 자체 호스팅 추가
   - 도메인: `<프로젝트>.pages.dev` 와 `*.<프로젝트>.pages.dev`(미리보기 주소) 둘 다
   - 정책: 허용(Allow) / 포함: 다음으로 끝나는 이메일 `@hallacement.co.kr`
   - 로그인 방법: 일회용 PIN
   - 저장 후 애플리케이션 개요의 **AUD 태그**를 복사
6. **환경변수**: Pages 프로젝트 → 설정 → 변수
   - `ACCESS_TEAM_DOMAIN` = `halla-yn.cloudflareaccess.com` (5번에서 정한 팀 이름)
   - `ACCESS_AUD` = 5번에서 복사한 AUD 태그
7. **다시 배포** 후 본인 메일로 로그인 → 홈 오른쪽 위에 이름과 「계정관리」가 보이면 완료.

## 확인 후

- 저장소를 비공개로 전환하면 기존 `github.io` 주소는 더 열리지 않습니다(무료 요금제). 구성원에게 새 주소를 알려 주세요.
- 비공개 저장소는 GitHub Actions 무료 사용시간(월 2,000분)을 씁니다. 날씨 갱신(`weather.yml`)을 매시간에서 2~3시간 간격으로 줄이는 것을 권합니다.
- 회사 메일 보안 필터가 인증코드 메일(Cloudflare 발송)을 막지 않는지 처음에 한 번 확인하세요.

## 운영

- 인사이동: 계정관리 화면에서 그 직책의 이름·사번·이메일을 바꾸면 이전 담당자는 바로 들어올 수 없습니다.
- 변경 이력은 D1의 `audit` 표에 남습니다.
- 계정표에 없는 회사 메일은 인증을 통과해도 「등록되지 않은 메일」 화면에서 막힙니다.
