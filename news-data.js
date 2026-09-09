// ══════════════════════════════════════════
// 업종 관련 뉴스 데이터 (영남지역 건설 / 레미콘·시멘트 업계 / 그 외 지역 — 3개 패널)
// date는 반드시 "YYYY-MM-DD" 형식(ISO) — 최신순 정렬 및
// "최근 한 달만 표시" 필터링에 사용됩니다.
// 매일 자동 갱신됩니다 (Claude 예약 작업).
// ══════════════════════════════════════════
const NEWS_UPDATED = "2026-09-09";

// 패널 1 — 영남지역 건설·부동산 뉴스
const NEWS_CONSTRUCTION = [
  { title:"신축이 구축보다 싸다…대구 미분양 아파트 전세 '오픈런'", source:"뉴스핌", date:"2026-09-09", url:"https://www.newspim.com/news/view/20260909000284" },
  { title:"\"부산 첫 리뉴얼 자이 브랜드\"…GS건설, 연제갤러리자이 10월 분양", source:"머니투데이", date:"2026-09-08", url:"https://www.mt.co.kr/estate/2026/09/08/2026090809265295720" },
  { title:"대구시, 달서천 5구역 BTL사업 우선협상대상자 지정…2028년 착공", source:"매일신문", date:"2026-09-03", url:"https://www.imaeil.com/page/view/2026090317295320389" },
  { title:"대구 7월 아파트 분양 `제로`…착공도 96% 급감", source:"매일신문", date:"2026-08-29", url:"https://www.imaeil.com/page/view/2026082919041533886" },
  { title:"9월 아파트 입주 1만4174가구…5년 5개월 만에 최소", source:"아주경제", date:"2026-08-28", url:"https://www.ajunews.com/view/20260828170536430" },
  { title:"대형 개발호재 지역 부동산 활기…울산·부산서 신고가", source:"아주경제", date:"2026-08-27", url:"https://www.ajunews.com/view/20260827092248157" },
  { title:"'6개월 새 8000만원↑'…교통망 확충에 양산 물금 부동산 '꿈틀'", source:"머니투데이", date:"2026-08-31", url:"https://www.mt.co.kr/estate/2026/08/31/2026083110581385472" },
  { title:"울산 입주 물량 감소… '그랑라크 에일린의 뜰' 분양", source:"뉴스핌", date:"2026-08-19", url:"https://www.newspim.com/news/view/20260819000943" },
];

// 패널 2 — 레미콘·시멘트 업계 뉴스 (전국 단위, 지역 제한 없음)
const NEWS_CEMENT = [
  { title:"시멘트 불황에 '무역' 키운 성신양회…매출 40% 뛰었다", source:"아시아투데이", date:"2026-09-04", url:"https://www.asiatoday.co.kr/kn/view.php?key=20260904010001680" },
  { title:"삼표그룹, 특수 콘크리트 전문가 키운다…'VAP 제너럴리스트' 양성", source:"아시아투데이", date:"2026-09-01", url:"https://www.asiatoday.co.kr/kn/view.php?key=20260901010000095" },
  { title:"한라시멘트, 폭염·강우 대응 콘크리트 기술인증 획득", source:"아시아투데이", date:"2026-08-25", url:"https://www.asiatoday.co.kr/kn/view.php?key=20260825010008180" },
  { title:"삼표그룹, 코리아빌드위크 참가…혁신기술 대거 공개", source:"아시아투데이", date:"2026-08-12", url:"https://www.asiatoday.co.kr/kn/view.php?key=20260812010003927" },
];

// 패널 3 — 그 외 지역 소식 (수도권·인천·충청·호남 등)
const NEWS_OTHER = [
  { title:"'2.2조'만큼 쌓이는 '불안'…재건축 46개 단지, 좌불안석", source:"머니투데이", date:"2026-09-09", url:"https://www.mt.co.kr/estate/2026/09/09/2026090913500435784" },
  { title:"\"공공임대 비율 조정·분담금 최저화\"…광명 철산하안 재건축 향방은?", source:"머니투데이", date:"2026-09-09", url:"https://www.mt.co.kr/policy/2026/09/09/2026090914314666611" },
  { title:"'모아주택 1호 준공' 강변역 센트럴 아이파크, 입주 시작…한토신 시행", source:"머니투데이", date:"2026-09-08", url:"https://www.mt.co.kr/estate/2026/09/08/2026090809164310626" },
  { title:"\"은마 재건축, 이제 공사비 전쟁\"…한미글로벌, 건설사업관리 맡는다", source:"머니투데이", date:"2026-09-07", url:"https://www.mt.co.kr/estate/2026/09/07/2026090709013625898" },
  { title:"\"14평이 23억\" 1년만에 '5억' 껑충...재건축 속도 내는 목동", source:"머니투데이", date:"2026-09-05", url:"https://www.mt.co.kr/estate/2026/09/05/2026090414063396070" },
  { title:"재건축·재개발 4000세대 풀린다…서울시 통합심의 통과", source:"아주경제", date:"2026-09-04", url:"https://www.ajunews.com/view/20260904110316036" },
  { title:"전남광주 매머드급 '올 뉴 챔피언스시티 1차' 분양...3216가구 규모", source:"뉴스핌", date:"2026-09-02", url:"https://www.newspim.com/news/view/20260902001139" },
];
