// 영업소 권역 날씨 — .github/scripts/update_weather.py가 매시간 자동 갱신 (기상청 단기예보)
const WEATHER = {
 "updated": "2026-11-08 03:20",
 "base": "11/08 02:00",
 "source": "기상청 단기예보",
 "regions": [
  {
   "office": "부산",
   "city": "부산",
   "days": [
    {
     "date": "2026-11-08",
     "label": "오늘",
     "dow": "일",
     "tmin": 4,
     "tmax": 14,
     "pop": 30,
     "wx": "흐림",
     "icon": "☁️"
    },
    {
     "date": "2026-11-09",
     "label": "내일",
     "dow": "월",
     "tmin": 10,
     "tmax": 13,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-10",
     "label": "모레",
     "dow": "화",
     "tmin": 8,
     "tmax": 15,
     "pop": 30,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-11",
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
   "office": "울산",
   "city": "울산",
   "days": [
    {
     "date": "2026-11-08",
     "label": "오늘",
     "dow": "일",
     "tmin": 2,
     "tmax": 15,
     "pop": 30,
     "wx": "흐림",
     "icon": "☁️"
    },
    {
     "date": "2026-11-09",
     "label": "내일",
     "dow": "월",
     "tmin": 9,
     "tmax": 14,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-10",
     "label": "모레",
     "dow": "화",
     "tmin": 9,
     "tmax": 15,
     "pop": 30,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-11",
     "label": "글피",
     "dow": "수",
     "tmin": 3,
     "tmax": 17,
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
     "date": "2026-11-08",
     "label": "오늘",
     "dow": "일",
     "tmin": 1,
     "tmax": 13,
     "pop": 30,
     "wx": "흐림",
     "icon": "☁️"
    },
    {
     "date": "2026-11-09",
     "label": "내일",
     "dow": "월",
     "tmin": 8,
     "tmax": 13,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-10",
     "label": "모레",
     "dow": "화",
     "tmin": 5,
     "tmax": 15,
     "pop": 30,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-11",
     "label": "글피",
     "dow": "수",
     "tmin": 2,
     "tmax": 16,
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
     "date": "2026-11-08",
     "label": "오늘",
     "dow": "일",
     "tmin": 3,
     "tmax": 13,
     "pop": 30,
     "wx": "흐림",
     "icon": "☁️"
    },
    {
     "date": "2026-11-09",
     "label": "내일",
     "dow": "월",
     "tmin": 9,
     "tmax": 13,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-10",
     "label": "모레",
     "dow": "화",
     "tmin": 5,
     "tmax": 15,
     "pop": 30,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-11",
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
   "office": "경북동부",
   "city": "포항",
   "days": [
    {
     "date": "2026-11-08",
     "label": "오늘",
     "dow": "일",
     "tmin": 0,
     "tmax": 15,
     "pop": 30,
     "wx": "흐림",
     "icon": "☁️"
    },
    {
     "date": "2026-11-09",
     "label": "내일",
     "dow": "월",
     "tmin": 7,
     "tmax": 15,
     "pop": 30,
     "wx": "흐림",
     "icon": "☁️"
    },
    {
     "date": "2026-11-10",
     "label": "모레",
     "dow": "화",
     "tmin": 9,
     "tmax": 15,
     "pop": 20,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-11",
     "label": "글피",
     "dow": "수",
     "tmin": 4,
     "tmax": 17,
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
     "date": "2026-11-08",
     "label": "오늘",
     "dow": "일",
     "tmin": 1,
     "tmax": 12,
     "pop": 30,
     "wx": "흐림",
     "icon": "☁️"
    },
    {
     "date": "2026-11-09",
     "label": "내일",
     "dow": "월",
     "tmin": 7,
     "tmax": 13,
     "pop": 30,
     "wx": "흐림",
     "icon": "☁️"
    },
    {
     "date": "2026-11-10",
     "label": "모레",
     "dow": "화",
     "tmin": 4,
     "tmax": 15,
     "pop": 30,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-11",
     "label": "글피",
     "dow": "수",
     "tmin": 3,
     "tmax": 16,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    }
   ]
  }
 ]
};
