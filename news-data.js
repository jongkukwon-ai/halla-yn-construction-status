// ══════════════════════════════════════════
// 업종 관련 뉴스 데이터 (영남지역 건설 / 레미콘·시멘트 업계 / 그 외 지역 — 3개 패널)
// date는 반드시 "YYYY-MM-DD" 형식(ISO) — 최신순 정렬 및
// "최근 한 달만 표시" 필터링에 사용됩니다.
// 매일 자동 갱신됩니다 (Claude 예약 작업).
// ══════════════════════════════════════════
const NEWS_UPDATED = "2026-09-20";

// 패널 1 — 영남지역 건설·부동산 뉴스
const NEWS_CONSTRUCTION = [
  { title:"현대건설, 2년 연속 정비사업 수주 10조 돌파…\"목표액 넘어설 듯\"", source:"머니투데이", date:"2026-09-20", url:"https://www.mt.co.kr/estate/2026/09/20/2026092009240340453" },
  { title:"울산·경주, 전철부터 도시가스까지…'생활권 동맹' 속도 낸다", source:"아시아경제", date:"2026-09-17", url:"https://view.asiae.co.kr/article/2026091715095686792" },
  { title:"울산 남구 '그랑라크 에일린의 뜰' 1521세대, 14일 특별공급 시작", source:"아시아경제", date:"2026-09-14", url:"https://view.asiae.co.kr/article/2026091410181299661" },
  { title:"부산 상승세 이끄는 '위브더제니스'… '두산위브더제니스 대연' 무순위 청약 주목", source:"아시아경제", date:"2026-09-14", url:"https://view.asiae.co.kr/article/2026091415170826709" },
  { title:"신동아건설, '부산 범천동 가로주택정비사업' 수주…누적 3500억원", source:"아시아경제", date:"2026-09-09", url:"https://view.asiae.co.kr/article/2026090909550078408" },
  { title:"\"부산 첫 리뉴얼 자이 브랜드\"…GS건설, 연제갤러리자이 10월 분양", source:"머니투데이", date:"2026-09-08", url:"https://www.mt.co.kr/estate/2026/09/08/2026090809265295720" },
  { title:"양산 집값·개발호재 같이 움직인다…'힐스테이트 양산더스카이' 관심", source:"뉴스핌", date:"2026-08-27", url:"https://www.newspim.com/news/view/20260827000926" },
];

// 패널 2 — 레미콘·시멘트 업계 뉴스 (전국 단위, 지역 제한 없음)
const NEWS_CEMENT = [
  { title:"매출 줄어도 이익 늘렸다...전근식 한일시멘트 대표 '내실 경영' 주력", source:"뉴스핌", date:"2026-09-14", url:"https://www.newspim.com/news/view/20260914000813" },
  { title:"[2026 대경 스마트건설대상] 건설자재대상 쌍용레미콘", source:"대한경제", date:"2026-09-12", url:"https://www.dnews.co.kr/uhtml/view.jsp?idxno=202609122218121310732" },
  { title:"시멘트·레미콘·건설업계, 저탄소 콘크리트 확산에 총력", source:"파이낸셜뉴스", date:"2026-09-10", url:"https://www.fnnews.com/news/202609101131067992" },
  { title:"시멘트 불황에 '무역' 키운 성신양회…매출 40% 뛰었다", source:"아시아투데이", date:"2026-09-04", url:"https://www.asiatoday.co.kr/kn/view.php?key=20260904010001680" },
];

// 패널 3 — 그 외 지역 소식 (수도권·인천·충청·호남 등)
const NEWS_OTHER = [
  { title:"금호건설, 송도세브란스병원 우선협상대상자 선정", source:"아시아경제", date:"2026-09-18", url:"https://view.asiae.co.kr/article/2026091821291204536" },
  { title:"추석 앞둔 9월 넷째주, 4591가구 청약…'더샵분당하이스트' 등 8곳", source:"머니투데이", date:"2026-09-18", url:"https://www.mt.co.kr/estate/2026/09/18/2026091813495279781" },
  { title:"실적 회복한 IPARK현대산업개발, 숙대입구역세권서 '용산벨트' 확장 속도", source:"아시아경제", date:"2026-09-16", url:"https://view.asiae.co.kr/article/2026091615381781015" },
  { title:"\"미니신도시부터 한강변 대단지까지\"…한남뉴타운 5곳 개발 속도전", source:"머니투데이", date:"2026-09-16", url:"https://www.mt.co.kr/estate/2026/09/16/2026091612191969761" },
  { title:"KCC건설, 교육·녹지 다 잡은 하이브리드 입지… '향남역 그로브 스위첸' 10월 분양", source:"아시아경제", date:"2026-09-15", url:"https://view.asiae.co.kr/article/2026091510032214037" },
  { title:"\"용적률 1.4배 완화는 과도한 인센티브\"…서울 도심공공복합사업 올스톱", source:"아시아경제", date:"2026-09-14", url:"https://view.asiae.co.kr/article/2026091418443213317" },
  { title:"금호건설, 수원 파장1구역 시공사 선정…수원 첫 '아테라' 브랜드 단지", source:"머니투데이", date:"2026-09-14", url:"https://www.mt.co.kr/estate/2026/09/14/2026091409294781837" },
  { title:"\"공공임대 비율 조정·분담금 최저화\"…광명 철산하안 재건축 향방은?", source:"머니투데이", date:"2026-09-09", url:"https://www.mt.co.kr/policy/2026/09/09/2026090914314666611" },
];
