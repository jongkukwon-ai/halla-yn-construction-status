// 영업소 권역 날씨 — .github/scripts/update_weather.py가 매시간 자동 갱신 (기상청 단기예보)
const WEATHER = {
 "updated": "2026-11-05 23:20",
 "base": "11/05 23:00",
 "source": "기상청 단기예보",
 "regions": [
  {
   "office": "부산",
   "city": "부산",
   "days": [
    {
     "date": "2026-11-05",
     "label": "오늘",
     "dow": "목",
     "tmin": 14,
     "tmax": 19,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-06",
     "label": "내일",
     "dow": "금",
     "tmin": 9,
     "tmax": 15,
     "pop": 30,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-07",
     "label": "모레",
     "dow": "토",
     "tmin": 3,
     "tmax": 14,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-08",
     "label": "글피",
     "dow": "일",
     "tmin": 3,
     "tmax": 15,
     "pop": 30,
     "wx": "흐림",
     "icon": "☁️"
    }
   ]
  },
  {
   "office": "울산",
   "city": "울산",
   "days": [
    {
     "date": "2026-11-05",
     "label": "오늘",
     "dow": "목",
     "tmin": 12,
     "tmax": 17,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-06",
     "label": "내일",
     "dow": "금",
     "tmin": 8,
     "tmax": 14,
     "pop": 30,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-07",
     "label": "모레",
     "dow": "토",
     "tmin": 3,
     "tmax": 12,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-08",
     "label": "글피",
     "dow": "일",
     "tmin": 1,
     "tmax": 14,
     "pop": 30,
     "wx": "흐림",
     "icon": "☁️"
    }
   ]
  },
  {
   "office": "경남동부",
   "city": "창원",
   "days": [
    {
     "date": "2026-11-05",
     "label": "오늘",
     "dow": "목",
     "tmin": 12,
     "tmax": 17,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-06",
     "label": "내일",
     "dow": "금",
     "tmin": 9,
     "tmax": 15,
     "pop": 30,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-07",
     "label": "모레",
     "dow": "토",
     "tmin": 2,
     "tmax": 13,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-08",
     "label": "글피",
     "dow": "일",
     "tmin": 1,
     "tmax": 14,
     "pop": 30,
     "wx": "흐림",
     "icon": "☁️"
    }
   ]
  },
  {
   "office": "경남서부",
   "city": "진주",
   "days": [
    {
     "date": "2026-11-05",
     "label": "오늘",
     "dow": "목",
     "tmin": 11,
     "tmax": 18,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-06",
     "label": "내일",
     "dow": "금",
     "tmin": 8,
     "tmax": 15,
     "pop": 30,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-07",
     "label": "모레",
     "dow": "토",
     "tmin": 2,
     "tmax": 13,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-08",
     "label": "글피",
     "dow": "일",
     "tmin": 1,
     "tmax": 12,
     "pop": 30,
     "wx": "흐림",
     "icon": "☁️"
    }
   ]
  },
  {
   "office": "경북동부",
   "city": "포항",
   "days": [
    {
     "date": "2026-11-05",
     "label": "오늘",
     "dow": "목",
     "tmin": 10,
     "tmax": 16,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-06",
     "label": "내일",
     "dow": "금",
     "tmin": 8,
     "tmax": 15,
     "pop": 30,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-07",
     "label": "모레",
     "dow": "토",
     "tmin": 2,
     "tmax": 13,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-08",
     "label": "글피",
     "dow": "일",
     "tmin": 1,
     "tmax": 14,
     "pop": 30,
     "wx": "흐림",
     "icon": "☁️"
    }
   ]
  },
  {
   "office": "경북서부",
   "city": "대구",
   "days": [
    {
     "date": "2026-11-05",
     "label": "오늘",
     "dow": "목",
     "tmin": 9,
     "tmax": 14,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-06",
     "label": "내일",
     "dow": "금",
     "tmin": 7,
     "tmax": 12,
     "pop": 30,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-07",
     "label": "모레",
     "dow": "토",
     "tmin": 1,
     "tmax": 10,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-08",
     "label": "글피",
     "dow": "일",
     "tmin": 0,
     "tmax": 11,
     "pop": 30,
     "wx": "흐림",
     "icon": "☁️"
    }
   ]
  }
 ]
};
