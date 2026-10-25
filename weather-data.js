// 영업소 권역 날씨 — .github/scripts/update_weather.py가 매시간 자동 갱신 (기상청 단기예보)
const WEATHER = {
 "updated": "2026-10-25 15:17",
 "base": "10/25 14:00",
 "source": "기상청 단기예보",
 "regions": [
  {
   "office": "부산",
   "city": "부산",
   "days": [
    {
     "date": "2026-10-25",
     "label": "오늘",
     "dow": "일",
     "tmin": 17,
     "tmax": 21,
     "pop": 70,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-10-26",
     "label": "내일",
     "dow": "월",
     "tmin": 17,
     "tmax": 22,
     "pop": 70,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-10-27",
     "label": "모레",
     "dow": "화",
     "tmin": 14,
     "tmax": 20,
     "pop": 20,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-10-28",
     "label": "글피",
     "dow": "수",
     "tmin": 6,
     "tmax": 16,
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
     "date": "2026-10-25",
     "label": "오늘",
     "dow": "일",
     "tmin": 17,
     "tmax": 21,
     "pop": 70,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-10-26",
     "label": "내일",
     "dow": "월",
     "tmin": 17,
     "tmax": 21,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-10-27",
     "label": "모레",
     "dow": "화",
     "tmin": 13,
     "tmax": 19,
     "pop": 20,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-10-28",
     "label": "글피",
     "dow": "수",
     "tmin": 5,
     "tmax": 16,
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
     "date": "2026-10-25",
     "label": "오늘",
     "dow": "일",
     "tmin": 16,
     "tmax": 21,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-10-26",
     "label": "내일",
     "dow": "월",
     "tmin": 17,
     "tmax": 24,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-10-27",
     "label": "모레",
     "dow": "화",
     "tmin": 13,
     "tmax": 19,
     "pop": 30,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-10-28",
     "label": "글피",
     "dow": "수",
     "tmin": 5,
     "tmax": 15,
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
     "date": "2026-10-25",
     "label": "오늘",
     "dow": "일",
     "tmin": 16,
     "tmax": 19,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-10-26",
     "label": "내일",
     "dow": "월",
     "tmin": 16,
     "tmax": 23,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-10-27",
     "label": "모레",
     "dow": "화",
     "tmin": 12,
     "tmax": 19,
     "pop": 30,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-10-28",
     "label": "글피",
     "dow": "수",
     "tmin": 4,
     "tmax": 16,
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
     "date": "2026-10-25",
     "label": "오늘",
     "dow": "일",
     "tmin": 17,
     "tmax": 21,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-10-26",
     "label": "내일",
     "dow": "월",
     "tmin": 17,
     "tmax": 21,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-10-27",
     "label": "모레",
     "dow": "화",
     "tmin": 12,
     "tmax": 20,
     "pop": 30,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-10-28",
     "label": "글피",
     "dow": "수",
     "tmin": 3,
     "tmax": 16,
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
     "date": "2026-10-25",
     "label": "오늘",
     "dow": "일",
     "tmin": 15,
     "tmax": 20,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-10-26",
     "label": "내일",
     "dow": "월",
     "tmin": 14,
     "tmax": 22,
     "pop": 30,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-10-27",
     "label": "모레",
     "dow": "화",
     "tmin": 11,
     "tmax": 17,
     "pop": 30,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-10-28",
     "label": "글피",
     "dow": "수",
     "tmin": 2,
     "tmax": 14,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    }
   ]
  }
 ]
};
