// ══════════════════════════════════════════
// 건설뉴스 데이터 (영남지역 중심 + 그 외 지역)
// 매일 자동 갱신됩니다 (Claude 예약 작업)
// ══════════════════════════════════════════
const NEWS_UPDATED = "2026.09.04";

const NEWS_YN = [
  { title:"입찰 경쟁 피하는 건설사들… 움츠린 부산 재개발·재건축", source:"부산일보", date:"2026.02.09", url:"https://mobile.busan.com/view/busan/view.php?code=2026020918423014322" },
  { title:"HJ중공업, 3497억 규모 부산 범천5구역 재개발정비사업 수주", source:"헤럴드경제(계열)", date:"2026.04.09", url:"https://heraldk.com/2026/04/09/hj%EC%A4%91%EA%B3%B5%EC%97%85-3497%EC%96%B5-%EA%B7%9C%EB%AA%A8-%EB%B6%80%EC%82%B0-%EB%B2%94%EC%B2%9C5%EA%B5%AC%EC%97%AD-%EC%9E%AC%EA%B0%9C%EB%B0%9C%EC%A0%95%EB%B9%84%EC%82%AC%EC%97%85-%EC%88%98/" },
  { title:"아이에스동서, 대구 중구 '남산4-7구역' 재개발 수주", source:"뉴시스", date:"2026.07.28", url:"https://www.newsis.com/view/NISX20260728_0003725897" },
  { title:"울산 주택사업 승인 잇따라…집값 잡을 '단비' 될까", source:"울산매일", date:"2026.08월", url:"https://www.iusm.co.kr/news/articleView.html?idxno=1067424" },
  { title:"울산 중구 아파트 신축현장서 구조물 무너져…인부 3명 경상", source:"네이트뉴스", date:"2026.08.25", url:"https://news.nate.com/view/20260825n20635" },
  { title:"거제~마산·김해~밀양 도로사업 내년 본격화", source:"헤럴드경제", date:"2026년", url:"https://biz.heraldcorp.com/article/10632141" },
  { title:"대구·경북, 실물경기 회복 속 '부동산 디커플링'", source:"영남경제", date:"2026년", url:"https://www.ynenews.kr/news/articleView.html?idxno=76537" },
  { title:"'허리' 끊긴 부산 고용시장…제조·건설 동반 추락에 자영업만 '비대'", source:"네이트뉴스", date:"2026.05.13", url:"https://news.nate.com/view/20260513n14949" },
];

const NEWS_OTHER = [
  { title:"9월 수도권 분양 2만가구…서울은 244가구 그쳐", source:"헤럴드경제", url:"https://biz.heraldcorp.com/article/10858462" },
  { title:"9월 아파트 입주 30% 급감...10채 중 7채는 수도권 쏠림", source:"헤럴드경제", url:"https://biz.heraldcorp.com/article/10849444" },
  { title:"인천 내항 1·8부두 재개발, 2026년 말 착공 목표", source:"연합시민의소리", url:"https://cunews.net/detail.php?number=171646&thread=22r03r03+style%3D" },
  { title:"대전·충북 아파트값 상승… 세종 보합, 충남 하락", source:"중도일보", url:"https://m.joongdo.co.kr/view.php?key=20260809010002679" },
  { title:"호남 반도체 훈풍?…장기 침체 광주 부동산 시장 달아오른다", source:"파이낸셜뉴스", url:"https://www.fnnews.com/news/202608120730149940" },
  { title:"정부, 재개발·재건축 '착공까지' 관리 범위 확대", source:"뉴스토마토", url:"https://www.newstomato.com/ReadNews.aspx?no=1312214" },
  { title:"국토부, 서울·대전서 정비사업 설명회 개최", source:"파이낸셜뉴스", url:"https://www.fnnews.com/news/202608291342318756" },
];
