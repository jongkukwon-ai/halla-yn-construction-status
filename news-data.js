// ══════════════════════════════════════════
// 건설뉴스 데이터 (영남지역 중심 + 그 외 지역)
// date는 반드시 "YYYY-MM-DD" 형식(ISO) — 최신순 정렬 및
// "최근 한 달만 표시" 필터링에 사용됩니다.
// 매일 자동 갱신됩니다 (Claude 예약 작업).
// ══════════════════════════════════════════
const NEWS_UPDATED = "2026-09-04";

const NEWS_YN = [
  { title:"광주 챔피언스시티 3000가구…울산서는 야음 뉴타운 1150가구", source:"한국경제", date:"2026-08-27", url:"https://www.hankyung.com/article/2026082759451" },
  { title:"울산 중구 아파트 신축현장서 구조물 무너져…인부 3명 경상", source:"네이트뉴스", date:"2026-08-25", url:"https://news.nate.com/view/20260825n20635" },
  { title:"동부건설, 센트레빌 아스테리움 거제 본격 분양", source:"경남신문", date:"2026-08-24", url:"http://www.knnews.co.kr/news/articleView.php?idxno=1547515" },
  { title:"울산 아파트 분양, 기대감은 100인데 공급은 '0'", source:"머니투데이", date:"2026-08-07", url:"https://v.daum.net/v/20260807001853548" },
  { title:"대구 8월 분양전망지수 꺾여…분양 기대감↓", source:"대구일보", date:"2026-08-01", url:"https://www.idaegu.com/news/articleView.html?idxno=664862" },
];

const NEWS_OTHER = [
  { title:"9월 수도권 분양 2만가구…서울은 244가구 그쳐", source:"헤럴드경제", date:"2026-08-31", url:"https://biz.heraldcorp.com/article/10858462" },
  { title:"국토부, 서울·대전서 정비사업 설명회 개최", source:"파이낸셜뉴스", date:"2026-08-29", url:"https://www.fnnews.com/news/202608291342318756" },
  { title:"9월 아파트 입주 30% 급감...10채 중 7채는 수도권 쏠림", source:"헤럴드경제", date:"2026-08-28", url:"https://biz.heraldcorp.com/article/10849444" },
  { title:"재건축·재개발 '속도전' 나선 정부…용적률 상향 빠져 사업성은 과제", source:"뉴스핌", date:"2026-08-14", url:"https://www.newspim.com/news/view/20260814000718" },
  { title:"호남 반도체 훈풍?…장기 침체 광주 부동산 시장 달아오른다", source:"파이낸셜뉴스", date:"2026-08-12", url:"https://www.fnnews.com/news/202608120730149940" },
  { title:"대전·충북 아파트값 상승… 세종 보합, 충남 하락", source:"중도일보", date:"2026-08-09", url:"https://m.joongdo.co.kr/view.php?key=20260809010002679" },
];
