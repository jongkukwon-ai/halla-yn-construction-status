// 영업소 권역 날씨 — .github/scripts/update_weather.py가 매시간 자동 갱신 (기상청 단기예보)
const WEATHER = {
 "updated": "2026-10-27 23:20",
 "base": "10/27 23:00",
 "source": "기상청 단기예보",
 "regions": [
  {
   "office": "부산",
   "city": "부산",
   "days": [
    {
     "date": "2026-10-27",
     "label": "오늘",
     "dow": "화",
     "tmin": 13,
     "tmax": 19,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-10-28",
     "label": "내일",
     "dow": "수",
     "tmin": 6,
     "tmax": 17,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-10-29",
     "label": "모레",
     "dow": "목",
     "tmin": 6,
     "tmax": 18,
     "pop": 30,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-10-30",
     "label": "글피",
     "dow": "금",
     "tmin": 12,
     "tmax": 21,
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
     "date": "2026-10-27",
     "label": "오늘",
     "dow": "화",
     "tmin": 12,
     "tmax": 19,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-10-28",
     "label": "내일",
     "dow": "수",
     "tmin": 5,
     "tmax": 15,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-10-29",
     "label": "모레",
     "dow": "목",
     "tmin": 4,
     "tmax": 18,
     "pop": 30,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-10-30",
     "label": "글피",
     "dow": "금",
     "tmin": 10,
     "tmax": 22,
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
     "date": "2026-10-27",
     "label": "오늘",
     "dow": "화",
     "tmin": 13,
     "tmax": 19,
     "pop": 20,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-10-28",
     "label": "내일",
     "dow": "수",
     "tmin": 5,
     "tmax": 15,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-10-29",
     "label": "모레",
     "dow": "목",
     "tmin": 4,
     "tmax": 17,
     "pop": 30,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-10-30",
     "label": "글피",
     "dow": "금",
     "tmin": 10,
     "tmax": 21,
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
     "date": "2026-10-27",
     "label": "오늘",
     "dow": "화",
     "tmin": 13,
     "tmax": 19,
     "pop": 30,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-10-28",
     "label": "내일",
     "dow": "수",
     "tmin": 3,
     "tmax": 16,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-10-29",
     "label": "모레",
     "dow": "목",
     "tmin": 2,
     "tmax": 16,
     "pop": 30,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-10-30",
     "label": "글피",
     "dow": "금",
     "tmin": 9,
     "tmax": 21,
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
     "date": "2026-10-27",
     "label": "오늘",
     "dow": "화",
     "tmin": 12,
     "tmax": 19,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-10-28",
     "label": "내일",
     "dow": "수",
     "tmin": 3,
     "tmax": 15,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-10-29",
     "label": "모레",
     "dow": "목",
     "tmin": 2,
     "tmax": 16,
     "pop": 30,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-10-30",
     "label": "글피",
     "dow": "금",
     "tmin": 8,
     "tmax": 22,
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
     "date": "2026-10-27",
     "label": "오늘",
     "dow": "화",
     "tmin": 12,
     "tmax": 17,
     "pop": 20,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-10-28",
     "label": "내일",
     "dow": "수",
     "tmin": 2,
     "tmax": 13,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-10-29",
     "label": "모레",
     "dow": "목",
     "tmin": 2,
     "tmax": 14,
     "pop": 30,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-10-30",
     "label": "글피",
     "dow": "금",
     "tmin": 8,
     "tmax": 20,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    }
   ]
  }
 ]
};
