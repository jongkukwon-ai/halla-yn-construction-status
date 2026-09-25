// ══════════════════════════════════════════
// 업종 관련 뉴스 데이터 (영남지역 건설 / 레미콘·시멘트 업계 / 그 외 지역 — 3개 패널)
// date는 반드시 "YYYY-MM-DD" 형식(ISO) — 최신순 정렬 및
// "최근 한 달만 표시" 필터링에 사용됩니다.
// 매일 자동 갱신됩니다 (Claude 예약 작업).
// ══════════════════════════════════════════
const NEWS_UPDATED = "2026-09-25";

// 패널 1 — 영남지역 건설·부동산 뉴스
const NEWS_CONSTRUCTION = [
  { title:"리치오션, 부산 다대포항역 인근 350세대 규모 주상복합단지 추진", source:"서울신문", date:"2026-09-23", url:"https://www.seoul.co.kr/news/economy/2026/09/23/20260923500258" },
  { title:"현대건설, 부산 감천2구역 주택재개발 공사 8828억원 수주", source:"디지털투데이", date:"2026-09-22", url:"https://www.digitaltoday.co.kr/disclosure/articleView.html?idxno=702601" },
  { title:"대구 서문시장 4지구, 10년 기다림 끝 연내 착공…상인들 다시 뛴다", source:"글로벌이코노믹", date:"2026-09-22", url:"https://www.g-enews.com/article/General-News/2026/09/202609221021141626d2e64277d7_1" },
  { title:"서희건설, 부산 서면(전포1동) 지역주택조합 아파트 신축공사 3182억원 수주", source:"글로벌이코노믹", date:"2026-09-21", url:"https://www.g-enews.com/article/Securities/2026/09/2026092110210135444093b5d4e_1" },
  { title:"창원시, 재건축 정비사업 통합심의 첫 시행…가음1구역 재건축", source:"뉴스핌", date:"2026-09-21", url:"https://www.newspim.com/news/view/20260921000775" },
  { title:"갑절로 뛴 재개발·재건축 공사비…부산 사업장도 배 가까이 증가", source:"부산일보", date:"2026-09-21", url:"https://www.busan.com/view/busan/view.php?code=2026092118212106997" },
  { title:"현대건설, 하루 3곳서 1.7조 확보…도시정비 누적 10조 돌파(울산 남구 B-01구역 '힐스테이트 신정리버프론트' 7110억원 포함)", source:"EBN", date:"2026-09-20", url:"https://www.ebn.co.kr/news/articleView.html?idxno=1724980" },
  { title:"수성구 30-11구역 재개발조합 시공자 선정 입찰공고(2차)", source:"위클리한국주택경제신문", date:"2026-09-18", url:"https://www.arunews.com/news/articleView.html?idxno=67397" },
  { title:"\"대규모 공원과 명문 학군\"...태영건설 '구미 파크원 데시앙' 11월 분양", source:"파이낸셜뉴스", date:"2026-09-17", url:"https://www.fnnews.com/news/202609171053525401" },
  { title:"울산 남구 '문수로 비스타 더파크', 9월 18일 견본주택 개관…22일 1순위 청약", source:"네이트뉴스", date:"2026-09-17", url:"https://m.news.nate.com/view/20260917n06944" },
  { title:"연산13구역, 10월 3일 시공자 선정 총회… IPARK현산 유력", source:"위클리한국주택경제신문", date:"2026-09-17", url:"https://www.arunews.com/news/articleView.html?idxno=67356" },
  { title:"'진주 판문지구 레이크써밋 웰가' 18일 견본주택 개관…9월28일 특별공급", source:"네이트뉴스", date:"2026-09-16", url:"https://m.news.nate.com/view/20260916n29825" },
  { title:"양산 증산지구 도시개발사업 본격 나선다…\"8331억 투입\"", source:"네이트뉴스", date:"2026-09-10", url:"https://m.news.nate.com/view/20260910n30866" },
];

// 패널 2 — 레미콘·시멘트 업계 뉴스 (전국 단위, 지역 제한 없음)
const NEWS_CEMENT = [
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
  { title:"두산건설, 5154억 규모 부천 원미 도심복합사업 수주(1628세대)", source:"이투데이", date:"2026-09-21", url:"https://www.etoday.co.kr/news/view/2627896" },
  { title:"삼성물산, 성수3지구 재개발 시공사 선정", source:"아주경제", date:"2026-09-21", url:"https://www.ajunews.com/view/20260921093921069" },
  { title:"현대건설, '여의도 광장아파트' 수주…도시정비 10조 돌파(38-1구역 재건축, 5463억원)", source:"뉴스1", date:"2026-09-20", url:"https://www.news1.kr/realestate/general/6296346" },
  { title:"분당·일산·산본·평촌…수도권 재건축 시계 빨라진다", source:"한국경제", date:"2026-09-20", url:"https://www.hankyung.com/article/2026092063451" },
  { title:"추석 앞두고 전국 3306가구 청약...경기에만 7개 단지", source:"파이낸셜뉴스", date:"2026-09-18", url:"https://www.fnnews.com/news/202609181543442842" },
  { title:"평택 '힐스테이트 고덕엘리스트' 18일 견본주택 개관…반도체 수혜 기대", source:"뉴스핌", date:"2026-09-17", url:"https://www.newspim.com/news/view/20260917000598" },
  { title:"멈췄던 전주 북부권 개발 다시 뛴다…전주대대 이전 2027년 착공", source:"아시아투데이", date:"2026-09-17", url:"https://www.asiatoday.co.kr/kn/view.php?key=20260917010006585" },
  { title:"안산 주공4단지, 재건축 시공자 현설에 4곳", source:"위클리한국주택경제신문", date:"2026-09-15", url:"https://www.arunews.com/news/articleView.html?idxno=67300" },
  { title:"산본, 1기 신도시 재건축 첫 시공사 선정 나선다", source:"한국경제", date:"2026-09-14", url:"https://www.hankyung.com/article/2026091437701" },
  { title:"[도시정비시장 풍향계] 쌍문 한양1차 재건축 현설 4곳 참석…내달 30일 입찰", source:"대한경제", date:"2026-09-14", url:"https://www.dnews.co.kr/uhtml/view.jsp?idxno=202609141620383530983" },
  { title:"계룡건설, 서울 종로 '신영1구역 재개발' 시공자 선정(916억원, 199가구)", source:"신아일보", date:"2026-09-14", url:"https://www.shinailbo.co.kr/news/articleView.html?idxno=5062119" },
  { title:"삼성물산, '공사비 5122억원' 여의도 목화아파트 재건축 수주", source:"파이낸셜뉴스", date:"2026-09-13", url:"https://www.fnnews.com/news/202609131344590590" },
  { title:"미아2구역 현설에 5개사 참석했으나…입찰참여확약서 롯데건설만 제출", source:"네이트뉴스", date:"2026-09-11", url:"https://m.news.nate.com/view/20260911n33712" },
  { title:"목동12단지 재입찰 현설도 GS건설 홀로…수의계약 가능성 높아져", source:"네이트뉴스", date:"2026-09-09", url:"https://m.news.nate.com/view/20260909n25704" },
  { title:"롯데건설, 도곡우성 재건축 수주…도시정비 4조 돌파", source:"파이낸셜뉴스", date:"2026-09-06", url:"https://www.fnnews.com/news/202609061337294029" },
];
