// ══════════════════════════════════════════
// 업종 관련 뉴스 데이터 (영남지역 건설 / 레미콘·시멘트 업계 / 그 외 지역 — 3개 패널)
// date는 반드시 "YYYY-MM-DD" 형식(ISO) — 최신순 정렬 및
// "최근 한 달만 표시" 필터링에 사용됩니다.
// 매일 자동 갱신됩니다 (Claude 예약 작업).
// ══════════════════════════════════════════
const NEWS_UPDATED = "2026-09-27";

// 패널 1 — 영남지역 건설·부동산 뉴스
const NEWS_CONSTRUCTION = [
  { title:"김해시, '원도심 RE:CORE 프로젝트' 신규 공모 총력 대응(국비 242억원 규모)", source:"뉴스핌", date:"2026-09-26", url:"https://www.newspim.com/news/view/20260926000094" },
  { title:"삼성물산, 5000억 규모 '부산 사직2 재개발' 시공사 선정(927가구, 4492억원)", source:"이데일리", date:"2026-09-25", url:"https://edaily.co.kr/News/Read?mediaCodeNo=257&newsId=01226726638990928" },
  { title:"리치오션, 부산 다대포항역 인근 350세대 규모 주상복합단지 추진", source:"서울신문", date:"2026-09-23", url:"https://www.seoul.co.kr/news/economy/2026/09/23/20260923500258" },
  { title:"현대건설, 부산 감천2구역 주택재개발 공사 8828억원 수주", source:"디지털투데이", date:"2026-09-22", url:"https://www.digitaltoday.co.kr/disclosure/articleView.html?idxno=702601" },
  { title:"대구 서문시장 4지구, 10년 기다림 끝 연내 착공…상인들 다시 뛴다", source:"글로벌이코노믹", date:"2026-09-22", url:"https://www.g-enews.com/article/General-News/2026/09/202609221021141626d2e64277d7_1" },
  { title:"부산진해경자청, 명지지구 개발사업 실시계획(25차) 변경 완료… 도시 품격·개발사업 활성화 동시에 잡는다", source:"대한경제", date:"2026-09-22", url:"https://www.dnews.co.kr/uhtml/view.jsp?idxno=202609222253116020246" },
  { title:"부산 강서구 에코델타시티 '금강펜테리움 에코리버', 9월 마지막 주 청약 접수", source:"파이낸셜뉴스", date:"2026-09-22", url:"https://www.fnnews.com/news/202609221454364832" },
  { title:"서희건설, 부산 서면(전포1동) 지역주택조합 아파트 신축공사 3182억원 수주", source:"글로벌이코노믹", date:"2026-09-21", url:"https://www.g-enews.com/article/Securities/2026/09/2026092110210135444093b5d4e_1" },
  { title:"창원시, 재건축 정비사업 통합심의 첫 시행…가음1구역 재건축", source:"뉴스핌", date:"2026-09-21", url:"https://www.newspim.com/news/view/20260921000775" },
  { title:"갑절로 뛴 재개발·재건축 공사비…부산 사업장도 배 가까이 증가", source:"부산일보", date:"2026-09-21", url:"https://www.busan.com/view/busan/view.php?code=2026092118212106997" },
  { title:"현대건설, 하루 3곳서 1.7조 확보…도시정비 누적 10조 돌파(울산 남구 B-01구역 '힐스테이트 신정리버프론트' 7110억원 포함)", source:"EBN", date:"2026-09-20", url:"https://www.ebn.co.kr/news/articleView.html?idxno=1724980" },
  { title:"현대건설, 2년 연속 도시정비사업 10조원 수주 돌파(대구 명륜지구 재개발 5001억원 포함)", source:"데일리안", date:"2026-09-20", url:"https://www.dailian.co.kr/news/view/1692606/%ED%98%84%EB%8C%80%EA%B1%B4%EC%84%A4-2%EB%85%84-%EC%97%B0%EC%86%8D-%EB%8F%84%EC%8B%9C%EC%A0%95%EB%B9%84%EC%82%AC%EC%97%85-10-2026" },
  { title:"수성구 30-11구역 재개발조합 시공자 선정 입찰공고(2차)", source:"위클리한국주택경제신문", date:"2026-09-18", url:"https://www.arunews.com/news/articleView.html?idxno=67397" },
  { title:"\"대규모 공원과 명문 학군\"...태영건설 '구미 파크원 데시앙' 11월 분양", source:"파이낸셜뉴스", date:"2026-09-17", url:"https://www.fnnews.com/news/202609171053525401" },
  { title:"연산13구역, 10월 3일 시공자 선정 총회… IPARK현산 유력", source:"위클리한국주택경제신문", date:"2026-09-17", url:"https://www.arunews.com/news/articleView.html?idxno=67356" },
];

// 패널 2 — 레미콘·시멘트 업계 뉴스 (전국 단위, 지역 제한 없음)
const NEWS_CEMENT = [
  { title:"유진기업, 완전자회사 천안기업·지구레미콘 흡수합병 결정…\"경영 효율화 승부수\"", source:"EBN", date:"2026-09-21", url:"https://www.ebn.co.kr/news/articleView.html?idxno=1725192" },
  { title:"\"바닥 다졌나\"...건자재·시멘트株, 주택·인프라 투자에 내년 반등 기대", source:"파이낸셜뉴스", date:"2026-09-23", url:"https://www.fnnews.com/news/202609232158260773" },
  { title:"탄소 줄이니 염소 늘었다…시멘트업계 설비투자 확대(한일시멘트·쌍용C&E 염소바이패스 설비 총 403억원 투자)", source:"시대", date:"2026-09-22", url:"https://www.sidae.com/article/2026092213413082859" },
  { title:"[현장에서] 반도체 볼모 노조 파업 유감...레미콘 트럭 규제 풀어야", source:"뉴스핌", date:"2026-09-15", url:"https://www.newspim.com/news/view/20260915000917" },
  { title:"매출 줄어도 이익 늘렸다...전근식 한일시멘트 대표 '내실 경영' 주력", source:"뉴스핌", date:"2026-09-14", url:"https://www.newspim.com/news/view/20260914000813" },
  { title:"[2026 대경 스마트건설대상] 건설자재대상 쌍용레미콘", source:"대한경제", date:"2026-09-12", url:"https://www.dnews.co.kr/uhtml/view.jsp?idxno=202609122218121310732" },
  { title:"시멘트·레미콘·건설업계 '저탄소 자재 확산' 연대", source:"파이낸셜뉴스", date:"2026-09-10", url:"https://www.fnnews.com/news/202609101830526240" },
  { title:"시멘트 불황에 '무역' 키운 성신양회…매출 40% 뛰었다", source:"아시아투데이", date:"2026-09-04", url:"https://www.asiatoday.co.kr/kn/view.php?key=20260904010001680" },
  { title:"아세아시멘트, 폭염·강우 대응 콘크리트 기술인증 획득", source:"아시아투데이", date:"2026-09-02", url:"https://www.asiatoday.co.kr/kn/view.php?key=20260902010000915" },
  { title:"원가절감 노력에 엇갈린 시멘트社 상반기 실적", source:"이데일리", date:"2026-08-31", url:"https://edaily.co.kr/News/Read?mediaCodeNo=257&newsId=03466966645552896" },
];

// 패널 3 — 그 외 지역 소식 (수도권·인천·충청·호남 등)
const NEWS_OTHER = [
  { title:"'광명시티프라디움에듀하임' 등 9월 마지막 주 전국 8개 단지 3641가구 분양", source:"메트로서울", date:"2026-09-27", url:"https://www.metroseoul.co.kr/article/20260927500011" },
  { title:"두산건설, 5154억 규모 부천 원미 도심복합사업 수주(1628세대)", source:"이투데이", date:"2026-09-21", url:"https://www.etoday.co.kr/news/view/2627896" },
  { title:"삼성물산, 성수3지구 재개발 시공사 선정", source:"아주경제", date:"2026-09-21", url:"https://www.ajunews.com/view/20260921093921069" },
  { title:"19만㎡·450억…멈췄던 인천 영종구 용유 개발, 다시 뛴다", source:"데일리안", date:"2026-09-21", url:"https://www.dailian.co.kr/news/view/1692727/19%EB%A7%8C%E3%8E%A1450%EC%96%B5%EB%A9%88%EC%B7%84%EB%8D%98-%EC%9D%B8%EC%B2%9C-%EC%98%81%EC%A2%85%EA%B5%AC-%EC%9A%A9-2026" },
  { title:"현대건설, '여의도 광장아파트' 수주…도시정비 10조 돌파(38-1구역 재건축, 5463억원)", source:"뉴스1", date:"2026-09-20", url:"https://www.news1.kr/realestate/general/6296346" },
  { title:"분당·일산·산본·평촌…수도권 재건축 시계 빨라진다", source:"한국경제", date:"2026-09-20", url:"https://www.hankyung.com/article/2026092063451" },
  { title:"추석 앞두고 전국 3306가구 청약...경기에만 7개 단지", source:"파이낸셜뉴스", date:"2026-09-18", url:"https://www.fnnews.com/news/202609181543442842" },
  { title:"대신자산신탁, 석촌 하단구역 1500가구 도심복합개발 추진", source:"아시아타임", date:"2026-09-18", url:"https://www.asiatime.co.kr/article/20260918500244" },
  { title:"평택 '힐스테이트 고덕엘리스트' 18일 견본주택 개관…반도체 수혜 기대", source:"뉴스핌", date:"2026-09-17", url:"https://www.newspim.com/news/view/20260917000598" },
  { title:"멈췄던 전주 북부권 개발 다시 뛴다…전주대대 이전 2027년 착공", source:"아시아투데이", date:"2026-09-17", url:"https://www.asiatoday.co.kr/kn/view.php?key=20260917010006585" },
  { title:"서울 미아2구역 4003가구 공급…'강북 미니 신도시'로", source:"아시아경제", date:"2026-09-16", url:"https://view.asiae.co.kr/article/2026091610291717115" },
  { title:"안산 주공4단지, 재건축 시공자 현설에 4곳", source:"위클리한국주택경제신문", date:"2026-09-15", url:"https://www.arunews.com/news/articleView.html?idxno=67300" },
  { title:"산본, 1기 신도시 재건축 첫 시공사 선정 나선다", source:"한국경제", date:"2026-09-14", url:"https://www.hankyung.com/article/2026091437701" },
  { title:"[도시정비시장 풍향계] 쌍문 한양1차 재건축 현설 4곳 참석…내달 30일 입찰", source:"대한경제", date:"2026-09-14", url:"https://www.dnews.co.kr/uhtml/view.jsp?idxno=202609141620383530983" },
  { title:"계룡건설, 서울 종로 '신영1구역 재개발' 시공자 선정(916억원, 199가구)", source:"신아일보", date:"2026-09-14", url:"https://www.shinailbo.co.kr/news/articleView.html?idxno=5062119" },
];
