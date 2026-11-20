// 영업소 권역 날씨 — .github/scripts/update_weather.py가 매시간 자동 갱신 (기상청 단기예보)
const WEATHER = {
 "updated": "2026-11-21 02:20",
 "base": "11/21 02:00",
 "source": "기상청 단기예보",
 "regions": [
  {
   "office": "부산",
   "city": "부산",
   "days": [
    {
     "date": "2026-11-21",
     "label": "오늘",
     "dow": "토",
     "tmin": 0,
     "tmax": 9,
     "pop": 20,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-22",
     "label": "내일",
     "dow": "일",
     "tmin": -1,
     "tmax": 9,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-23",
     "label": "모레",
     "dow": "월",
     "tmin": 1,
     "tmax": 13,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-24",
     "label": "글피",
     "dow": "화",
     "tmin": 5,
     "tmax": 8,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    }
   ]
  },
  {
   "office": "울산",
   "city": "울산",
   "days": [
    {
     "date": "2026-11-21",
     "label": "오늘",
     "dow": "토",
     "tmin": -2,
     "tmax": 8,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-22",
     "label": "내일",
     "dow": "일",
     "tmin": -2,
     "tmax": 8,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-23",
     "label": "모레",
     "dow": "월",
     "tmin": -1,
     "tmax": 14,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-24",
     "label": "글피",
     "dow": "화",
     "tmin": 4,
     "tmax": 8,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    }
   ]
  },
  {
   "office": "경남동부",
   "city": "창원",
   "days": [
    {
     "date": "2026-11-21",
     "label": "오늘",
     "dow": "토",
     "tmin": -1,
     "tmax": 8,
     "pop": 20,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-22",
     "label": "내일",
     "dow": "일",
     "tmin": -2,
     "tmax": 8,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-23",
     "label": "모레",
     "dow": "월",
     "tmin": -1,
     "tmax": 13,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-24",
     "label": "글피",
     "dow": "화",
     "tmin": 5,
     "tmax": 8,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    }
   ]
  },
  {
   "office": "경남서부",
   "city": "진주",
   "days": [
    {
     "date": "2026-11-21",
     "label": "오늘",
     "dow": "토",
     "tmin": -1,
     "tmax": 9,
     "pop": 20,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-22",
     "label": "내일",
     "dow": "일",
     "tmin": -3,
     "tmax": 9,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-23",
     "label": "모레",
     "dow": "월",
     "tmin": -2,
     "tmax": 13,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-24",
     "label": "글피",
     "dow": "화",
     "tmin": 5,
     "tmax": 9,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    }
   ]
  },
  {
   "office": "경북동부",
   "city": "포항",
   "days": [
    {
     "date": "2026-11-21",
     "label": "오늘",
     "dow": "토",
     "tmin": -2,
     "tmax": 7,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-22",
     "label": "내일",
     "dow": "일",
     "tmin": -3,
     "tmax": 8,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-23",
     "label": "모레",
     "dow": "월",
     "tmin": -2,
     "tmax": 13,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-24",
     "label": "글피",
     "dow": "화",
     "tmin": 4,
     "tmax": 7,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    }
   ]
  },
  {
   "office": "경북서부",
   "city": "대구",
   "days": [
    {
     "date": "2026-11-21",
     "label": "오늘",
     "dow": "토",
     "tmin": -3,
     "tmax": 5,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-22",
     "label": "내일",
     "dow": "일",
     "tmin": -4,
     "tmax": 6,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-23",
     "label": "모레",
     "dow": "월",
     "tmin": -3,
     "tmax": 11,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-24",
     "label": "글피",
     "dow": "화",
     "tmin": 1,
     "tmax": 6,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    }
   ]
  }
 ]
};
