// ══════════════════════════════════════════
// 건설뉴스 데이터 (영남지역 중심 + 그 외 지역)
// date는 반드시 "YYYY-MM-DD" 형식(ISO) — 최신순 정렬 및
// "최근 한 달만 표시" 필터링에 사용됩니다.
// 매일 자동 갱신됩니다 (Claude 예약 작업).
// ══════════════════════════════════════════
const NEWS_UPDATED = "2026-09-04";

const NEWS_YN = [
  { title:"대구시, 달서천 5구역 BTL사업 우선협상대상자 지정…2028년 착공", source:"매일신문", date:"2026-09-03", url:"https://www.imaeil.com/page/view/2026090317295320389" },
  { title:"전세 매물 마른 진주…'판문지구 레이크써밋 웰가' 9월 분양", source:"서울경제TV", date:"2026-09-01", url:"https://www.sentv.co.kr/article/view/sentv202609010090" },
  { title:"부산 동래구 시공사 선정 줄 잇는다", source:"대한경제", date:"2026-09-01", url:"https://www.dnews.co.kr/uhtml/view.jsp?idxno=202509011527098570873" },
  { title:"'6개월 새 8000만원↑'…교통망 확충에 양산 물금 부동산 '꿈틀'", source:"머니투데이", date:"2026-08-31", url:"https://www.mt.co.kr/estate/2026/08/31/2026083110581385472" },
  { title:"대구 7월 아파트 분양 '제로'…착공도 96% 급감", source:"매일신문", date:"2026-08-29", url:"https://www.imaeil.com/page/view/2026082919041533886" },
  { title:"에스엔시스, 부산 제2공장 신설 추진", source:"뉴스핌", date:"2026-08-27", url:"https://www.newspim.com/news/view/20260827000180" },
  { title:"울산 입주 물량 감소… '그랑라크 에일린의 뜰' 분양", source:"뉴스핌", date:"2026-08-19", url:"https://www.newspim.com/news/view/20260819000943" },
  { title:"GS건설, 4082억 규모 부산 사직3구역 재개발 본계약", source:"아주경제", date:"2026-08-07", url:"https://www.ajunews.com/view/20260807173907679" },
];

const NEWS_OTHER = [
  { title:"9월 가을분양 성수기...다음주 1021가구 분양 돌입", source:"파이낸셜뉴스", date:"2026-09-04", url:"https://www.fnnews.com/news/202609041519343392" },
  { title:"전남광주 매머드급 '올 뉴 챔피언스시티 1차' 분양...3216가구 규모", source:"뉴스핌", date:"2026-09-02", url:"https://www.newspim.com/news/view/20260902001139" },
  { title:"[주간 AI 부동산] 서울 그린벨트 풀리나…7.3만가구 신규택지에 쏠린 눈", source:"뉴스핌", date:"2026-08-21", url:"https://www.newspim.com/news/view/20260821000910" },
  { title:"[르포] 메탄 연기 뿜던 공장터, 반도체 도시로…청주 부동산 '상전벽해'", source:"뉴스핌", date:"2026-08-18", url:"https://www.newspim.com/news/view/20260818001015" },
  { title:"[AI 부동산 투데이] 치솟는 아파트 분양가…서울 '국평' 19억 넘겼다", source:"뉴스핌", date:"2026-08-10", url:"https://www.newspim.com/news/view/20260810001268" },
  { title:"[분양캘린더] 김포 한강푸르지오리버프론트 등 3284가구 분양", source:"뉴스핌", date:"2026-08-07", url:"https://www.newspim.com/news/view/20260807001028" },
];
