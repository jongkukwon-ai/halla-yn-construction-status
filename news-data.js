// ══════════════════════════════════════════
// 업종 관련 뉴스 데이터 (영남지역 건설 / 레미콘·시멘트 업계 / 그 외 지역 — 3개 패널)
// date는 반드시 "YYYY-MM-DD" 형식(ISO) — 최신순 정렬 및
// "최근 한 달만 표시" 필터링에 사용됩니다.
// 매일 자동 갱신됩니다 (Claude 예약 작업).
// ══════════════════════════════════════════
const NEWS_UPDATED = "2026-09-19";

// 패널 1 — 영남지역 건설·부동산 뉴스
const NEWS_CONSTRUCTION = [
  { title:"태영건설 '구미 파크원 데시앙' 11월 분양…대규모 공원 품은 대단지", source:"파이낸셜뉴스", date:"2026-09-17", url:"https://www.fnnews.com/news/202609171053525401" },
  { title:"대구 달성군, 지역주택조합 피해예방 조례안 의결…민주당 양은숙 군의원 대표발의", source:"아시아경제", date:"2026-09-17", url:"https://view.asiae.co.kr/article/2026091714140994675" },
  { title:"울산 남구 '그랑라크 에일린의 뜰' 1521세대, 14일 특별공급 시작", source:"아시아경제", date:"2026-09-14", url:"https://view.asiae.co.kr/article/2026091410181299661" },
  { title:"부산 상승세 이끄는 '위브더제니스'… '두산위브더제니스 대연' 무순위 청약 주목", source:"아시아경제", date:"2026-09-14", url:"https://view.asiae.co.kr/article/2026091415170826709" },
  { title:"\"부산 첫 리뉴얼 자이 브랜드\"…GS건설, 연제갤러리자이 10월 분양", source:"머니투데이", date:"2026-09-08", url:"https://www.mt.co.kr/estate/2026/09/08/2026090809265295720" },
  { title:"\"6개월 새 8000만원↑\"…교통망 확충에 양산 물금 부동산 '꿈틀'", source:"머니투데이", date:"2026-08-31", url:"https://www.mt.co.kr/estate/2026/08/31/2026083110581385472" },
  { title:"[위기의 건설업] '수주 급감' 대구경북 건설사 줄폐업…피 마르는 지역 경제", source:"매일신문", date:"2026-08-21", url:"https://www.imaeil.com/page/view/2026082110094756269" },
];

// 패널 2 — 레미콘·시멘트 업계 뉴스 (전국 단위, 지역 제한 없음)
const NEWS_CEMENT = [
  { title:"매출 줄어도 이익 늘렸다...전근식 한일시멘트 대표 '내실 경영' 주력", source:"뉴스핌", date:"2026-09-14", url:"https://www.newspim.com/news/view/20260914000813" },
  { title:"[2026 대경 스마트건설대상] 건설자재대상 쌍용레미콘", source:"대한경제", date:"2026-09-12", url:"https://www.dnews.co.kr/uhtml/view.jsp?idxno=202609122218121310732" },
  { title:"시멘트 불황에 '무역' 키운 성신양회…매출 40% 뛰었다", source:"아시아투데이", date:"2026-09-04", url:"https://www.asiatoday.co.kr/kn/view.php?key=20260904010001680" },
];

// 패널 3 — 그 외 지역 소식 (수도권·인천·충청·호남 등)
const NEWS_OTHER = [
  { title:"금호건설, 송도세브란스병원 우선협상대상자 선정", source:"아시아경제", date:"2026-09-18", url:"https://view.asiae.co.kr/article/2026091821291204536" },
  { title:"추석 앞둔 9월 넷째주, 4591가구 청약…'더샵분당하이스트' 등 8곳", source:"머니투데이", date:"2026-09-18", url:"https://www.mt.co.kr/estate/2026/09/18/2026091813495279781" },
  { title:"실적 회복한 IPARK현대산업개발, 숙대입구역세권서 '용산벨트' 확장 속도", source:"아시아경제", date:"2026-09-16", url:"https://view.asiae.co.kr/article/2026091615381781015" },
  { title:"[단독] 재개발·재건축 공사비 올려달라더니…검증하자 상위 10곳서 1.6조원 깎여", source:"아시아경제", date:"2026-09-15", url:"https://view.asiae.co.kr/article/2026091510032212774" },
  { title:"KCC건설, 교육·녹지 다 잡은 하이브리드 입지… '향남역 그로브 스위첸' 10월 분양", source:"아시아경제", date:"2026-09-15", url:"https://view.asiae.co.kr/article/2026091510032214037" },
  { title:"\"용적률 1.4배 완화는 과도한 인센티브\"…서울 도심공공복합사업 올스톱", source:"아시아경제", date:"2026-09-14", url:"https://view.asiae.co.kr/article/2026091418443213317" },
  { title:"금호건설, 수원 파장1구역 시공사 선정…수원 첫 '아테라' 브랜드 단지", source:"머니투데이", date:"2026-09-14", url:"https://www.mt.co.kr/estate/2026/09/14/2026091409294781837" },
  { title:"SH, 재개발임대주택 3821가구 모집 재공고…전용 39㎡ 이하 소형", source:"머니투데이", date:"2026-09-09", url:"https://www.mt.co.kr/estate/2026/09/09/2026090916483512189" },
];
