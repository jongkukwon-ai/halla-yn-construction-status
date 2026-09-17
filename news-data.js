// ══════════════════════════════════════════
// 업종 관련 뉴스 데이터 (영남지역 건설 / 레미콘·시멘트 업계 / 그 외 지역 — 3개 패널)
// date는 반드시 "YYYY-MM-DD" 형식(ISO) — 최신순 정렬 및
// "최근 한 달만 표시" 필터링에 사용됩니다.
// 매일 자동 갱신됩니다 (Claude 예약 작업).
// ══════════════════════════════════════════
const NEWS_UPDATED = "2026-09-17";

// 패널 1 — 영남지역 건설·부동산 뉴스
const NEWS_CONSTRUCTION = [
  { title:"\"분양가 상승 계속되는데\"… 부산서 1억원대 보증금 신축 아파트 관심", source:"서울신문", date:"2026-09-16", url:"https://www.seoul.co.kr/news/economy/estate/2026/09/16/20260916500135" },
  { title:"부산 첫 '리뉴얼 자이'… 새달 499가구 분양", source:"서울신문", date:"2026-09-15", url:"https://www.seoul.co.kr/news/economy/estate/2026/09/15/20260915022001" },
  { title:"국가철도공단, '동해남부선 센텀역'·'거제역' 유휴부지 민간개발 공모", source:"머니투데이", date:"2026-09-14", url:"https://www.mt.co.kr/policy/2026/09/14/2026091412555770282" },
  { title:"부산 상승세 이끄는 '위브더제니스'…'두산위브더제니스 대연' 무순위 청약 주목", source:"아시아경제", date:"2026-09-14", url:"https://view.asiae.co.kr/article/2026091415170826709" },
  { title:"부산 사상∼해운대 고속도 건설, 동서고가로는 철거 등 방안 모색", source:"머니투데이", date:"2026-09-11", url:"https://www.mt.co.kr/policy/2026/09/11/2026091114574278447" },
  { title:"진주 신축 아파트 품귀…'진주 판문지구 레이크써밋 웰가' 9월 공급", source:"뉴스핌", date:"2026-09-09", url:"https://www.newspim.com/news/view/20260909000381" },
  { title:"당리4구역 재개발조합 시공자 선정 입찰공고", source:"위클리한국주택경제신문", date:"2026-09-09", url:"https://www.arunews.com/news/articleView.html?idxno=66986" },
  { title:"대구시, 청년세대주 부동산 중개수수료 최대 30만원 지원", source:"아시아경제", date:"2026-09-08", url:"https://view.asiae.co.kr/article/2026090810175148557" },
  { title:"대구시, 달서천 5구역 BTL사업 우선협상대상자 지정…2028년 착공", source:"매일신문", date:"2026-09-03", url:"https://www.imaeil.com/page/view/2026090317295320389" },
];

// 패널 2 — 레미콘·시멘트 업계 뉴스 (전국 단위, 지역 제한 없음)
const NEWS_CEMENT = [
  { title:"한일시멘트, 추석 앞두고 협력사 대금 420억원 조기 지급", source:"아시아투데이", date:"2026-09-14", url:"https://www.asiatoday.co.kr/kn/view.php?key=20260914010004981" },
  { title:"아세아시멘트, '강우 환경 대응 콘크리트' 기술인증 획득", source:"대한경제", date:"2026-09-14", url:"https://www.dnews.co.kr/uhtml/view.jsp?idxno=202609141412220540931" },
  { title:"매출 줄어도 이익 늘렸다...전근식 한일시멘트 대표 '내실 경영' 주력", source:"뉴스핌", date:"2026-09-14", url:"https://www.newspim.com/news/view/20260914000813" },
  { title:"전근식 시멘트협회장 \"탄소중립 기술, 산업간 신뢰제고로 함께 실현\"", source:"뉴스핌", date:"2026-09-10", url:"https://www.newspim.com/news/view/20260910000453" },
  { title:"시멘트 불황에 '무역' 키운 성신양회…매출 40% 뛰었다", source:"아시아투데이", date:"2026-09-04", url:"https://www.asiatoday.co.kr/kn/view.php?key=20260904010001680" },
];

// 패널 3 — 그 외 지역 소식 (수도권·인천·충청·호남 등)
const NEWS_OTHER = [
  { title:"포스코이앤씨, 천안 부성2지구 '더샵 천안라크원' 1290가구 10월 분양 예정", source:"뉴스핌", date:"2026-09-16", url:"https://www.newspim.com/news/view/20260916000419" },
  { title:"GTX-C 15일 착공…수원~청량리 '75분→30분' 단축", source:"머니투데이", date:"2026-09-14", url:"https://www.mt.co.kr/estate/2026/09/14/2026091411185578958" },
  { title:"금호건설, 수원 파장1구역 시공사 선정…수원 첫 '아테라' 브랜드 단지", source:"머니투데이", date:"2026-09-14", url:"https://www.mt.co.kr/estate/2026/09/14/2026091409294781837" },
  { title:"LH 손잡은 산본 9-2구역, 3376가구 재건축 시공사 선정 착수", source:"한국경제", date:"2026-09-14", url:"https://www.hankyung.com/article/202609142661i" },
  { title:"\"향남 5년만의 새 아파트\"…KCC건설, 향남역 그로브 스위첸 10월 분양", source:"머니투데이", date:"2026-09-11", url:"https://www.mt.co.kr/estate/2026/09/11/2026091109001823324" },
  { title:"아파트 안 허물고 지하4층 판다…'더샵 분당하이스트' 가보니", source:"머니투데이", date:"2026-09-10", url:"https://www.mt.co.kr/estate/2026/09/10/2026090915185398035" },
  { title:"송파도 꺾였다…강남3구 아파트값 동반 하락", source:"아시아경제", date:"2026-09-10", url:"https://view.asiae.co.kr/article/2026091013431620915" },
  { title:"현대건설, 평택 '힐스테이트 고덕엘리스트' 1779가구 분양", source:"머니투데이", date:"2026-09-09", url:"https://www.mt.co.kr/estate/2026/09/09/2026090913441191577" },
];
