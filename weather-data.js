// 영업소 권역 날씨 — .github/scripts/update_weather.py가 매시간 자동 갱신 (기상청 단기예보)
const WEATHER = {
 "updated": "2026-11-01 02:20",
 "base": "11/01 02:00",
 "source": "기상청 단기예보",
 "regions": [
  {
   "office": "부산",
   "city": "부산",
   "days": [
    {
     "date": "2026-11-01",
     "label": "오늘",
     "dow": "일",
     "tmin": 8,
     "tmax": 18,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-02",
     "label": "내일",
     "dow": "월",
     "tmin": 14,
     "tmax": 21,
     "pop": 80,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-03",
     "label": "모레",
     "dow": "화",
     "tmin": 8,
     "tmax": 19,
     "pop": 20,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-04",
     "label": "글피",
     "dow": "수",
     "tmin": 10,
     "tmax": 19,
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
     "date": "2026-11-01",
     "label": "오늘",
     "dow": "일",
     "tmin": 7,
     "tmax": 17,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-02",
     "label": "내일",
     "dow": "월",
     "tmin": 12,
     "tmax": 19,
     "pop": 70,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-03",
     "label": "모레",
     "dow": "화",
     "tmin": 7,
     "tmax": 18,
     "pop": 20,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-04",
     "label": "글피",
     "dow": "수",
     "tmin": 8,
     "tmax": 19,
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
     "date": "2026-11-01",
     "label": "오늘",
     "dow": "일",
     "tmin": 7,
     "tmax": 16,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-02",
     "label": "내일",
     "dow": "월",
     "tmin": 12,
     "tmax": 20,
     "pop": 70,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-03",
     "label": "모레",
     "dow": "화",
     "tmin": 6,
     "tmax": 18,
     "pop": 20,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-04",
     "label": "글피",
     "dow": "수",
     "tmin": 8,
     "tmax": 18,
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
     "date": "2026-11-01",
     "label": "오늘",
     "dow": "일",
     "tmin": 6,
     "tmax": 14,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-02",
     "label": "내일",
     "dow": "월",
     "tmin": 10,
     "tmax": 20,
     "pop": 70,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-03",
     "label": "모레",
     "dow": "화",
     "tmin": 5,
     "tmax": 19,
     "pop": 20,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-04",
     "label": "글피",
     "dow": "수",
     "tmin": 7,
     "tmax": 18,
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
     "date": "2026-11-01",
     "label": "오늘",
     "dow": "일",
     "tmin": 5,
     "tmax": 16,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-02",
     "label": "내일",
     "dow": "월",
     "tmin": 11,
     "tmax": 20,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-03",
     "label": "모레",
     "dow": "화",
     "tmin": 4,
     "tmax": 19,
     "pop": 20,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-04",
     "label": "글피",
     "dow": "수",
     "tmin": 5,
     "tmax": 19,
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
     "date": "2026-11-01",
     "label": "오늘",
     "dow": "일",
     "tmin": 5,
     "tmax": 12,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-02",
     "label": "내일",
     "dow": "월",
     "tmin": 9,
     "tmax": 17,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-03",
     "label": "모레",
     "dow": "화",
     "tmin": 4,
     "tmax": 17,
     "pop": 20,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-04",
     "label": "글피",
     "dow": "수",
     "tmin": 6,
     "tmax": 17,
     "pop": 30,
     "wx": "흐림",
     "icon": "☁️"
    }
   ]
  }
 ]
};
