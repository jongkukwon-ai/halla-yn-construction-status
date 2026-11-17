// 영업소 권역 날씨 — .github/scripts/update_weather.py가 매시간 자동 갱신 (기상청 단기예보)
const WEATHER = {
 "updated": "2026-11-17 11:20",
 "base": "11/17 11:00",
 "source": "기상청 단기예보",
 "regions": [
  {
   "office": "부산",
   "city": "부산",
   "days": [
    {
     "date": "2026-11-17",
     "label": "오늘",
     "dow": "화",
     "tmin": 12,
     "tmax": 18,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-18",
     "label": "내일",
     "dow": "수",
     "tmin": 10,
     "tmax": 14,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-19",
     "label": "모레",
     "dow": "목",
     "tmin": 2,
     "tmax": 9,
     "pop": 20,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-20",
     "label": "글피",
     "dow": "금",
     "tmin": 0,
     "tmax": 8,
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
     "date": "2026-11-17",
     "label": "오늘",
     "dow": "화",
     "tmin": 11,
     "tmax": 17,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-18",
     "label": "내일",
     "dow": "수",
     "tmin": 10,
     "tmax": 14,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-19",
     "label": "모레",
     "dow": "목",
     "tmin": 2,
     "tmax": 9,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-20",
     "label": "글피",
     "dow": "금",
     "tmin": 0,
     "tmax": 8,
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
     "date": "2026-11-17",
     "label": "오늘",
     "dow": "화",
     "tmin": 11,
     "tmax": 18,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-18",
     "label": "내일",
     "dow": "수",
     "tmin": 10,
     "tmax": 14,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-19",
     "label": "모레",
     "dow": "목",
     "tmin": 2,
     "tmax": 9,
     "pop": 20,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-20",
     "label": "글피",
     "dow": "금",
     "tmin": 0,
     "tmax": 8,
     "pop": 10,
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
     "date": "2026-11-17",
     "label": "오늘",
     "dow": "화",
     "tmin": 10,
     "tmax": 18,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-18",
     "label": "내일",
     "dow": "수",
     "tmin": 9,
     "tmax": 14,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-19",
     "label": "모레",
     "dow": "목",
     "tmin": 2,
     "tmax": 9,
     "pop": 20,
     "wx": "구름많음",
     "icon": "⛅"
    },
    {
     "date": "2026-11-20",
     "label": "글피",
     "dow": "금",
     "tmin": 0,
     "tmax": 8,
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
     "date": "2026-11-17",
     "label": "오늘",
     "dow": "화",
     "tmin": 11,
     "tmax": 17,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-18",
     "label": "내일",
     "dow": "수",
     "tmin": 9,
     "tmax": 14,
     "pop": 30,
     "wx": "흐림",
     "icon": "☁️"
    },
    {
     "date": "2026-11-19",
     "label": "모레",
     "dow": "목",
     "tmin": 1,
     "tmax": 8,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-20",
     "label": "글피",
     "dow": "금",
     "tmin": -1,
     "tmax": 7,
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
     "date": "2026-11-17",
     "label": "오늘",
     "dow": "화",
     "tmin": 9,
     "tmax": 16,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-18",
     "label": "내일",
     "dow": "수",
     "tmin": 8,
     "tmax": 12,
     "pop": 30,
     "wx": "흐림",
     "icon": "☁️"
    },
    {
     "date": "2026-11-19",
     "label": "모레",
     "dow": "목",
     "tmin": 0,
     "tmax": 7,
     "pop": 20,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-20",
     "label": "글피",
     "dow": "금",
     "tmin": -2,
     "tmax": 5,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    }
   ]
  }
 ]
};
