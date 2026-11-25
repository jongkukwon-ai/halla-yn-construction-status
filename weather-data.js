// 영업소 권역 날씨 — .github/scripts/update_weather.py가 매시간 자동 갱신 (기상청 단기예보)
const WEATHER = {
 "updated": "2026-11-26 05:20",
 "base": "11/26 05:00",
 "source": "기상청 단기예보",
 "regions": [
  {
   "office": "부산",
   "city": "부산",
   "days": [
    {
     "date": "2026-11-26",
     "label": "오늘",
     "dow": "목",
     "tmin": 4,
     "tmax": 16,
     "pop": 20,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-27",
     "label": "내일",
     "dow": "금",
     "tmin": 10,
     "tmax": 20,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-28",
     "label": "모레",
     "dow": "토",
     "tmin": 8,
     "tmax": 13,
     "pop": 20,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-29",
     "label": "글피",
     "dow": "일",
     "tmin": 2,
     "tmax": 11,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    }
   ]
  },
  {
   "office": "울산",
   "city": "울산",
   "days": [
    {
     "date": "2026-11-26",
     "label": "오늘",
     "dow": "목",
     "tmin": 2,
     "tmax": 17,
     "pop": 20,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-27",
     "label": "내일",
     "dow": "금",
     "tmin": 7,
     "tmax": 21,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-28",
     "label": "모레",
     "dow": "토",
     "tmin": 7,
     "tmax": 12,
     "pop": 20,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-29",
     "label": "글피",
     "dow": "일",
     "tmin": 1,
     "tmax": 11,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    }
   ]
  },
  {
   "office": "경남동부",
   "city": "창원",
   "days": [
    {
     "date": "2026-11-26",
     "label": "오늘",
     "dow": "목",
     "tmin": 2,
     "tmax": 16,
     "pop": 20,
     "wx": "구름많음",
     "icon": "⛅"
    },
    {
     "date": "2026-11-27",
     "label": "내일",
     "dow": "금",
     "tmin": 8,
     "tmax": 20,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-28",
     "label": "모레",
     "dow": "토",
     "tmin": 8,
     "tmax": 12,
     "pop": 30,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-29",
     "label": "글피",
     "dow": "일",
     "tmin": 1,
     "tmax": 11,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    }
   ]
  },
  {
   "office": "경남서부",
   "city": "진주",
   "days": [
    {
     "date": "2026-11-26",
     "label": "오늘",
     "dow": "목",
     "tmin": 1,
     "tmax": 16,
     "pop": 20,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-27",
     "label": "내일",
     "dow": "금",
     "tmin": 5,
     "tmax": 19,
     "pop": 20,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-28",
     "label": "모레",
     "dow": "토",
     "tmin": 5,
     "tmax": 12,
     "pop": 30,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-29",
     "label": "글피",
     "dow": "일",
     "tmin": 0,
     "tmax": 11,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    }
   ]
  },
  {
   "office": "경북동부",
   "city": "포항",
   "days": [
    {
     "date": "2026-11-26",
     "label": "오늘",
     "dow": "목",
     "tmin": 1,
     "tmax": 16,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-27",
     "label": "내일",
     "dow": "금",
     "tmin": 4,
     "tmax": 21,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-28",
     "label": "모레",
     "dow": "토",
     "tmin": 8,
     "tmax": 12,
     "pop": 20,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-29",
     "label": "글피",
     "dow": "일",
     "tmin": 1,
     "tmax": 11,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    }
   ]
  },
  {
   "office": "경북서부",
   "city": "대구",
   "days": [
    {
     "date": "2026-11-26",
     "label": "오늘",
     "dow": "목",
     "tmin": 0,
     "tmax": 15,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-27",
     "label": "내일",
     "dow": "금",
     "tmin": 5,
     "tmax": 18,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-28",
     "label": "모레",
     "dow": "토",
     "tmin": 7,
     "tmax": 10,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-29",
     "label": "글피",
     "dow": "일",
     "tmin": 0,
     "tmax": 9,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    }
   ]
  }
 ]
};
