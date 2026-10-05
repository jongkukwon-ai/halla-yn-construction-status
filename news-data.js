// ══════════════════════════════════════════
// 업종 관련 뉴스 데이터 (영남지역 건설 / 레미콘·시멘트 업계 / 그 외 지역 — 3개 패널)
// date는 반드시 "YYYY-MM-DD" 형식(ISO) — 최신순 정렬 및
// "최근 한 달만 표시" 필터링에 사용됩니다.
// 매일 자동 갱신됩니다 (Claude 예약 작업).
// ══════════════════════════════════════════
const NEWS_UPDATED = "2026-10-05";

// 패널 1 — 영남지역 건설·부동산 뉴스
const NEWS_CONSTRUCTION = [
  { title:"대구시 '주택시장 정상화' 종합대책 무얼 담았나", source:"뉴스핌", date:"2026-10-02", url:"https://www.newspim.com/news/view/20261002000049" },
  { title:"[이번주 재개발ㆍ재건축] 부산 연산13구역 재개발 시공사 결정", source:"대한경제", date:"2026-09-27", url:"https://www.dnews.co.kr/uhtml/view.jsp?idxno=202609271318336830438" },
  { title:"경남도, 재개발·재건축 표준정관 제정 추진…투명한 조합 운영 지원", source:"뉴스핌", date:"2026-09-23", url:"https://www.newspim.com/news/view/20260923000525" },
  { title:"김해시, '원도심 RE:CORE 프로젝트' 신규 공모 총력 대응(국비 242억원 규모)", source:"뉴스핌", date:"2026-09-26", url:"https://www.newspim.com/news/view/20260926000094" },
  { title:"삼성물산, 5000억 규모 '부산 사직2 재개발' 시공사 선정(927가구, 4492억원)", source:"이데일리", date:"2026-09-25", url:"https://edaily.co.kr/News/Read?mediaCodeNo=257&newsId=01226726638990928" },
  { title:"리치오션, 부산 다대포항역 인근 350세대 규모 주상복합단지 추진", source:"서울신문", date:"2026-09-23", url:"https://www.seoul.co.kr/news/economy/2026/09/23/20260923500258" },
  { title:"현대건설, 부산 감천2구역 주택재개발 공사 8828억원 수주", source:"디지털투데이", date:"2026-09-22", url:"https://www.digitaltoday.co.kr/disclosure/articleView.html?idxno=702601" },
  { title:"대구 서문시장 4지구, 10년 기다림 끝 연내 착공…상인들 다시 뛴다", source:"글로벌이코노믹", date:"2026-09-22", url:"https://www.g-enews.com/article/General-News/2026/09/202609221021141626d2e64277d7_1" },
  { title:"부산 강서구 에코델타시티 '금강펜테리움 에코리버', 9월 마지막 주 청약 접수", source:"파이낸셜뉴스", date:"2026-09-22", url:"https://www.fnnews.com/news/202609221454364832" },
  { title:"4년 새 분양 89% 급감한 구미…태영건설, 1355가구 '데시앙' 공급", source:"EBN", date:"2026-09-17", url:"https://www.ebn.co.kr/news/articleView.html?idxno=1724601" },
  { title:"'진주 판문지구 레이크써밋 웰가' 18일 견본주택 개관", source:"한경비즈니스", date:"2026-09-17", url:"https://magazine.hankyung.com/money/article/202609170867c" },
  { title:"울산 B-01구역 재개발, 19일 시공사 선정 총회…현대건설 '유력'", source:"네이트뉴스", date:"2026-09-18", url:"https://m.news.nate.com/view/20260918n18677" },
  { title:"갑절로 뛴 재개발·재건축 공사비…부산 사업장도 배 가까이 증가", source:"부산일보", date:"2026-09-21", url:"https://www.busan.com/view/busan/view.php?code=2026092118212106997" },
  { title:"신동아건설, 부산 범천1구역 가로주택정비사업 수주...2500억 규모", source:"뉴스핌", date:"2026-09-09", url:"https://www.newspim.com/news/view/20260909000457" },
  { title:"\"부산 부동산 시장 반등?\", '힐스테이트 사직아시아드'·'베뉴브 해운대' 특별공급 청약에 수요자 몰려", source:"파이낸셜뉴스", date:"2026-09-30", url:"https://www.fnnews.com/news/202509301036250431" },
];

// 패널 2 — 레미콘·시멘트 업계 뉴스 (전국 단위, 지역 제한 없음)
const NEWS_CEMENT = [
  { title:"'레미콘 빅2' 유진·삼표그룹, 국정감사·청문회 촉각", source:"뉴스핌", date:"2026-10-02", url:"https://www.newspim.com/news/view/20261002000897" },
  { title:"탄소 줄이니 염소 늘었다…시멘트업계 설비투자 확대(한일시멘트·쌍용C&E 염소바이패스 설비 총 403억원 투자)", source:"시대", date:"2026-09-22", url:"https://www.sidae.com/article/2026092213413082859" },
  { title:"유진기업, 완전자회사 천안기업·지구레미콘 흡수합병 결정…\"경영 효율화 승부수\"", source:"EBN", date:"2026-09-21", url:"https://www.ebn.co.kr/news/articleView.html?idxno=1725192" },
  { title:"[현장에서] 반도체 볼모 노조 파업 유감...레미콘 트럭 규제 풀어야", source:"뉴스핌", date:"2026-09-15", url:"https://www.newspim.com/news/view/20260915000917" },
  { title:"매출 줄어도 이익 늘렸다...전근식 한일시멘트 대표 '내실 경영' 주력", source:"뉴스핌", date:"2026-09-14", url:"https://www.newspim.com/news/view/20260914000813" },
  { title:"[2026 대경 스마트건설대상] 건설자재대상 쌍용레미콘", source:"대한경제", date:"2026-09-12", url:"https://www.dnews.co.kr/uhtml/view.jsp?idxno=202609122218121310732" },
  { title:"전근식 시멘트협회장 \"탄소중립 기술, 산업간 신뢰제고로 함께 실현\"", source:"뉴스핌", date:"2026-09-10", url:"https://www.newspim.com/news/view/20260910000453" },
  { title:"시멘트·레미콘·건설업계 '저탄소 자재 확산' 연대", source:"파이낸셜뉴스", date:"2026-09-10", url:"https://www.fnnews.com/news/202609101830526240" },
];

// 패널 3 — 그 외 지역 소식 (수도권·인천·충청·호남 등)
const NEWS_OTHER = [
  { title:"목동7단지 재건축, 시공사 선정 지원 CM업체로 건원CM 선정", source:"한경비즈니스", date:"2026-10-02", url:"https://magazine.hankyung.com/money/article/202610029562c" },
  { title:"'또 너냐' 삼성물산 vs 포스코이앤씨…송파 오금현대 재건축서 맞붙나", source:"뉴스핌", date:"2026-09-30", url:"https://www.newspim.com/news/view/20260930001001" },
  { title:"\"옆 단지도 우리 브랜드로\"…건설사들 '브랜드 타운' 승부", source:"뉴스핌", date:"2026-09-30", url:"https://www.newspim.com/news/view/20260930001044" },
  { title:"DL이앤씨, 성수2지구 재개발 위해 10개 금융기관과 업무협약", source:"아시아투데이", date:"2026-09-30", url:"https://asiatoday.co.kr/kn/view.php?key=20260930010010492" },
  { title:"분당 재건축 2차 물량 1만3천429가구…시범단지·파크타운 등 5개 구역", source:"경기일보", date:"2026-09-29", url:"https://www.kyeonggi.com/article/20260929580417" },
  { title:"군포 원도심 재개발 본격화...1만 8000세대 신흥 주거타운 탈바꿈", source:"뉴스핌", date:"2026-09-29", url:"https://www.newspim.com/news/view/20260929000661" },
  { title:"노량진4구역이 쏘아올린 '1+1 분양'…곳곳서 추가주택 가격 놓고 갈등", source:"뉴스핌", date:"2026-09-23", url:"https://www.newspim.com/news/view/20260923000746" },
  { title:"서대문구 옛 홍제4구역 일대, 30층-2520가구 재개발 신통기획 확정", source:"뉴스핌", date:"2026-09-22", url:"https://www.newspim.com/news/view/20260922000663" },
  { title:"'광명시티프라디움에듀하임' 등 9월 마지막 주 전국 8개 단지 3641가구 분양", source:"메트로서울", date:"2026-09-27", url:"https://www.metroseoul.co.kr/article/20260927500011" },
  { title:"'30조 규모' 목동 재건축 속도... 11개 단지 시공사 선정 목전", source:"파이낸셜뉴스", date:"2026-09-27", url:"https://www.fnnews.com/news/202609271757472371" },
  { title:"두산건설, 5154억 규모 부천 원미 도심복합사업 수주(1628세대)", source:"이투데이", date:"2026-09-21", url:"https://www.etoday.co.kr/news/view/2627896" },
  { title:"삼성물산, 성수3지구 재개발 시공사 선정", source:"아주경제", date:"2026-09-21", url:"https://www.ajunews.com/view/20260921093921069" },
  { title:"19만㎡·450억…멈췄던 인천 영종구 용유 개발, 다시 뛴다", source:"데일리안", date:"2026-09-21", url:"https://www.dailian.co.kr/news/view/1692727/19%EB%A7%8C%E3%8E%A1450%EC%96%B5%EB%A9%88%EC%B7%84%EB%8D%98-%EC%9D%B8%EC%B2%9C-%EC%98%81%EC%A2%85%EA%B5%AC-%EC%9A%A9-2026" },
  { title:"현대건설, '여의도 광장아파트' 수주…도시정비 10조 돌파(38-1구역 재건축, 5463억원)", source:"뉴스1", date:"2026-09-20", url:"https://www.news1.kr/realestate/general/6296346" },
  { title:"송파 전역 재건축 열기…대단지 시공사 선정 '2막' 열렸다(오금현대·잠실 장미 등)", source:"머니투데이", date:"2026-09-11", url:"https://news.mtn.co.kr/news-detail/2026091116254450487" },
];
