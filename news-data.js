// ══════════════════════════════════════════
// 업종 관련 뉴스 데이터 (영남지역 건설 / 레미콘·시멘트 업계 / 그 외 지역 — 3개 패널)
// date는 반드시 "YYYY-MM-DD" 형식(ISO) — 최신순 정렬 및
// "최근 한 달만 표시" 필터링에 사용됩니다.
// 매일 자동 갱신됩니다 (Claude 예약 작업).
// ══════════════════════════════════════════
const NEWS_UPDATED = "2026-10-09";

// 패널 1 — 영남지역 건설·부동산 뉴스
const NEWS_CONSTRUCTION = [
  { title:"IPARK현대산업개발, 부산 연산13구역 재개발 시공사 최종 선정(도급액 2812억원)", source:"파이낸셜뉴스", date:"2026-10-06", url:"https://www.fnnews.com/news/202610061035254853" },
  { title:"연 200만명 찾는 동래온천…전국 네 번째 '온천도시' 지정", source:"데일리안", date:"2026-10-01", url:"https://www.dailian.co.kr/news/view/1696651" },
  { title:"대구시 '주택시장 정상화' 종합대책 무얼 담았나", source:"뉴스핌", date:"2026-10-02", url:"https://www.newspim.com/news/view/20261002000049" },
  { title:"대구시, 3년 8개월 만에 주택 공급 빗장 푼다… 공급 정상화 수순", source:"서울신문", date:"2026-10-01", url:"https://www.seoul.co.kr/news/economy/2026/10/01/20261001500244" },
  { title:"교통·평지·생활 인프라 삼박자… GS건설, '연제갤러리자이' 10월 분양", source:"뉴데일리경제", date:"2026-09-30", url:"https://biz.newdaily.co.kr/site/data/html/2026/09/30/2026093000111.html" },
  { title:"\"부산 부동산 시장 반등?\", '힐스테이트 사직아시아드'·'베뉴브 해운대' 특별공급 청약에 수요자 몰려", source:"파이낸셜뉴스", date:"2026-09-30", url:"https://www.fnnews.com/news/202509301036250431" },
  { title:"전국 건설계약 27% 늘었는데 대구는 반토막…17개 시·도 꼴찌", source:"경북매일", date:"2026-09-29", url:"https://kbmaeil.com/article/20260928500560" },
  { title:"김해시, '원도심 RE:CORE 프로젝트' 신규 공모 총력 대응(국비 242억원 규모)", source:"뉴스핌", date:"2026-09-26", url:"https://www.newspim.com/news/view/20260926000094" },
  { title:"삼성물산, 5000억 규모 '부산 사직2 재개발' 시공사 선정(927가구, 4492억원)", source:"이데일리", date:"2026-09-25", url:"https://edaily.co.kr/News/Read?mediaCodeNo=257&newsId=01226726638990928" },
  { title:"경남도, 재개발·재건축 표준정관 제정 추진…투명한 조합 운영 지원", source:"뉴스핌", date:"2026-09-23", url:"https://www.newspim.com/news/view/20260923000525" },
  { title:"리치오션, 부산 다대포항역 인근 350세대 규모 주상복합단지 추진", source:"서울신문", date:"2026-09-23", url:"https://www.seoul.co.kr/news/economy/2026/09/23/20260923500258" },
  { title:"현대건설, 부산 감천2구역 주택재개발 공사 8828억원 수주", source:"디지털투데이", date:"2026-09-22", url:"https://www.digitaltoday.co.kr/disclosure/articleView.html?idxno=702601" },
  { title:"갑절로 뛴 재개발·재건축 공사비…부산 사업장도 배 가까이 증가", source:"부산일보", date:"2026-09-21", url:"https://www.busan.com/view/busan/view.php?code=2026092118212106997" },
  { title:"현대건설, 도시정비 수주 2년 연속 10조 돌파(대구 명륜지구 재개발 등 3건, 1조7574억원)", source:"이투데이", date:"2026-09-20", url:"https://www.etoday.co.kr/news/view/2627535" },
  { title:"4년 새 분양 89% 급감한 구미…태영건설, 1355가구 '데시앙' 공급", source:"EBN", date:"2026-09-17", url:"https://www.ebn.co.kr/news/articleView.html?idxno=1724601" },
];

// 패널 2 — 레미콘·시멘트 업계 뉴스 (전국 단위, 지역 제한 없음)
const NEWS_CEMENT = [
  { title:"'레미콘 빅2' 유진·삼표그룹, 국정감사·청문회 촉각", source:"뉴스핌", date:"2026-10-02", url:"https://www.newspim.com/news/view/20261002000897" },
  { title:"레미콘조합연합회, 제주서 경영혁신 해법 모색…\"단단한 성장으로\"", source:"머니투데이", date:"2026-10-06", url:"https://news.mtn.co.kr/news-detail/2026100613165763691" },
  { title:"탄소 줄이니 염소 늘었다…시멘트업계 설비투자 확대(한일시멘트·쌍용C&E 염소바이패스 설비 총 403억원 투자)", source:"시대", date:"2026-09-22", url:"https://www.sidae.com/article/2026092213413082859" },
  { title:"유진기업, 완전자회사 천안기업·지구레미콘 흡수합병 결정…\"경영 효율화 승부수\"", source:"EBN", date:"2026-09-21", url:"https://www.ebn.co.kr/news/articleView.html?idxno=1725192" },
  { title:"매출 줄어도 이익 늘렸다...전근식 한일시멘트 대표 '내실 경영' 주력", source:"뉴스핌", date:"2026-09-14", url:"https://www.newspim.com/news/view/20260914000813" },
  { title:"[2026 대경 스마트건설대상] 건설자재대상 쌍용레미콘", source:"대한경제", date:"2026-09-12", url:"https://www.dnews.co.kr/uhtml/view.jsp?idxno=202609122218121310732" },
  { title:"전근식 시멘트협회장 \"탄소중립 기술, 산업간 신뢰제고로 함께 실현\"", source:"뉴스핌", date:"2026-09-10", url:"https://www.newspim.com/news/view/20260910000453" },
  { title:"시멘트·레미콘·건설업계 '저탄소 자재 확산' 연대", source:"파이낸셜뉴스", date:"2026-09-10", url:"https://www.fnnews.com/news/202609101830526240" },
];

// 패널 3 — 그 외 지역 소식 (수도권·인천·충청·호남 등)
const NEWS_OTHER = [
  { title:"목동 재건축 '수주 홍보관' 대전 시작…10단지, 18일 시공사 선정", source:"머니투데이", date:"2026-10-05", url:"https://news.mtn.co.kr/news-detail/2026100518382248649" },
  { title:"성수전략구역 '옆'도 움직인다…존치 아파트 정비 잰걸음", source:"머니투데이", date:"2026-10-01", url:"https://news.mtn.co.kr/news-detail/2026100116254951561" },
  { title:"목동7단지 재건축, 시공사 선정 지원 CM업체로 건원CM 선정", source:"한경비즈니스", date:"2026-10-02", url:"https://magazine.hankyung.com/money/article/202610029562c" },
  { title:"'또 너냐' 삼성물산 vs 포스코이앤씨…송파 오금현대 재건축서 맞붙나", source:"뉴스핌", date:"2026-09-30", url:"https://www.newspim.com/news/view/20260930001001" },
  { title:"DL이앤씨, 성수2지구 재개발 위해 10개 금융기관과 업무협약", source:"아시아투데이", date:"2026-09-30", url:"https://asiatoday.co.kr/kn/view.php?key=20260930010010492" },
  { title:"분당 재건축 2차 물량 1만3천429가구…시범단지·파크타운 등 5개 구역", source:"경기일보", date:"2026-09-29", url:"https://www.kyeonggi.com/article/20260929580417" },
  { title:"군포 원도심 재개발 본격화...1만 8000세대 신흥 주거타운 탈바꿈", source:"뉴스핌", date:"2026-09-29", url:"https://www.newspim.com/news/view/20260929000661" },
  { title:"'30조 규모' 목동 재건축 속도... 11개 단지 시공사 선정 목전", source:"파이낸셜뉴스", date:"2026-09-27", url:"https://www.fnnews.com/news/202609271757472371" },
  { title:"한남5구역, 조합원 분양신청 돌입…관리처분계획 시동", source:"머니투데이", date:"2026-09-21", url:"https://news.mtn.co.kr/news-detail/2026092117000543031" },
  { title:"노량진4구역이 쏘아올린 '1+1 분양'…곳곳서 추가주택 가격 놓고 갈등", source:"뉴스핌", date:"2026-09-23", url:"https://www.newspim.com/news/view/20260923000746" },
  { title:"서대문구 옛 홍제4구역 일대, 30층-2520가구 재개발 신통기획 확정", source:"뉴스핌", date:"2026-09-22", url:"https://www.newspim.com/news/view/20260922000663" },
  { title:"두산건설, 5154억 규모 부천 원미 도심복합사업 수주(1628세대)", source:"이투데이", date:"2026-09-21", url:"https://www.etoday.co.kr/news/view/2627896" },
  { title:"삼성물산, 성수3지구 재개발 시공사 선정", source:"아주경제", date:"2026-09-21", url:"https://www.ajunews.com/view/20260921093921069" },
  { title:"19만㎡·450억…멈췄던 인천 영종구 용유 개발, 다시 뛴다", source:"데일리안", date:"2026-09-21", url:"https://www.dailian.co.kr/news/view/1692727/19%EB%A7%8C%E3%8E%A1450%EC%96%B5%EB%A9%88%EC%B7%84%EB%8D%98-%EC%9D%B8%EC%B2%9C-%EC%98%81%EC%A2%85%EA%B5%AC-%EC%9A%A9-2026" },
  { title:"[단독]대치 '우쌍', 조합설립인가…10월 시공사 공고에 삼성물산도 채비", source:"머니투데이", date:"2026-09-16", url:"https://news.mtn.co.kr/news-detail/2026091615025075679" },
];
