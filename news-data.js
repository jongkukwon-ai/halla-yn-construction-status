// ══════════════════════════════════════════
// 업종 관련 뉴스 데이터 (영남지역 건설 / 레미콘·시멘트 업계 / 그 외 지역 — 3개 패널)
// date는 반드시 "YYYY-MM-DD" 형식(ISO) — 최신순 정렬 및
// "최근 한 달만 표시" 필터링에 사용됩니다.
// 매일 자동 갱신됩니다 (Claude 예약 작업).
// ══════════════════════════════════════════
const NEWS_UPDATED = "2026-09-23";

// 패널 1 — 영남지역 건설·부동산 뉴스
const NEWS_CONSTRUCTION = [
  { title:"여의도·울산·대구서 하루에 1.7조 삼켰다… 거침없는 현대건설 '10조 질주'", source:"디지털타임스", date:"2026-09-20", url:"https://www.dt.co.kr/article/12084904" },
  { title:"창원시, 재건축 정비사업 통합심의 첫 시행…가음1구역 재건축", source:"뉴스핌", date:"2026-09-21", url:"https://www.newspim.com/news/view/20260921000775" },
  { title:"대구 서문시장 4지구, 10년 기다림 끝 연내 착공…상인들 다시 뛴다", source:"글로벌이코노믹", date:"2026-09-22", url:"https://www.g-enews.com/article/General-News/2026/09/202609221021141626d2e64277d7_1" },
  { title:"갑절로 뛴 재개발·재건축 공사비…부산 사업장도 배 가까이 증가", source:"부산일보", date:"2026-09-21", url:"https://www.busan.com/view/busan/view.php?code=2026092118212106997" },
  { title:"\"대규모 공원과 명문 학군\"...태영건설 '구미 파크원 데시앙' 11월 분양", source:"파이낸셜뉴스", date:"2026-09-17", url:"https://www.fnnews.com/news/202609171053525401" },
  { title:"'진주 판문지구 레이크써밋 웰가' 18일 견본주택 개관…9월28일 특별공급", source:"네이트뉴스", date:"2026-09-16", url:"https://m.news.nate.com/view/20260916n29825" },
  { title:"\"6개월 새 8000만원↑\"…교통망 확충에 양산 물금 부동산 '꿈틀'", source:"머니투데이", date:"2026-08-31", url:"https://www.mt.co.kr/estate/2026/08/31/2026083110581385472" },
  { title:"양산 집값·개발호재 같이 움직인다…'힐스테이트 양산더스카이' 관심", source:"뉴스핌", date:"2026-08-27", url:"https://www.newspim.com/news/view/20260827000926" },
];

// 패널 2 — 레미콘·시멘트 업계 뉴스 (전국 단위, 지역 제한 없음)
const NEWS_CEMENT = [
  { title:"원가절감 노력에 엇갈린 시멘트社 상반기 실적", source:"이데일리", date:"2026-08-31", url:"https://edaily.co.kr/News/Read?mediaCodeNo=257&newsId=03466966645552896" },
  { title:"매출 줄어도 이익 늘렸다...전근식 한일시멘트 대표 '내실 경영' 주력", source:"뉴스핌", date:"2026-09-14", url:"https://www.newspim.com/news/view/20260914000813" },
  { title:"[2026 대경 스마트건설대상] 건설자재대상 쌍용레미콘", source:"대한경제", date:"2026-09-12", url:"https://www.dnews.co.kr/uhtml/view.jsp?idxno=202609122218121310732" },
  { title:"저탄소 시멘트 기술은 나왔는데…업계 \"현장 적용할 제도 개선 시급\"", source:"신아일보", date:"2026-09-10", url:"https://www.shinailbo.co.kr/news/articleView.html?idxno=5060991" },
  { title:"저탄소 시멘트 현장 적용 확대…시멘트·레미콘·건설업계 공동 대응", source:"매일일보", date:"2026-09-10", url:"https://www.m-i.kr/news/articleView.html?idxno=1412519" },
  { title:"시멘트 불황에 '무역' 키운 성신양회…매출 40% 뛰었다", source:"아시아투데이", date:"2026-09-04", url:"https://www.asiatoday.co.kr/kn/view.php?key=20260904010001680" },
  { title:"아세아시멘트, 폭염·강우 대응 콘크리트 기술인증 획득", source:"아시아투데이", date:"2026-09-02", url:"https://www.asiatoday.co.kr/kn/view.php?key=20260902010000915" },
];

// 패널 3 — 그 외 지역 소식 (수도권·인천·충청·호남 등)
const NEWS_OTHER = [
  { title:"분당·일산·산본·평촌…수도권 재건축 시계 빨라진다", source:"한국경제", date:"2026-09-20", url:"https://www.hankyung.com/article/2026092063451" },
  { title:"삼성물산, '공사비 5122억원' 여의도 목화아파트 재건축 수주", source:"파이낸셜뉴스", date:"2026-09-13", url:"https://www.fnnews.com/news/202609131344590590" },
  { title:"안산 주공4단지, 재건축 시공자 현설에 4곳", source:"위클리한국주택경제신문", date:"2026-09-15", url:"https://www.arunews.com/news/articleView.html?idxno=67300" },
  { title:"산본, 1기 신도시 재건축 첫 시공사 선정 나선다", source:"한국경제", date:"2026-09-14", url:"https://www.hankyung.com/article/2026091437701" },
  { title:"[도시정비시장 풍향계] 쌍문 한양1차 재건축 현설 4곳 참석…내달 30일 입찰", source:"대한경제", date:"2026-09-14", url:"https://www.dnews.co.kr/uhtml/view.jsp?idxno=202609141620383530983" },
  { title:"광주·전남 9월 분양전망 엇갈린 온도차…광주 100·전남 60", source:"아시아경제", date:"2026-09-04", url:"https://view.asiae.co.kr/article/2026090412545304616" },
  { title:"'검암역 푸르지오 프라베뉴' 1순위 청약 2161건…평균 18.96대 1", source:"한국금융신문", date:"2026-09-02", url:"https://www.fntimes.com/html/view.php?ud=202609021054147784048b718333_18" },
  { title:"신동아건설, 송파 풍납강변현대 가로주택정비사업 수주...539억원 규모", source:"뉴스핌", date:"2026-08-31", url:"https://www.newspim.com/news/view/20260831000549" },
  { title:"시티오씨엘 9단지 견본주택, 나흘간 1만8000명 찾아", source:"아주경제", date:"2026-08-30", url:"https://www.ajunews.com/view/20260830144133962" },
];
