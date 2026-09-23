// ══════════════════════════════════════════
// 업종 관련 뉴스 데이터 (영남지역 건설 / 레미콘·시멘트 업계 / 그 외 지역 — 3개 패널)
// date는 반드시 "YYYY-MM-DD" 형식(ISO) — 최신순 정렬 및
// "최근 한 달만 표시" 필터링에 사용됩니다.
// 매일 자동 갱신됩니다 (Claude 예약 작업).
// ══════════════════════════════════════════
const NEWS_UPDATED = "2026-09-23";

// 패널 1 — 영남지역 건설·부동산 뉴스
const NEWS_CONSTRUCTION = [
  { title:"포스코이앤씨·현대엔지니어링, 부산 부민2구역 재개발 수주", source:"이데일리", date:"2026-09-23", url:"https://edaily.co.kr/News/Read?mediaCodeNo=257&newsId=01869606635677472" },
  { title:"대구 서문시장 4지구, 10년 기다림 끝 연내 착공…상인들 다시 뛴다", source:"글로벌이코노믹", date:"2026-09-22", url:"https://www.g-enews.com/article/General-News/2026/09/202609221021141626d2e64277d7_1" },
  { title:"갑절로 뛴 재개발·재건축 공사비…부산 사업장도 배 가까이 증가", source:"부산일보", date:"2026-09-21", url:"https://www.busan.com/view/busan/view.php?code=2026092118212106997" },
  { title:"창원시, 재건축 정비사업 통합심의 첫 시행…가음1구역 재건축", source:"부산일보", date:"2026-09-21", url:"https://www.busan.com/view/busan/view.php?code=2026092117441033598" },
  { title:"\"대규모 공원과 명문 학군\"...태영건설 '구미 파크원 데시앙' 11월 분양", source:"파이낸셜뉴스", date:"2026-09-17", url:"https://www.fnnews.com/news/202609171053525401" },
  { title:"'진주 판문지구 레이크써밋 웰가' 18일 견본주택 개관…9월28일 특별공급", source:"네이트뉴스", date:"2026-09-16", url:"https://m.news.nate.com/view/20260916n29825" },
  { title:"\"6개월 새 8000만원↑\"…교통망 확충에 양산 물금 부동산 '꿈틀'", source:"머니투데이", date:"2026-08-31", url:"https://www.mt.co.kr/estate/2026/08/31/2026083110581385472" },
  { title:"양산 집값·개발호재 같이 움직인다…'힐스테이트 양산더스카이' 관심", source:"뉴스핌", date:"2026-08-27", url:"https://www.newspim.com/news/view/20260827000926" },
];

// 패널 2 — 레미콘·시멘트 업계 뉴스 (전국 단위, 지역 제한 없음)
const NEWS_CEMENT = [
  { title:"매출 줄어도 이익 늘렸다...전근식 한일시멘트 대표 '내실 경영' 주력", source:"뉴스핌", date:"2026-09-14", url:"https://www.newspim.com/news/view/20260914000813" },
  { title:"[2026 대경 스마트건설대상] 건설자재대상 쌍용레미콘", source:"대한경제", date:"2026-09-12", url:"https://www.dnews.co.kr/uhtml/view.jsp?idxno=202609122218121310732" },
  { title:"저탄소 시멘트 기술은 나왔는데…업계 \"현장 적용할 제도 개선 시급\"", source:"신아일보", date:"2026-09-10", url:"https://www.shinailbo.co.kr/news/articleView.html?idxno=5060991" },
  { title:"저탄소 시멘트 현장 적용 확대…시멘트·레미콘·건설업계 공동 대응", source:"매일일보", date:"2026-09-10", url:"https://www.m-i.kr/news/articleView.html?idxno=1412519" },
  { title:"시멘트 불황에 '무역' 키운 성신양회…매출 40% 뛰었다", source:"아시아투데이", date:"2026-09-04", url:"https://www.asiatoday.co.kr/kn/view.php?key=20260904010001680" },
  { title:"아세아시멘트, 폭염·강우 대응 콘크리트 기술인증 획득", source:"아시아투데이", date:"2026-09-02", url:"https://www.asiatoday.co.kr/kn/view.php?key=20260902010000915" },
];

// 패널 3 — 그 외 지역 소식 (수도권·인천·충청·호남 등)
const NEWS_OTHER = [
  { title:"'1.8조' 성수3지구 품은 삼성물산…시공사로 선정", source:"MTN뉴스", date:"2026-09-19", url:"https://news.mtn.co.kr/news-detail/2026091916154196913" },
  { title:"금호건설, 송도세브란스병원 우선협상대상자 선정", source:"아시아경제", date:"2026-09-18", url:"https://view.asiae.co.kr/article/2026091821291204536" },
  { title:"전주 노후주택 70%, 신축 갈증 속 '삼천 하늘채 라비엘' 9월 분양", source:"네이트뉴스", date:"2026-09-17", url:"https://m.news.nate.com/view/20260917n06918" },
  { title:"\"미니신도시부터 한강변 대단지까지\"…한남뉴타운 5곳 개발 속도전", source:"머니투데이", date:"2026-09-16", url:"https://www.mt.co.kr/estate/2026/09/16/2026091612191969761" },
  { title:"산본 선도지구 9-2구역, 3376가구 재건축…시공자 선정 착수", source:"파이낸셜뉴스", date:"2026-09-15", url:"https://www.fnnews.com/news/202609150832522341" },
  { title:"KCC건설, 교육·녹지 다 잡은 하이브리드 입지… '향남역 그로브 스위첸' 10월 분양", source:"아시아경제", date:"2026-09-15", url:"https://view.asiae.co.kr/article/2026091510032214037" },
  { title:"롯데건설, 도곡우성 재건축 수주…올해 도시정비 4조 클럽 가입", source:"한국경제", date:"2026-09-07", url:"https://www.hankyung.com/article/2026090793311" },
  { title:"광주·전남 9월 분양전망 엇갈린 온도차…광주 100·전남 60", source:"아시아경제", date:"2026-09-04", url:"https://view.asiae.co.kr/article/2026090412545304616" },
  { title:"롯데·현대 컨소, 1.4조 안양 충훈부 공공재개발 수주", source:"한국금융신문", date:"2026-08-31", url:"https://www.fntimes.com/html/view.php?ud=202608310926125846048b718333_18" },
  { title:"IPARK현대산업개발, 의정부 장암2구역 재개발 시공사 선정", source:"한국경제TV", date:"2026-08-31", url:"https://www.wowtv.co.kr/NewsCenter/News/Read?articleId=A202608310431" },
  { title:"삼성물산, 마포한강삼성 리모델링 따냈다…2810억원 규모", source:"서울경제TV", date:"2026-08-30", url:"https://www.sentv.co.kr/article/view/sentv202608300024" },
];
