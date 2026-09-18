// ══════════════════════════════════════════
// 업종 관련 뉴스 데이터 (영남지역 건설 / 레미콘·시멘트 업계 / 그 외 지역 — 3개 패널)
// date는 반드시 "YYYY-MM-DD" 형식(ISO) — 최신순 정렬 및
// "최근 한 달만 표시" 필터링에 사용됩니다.
// 매일 자동 갱신됩니다 (Claude 예약 작업).
// ══════════════════════════════════════════
const NEWS_UPDATED = "2026-09-18";

// 패널 1 — 영남지역 건설·부동산 뉴스
const NEWS_CONSTRUCTION = [
  { title:"대우건설, 신대방역세권 재개발정비사업 수주", source:"아시아경제", date:"2026-09-18", url:"https://view.asiae.co.kr/article/2026091814061971694" },
  { title:"진주 신축 아파트 품귀…'진주 판문지구 레이크써밋 웰가' 9월 공급", source:"뉴스핌", date:"2026-09-09", url:"https://www.newspim.com/news/view/20260909000381" },
  { title:"GS건설, 부산 트리플 역세권 '연제갤러리자이' 10월 분양", source:"아시아경제", date:"2026-09-08", url:"https://view.asiae.co.kr/article/2026090809180918768" },
  { title:"대구시, 청년세대주 부동산 중개수수료 최대 30만원 지원", source:"아시아경제", date:"2026-09-08", url:"https://view.asiae.co.kr/article/2026090810175148557" },
  { title:"중흥토건 '부산 장안 중흥S-클래스' 선착순 동·호 지정 분양", source:"아시아경제", date:"2026-09-07", url:"https://view.asiae.co.kr/article/2026090717064805144" },
  { title:"대구시, 달서천 5구역 BTL사업 우선협상대상자 지정…2028년 착공", source:"매일신문", date:"2026-09-03", url:"https://www.imaeil.com/page/view/2026090317295320389" },
];

// 패널 2 — 레미콘·시멘트 업계 뉴스 (전국 단위, 지역 제한 없음)
const NEWS_CEMENT = [
  { title:"한일시멘트, 추석 앞두고 협력사 대금 420억원 조기 지급", source:"아시아투데이", date:"2026-09-14", url:"https://www.asiatoday.co.kr/kn/view.php?key=20260914010004981" },
  { title:"아세아시멘트, '강우 환경 대응 콘크리트' 기술인증 획득", source:"대한경제", date:"2026-09-14", url:"https://www.dnews.co.kr/uhtml/view.jsp?idxno=202609141412220540931" },
  { title:"[2026 대경 스마트건설대상] 건설자재대상 쌍용레미콘", source:"대한경제", date:"2026-09-12", url:"https://www.dnews.co.kr/uhtml/view.jsp?idxno=202609122218121310732" },
  { title:"시멘트·레미콘·건설업계, '저탄소 건축자재' 적용 확대 협력 논의", source:"아시아경제", date:"2026-09-10", url:"https://view.asiae.co.kr/article/2026091015134520350" },
  { title:"전근식 시멘트협회장 \"탄소중립 기술, 산업간 신뢰제고로 함께 실현\"", source:"뉴스핌", date:"2026-09-10", url:"https://www.newspim.com/news/view/20260910000453" },
];

// 패널 3 — 그 외 지역 소식 (수도권·인천·충청·호남 등)
const NEWS_OTHER = [
  { title:"금호건설, 송도세브란스병원 우선협상대상자 선정", source:"아시아경제", date:"2026-09-18", url:"https://view.asiae.co.kr/article/2026091821291204536" },
  { title:"추석 앞둔 9월 넷째주, 4591가구 청약…'더샵분당하이스트' 등 8곳", source:"머니투데이", date:"2026-09-18", url:"https://www.mt.co.kr/estate/2026/09/18/2026091813495279781" },
  { title:"실적 회복한 IPARK현대산업개발, 숙대입구역세권서 '용산벨트' 확장 속도", source:"아시아경제", date:"2026-09-16", url:"https://view.asiae.co.kr/article/2026091615381781015" },
  { title:"KCC건설, 교육·녹지 다 잡은 하이브리드 입지… '향남역 그로브 스위첸' 10월 분양", source:"아시아경제", date:"2026-09-15", url:"https://view.asiae.co.kr/article/2026091510032214037" },
  { title:"\"용적률 1.4배 완화는 과도한 인센티브\"…서울 도심공공복합사업 올스톱", source:"아시아경제", date:"2026-09-14", url:"https://view.asiae.co.kr/article/2026091418443213317" },
  { title:"금호건설, 수원 파장1구역 시공사 선정…수원 첫 '아테라' 브랜드 단지", source:"머니투데이", date:"2026-09-14", url:"https://www.mt.co.kr/estate/2026/09/14/2026091409294781837" },
];
