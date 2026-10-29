// 영업소 권역 날씨 — .github/scripts/update_weather.py가 매시간 자동 갱신 (기상청 단기예보)
const WEATHER = {
 "updated": "2026-10-30 00:20",
 "base": "10/29 23:00",
 "source": "기상청 단기예보",
 "regions": [
  {
   "office": "부산",
   "city": "부산",
   "days": [
    {
     "date": "2026-10-30",
     "label": "오늘",
     "dow": "금",
     "tmin": 12,
     "tmax": 21,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-10-31",
     "label": "내일",
     "dow": "토",
     "tmin": 10,
     "tmax": 21,
     "pop": 20,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-01",
     "label": "모레",
     "dow": "일",
     "tmin": 9,
     "tmax": 18,
     "pop": 30,
     "wx": "흐림",
     "icon": "☁️"
    },
    {
     "date": "2026-11-02",
     "label": "글피",
     "dow": "월",
     "tmin": 14,
     "tmax": 21,
     "pop": 80,
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
     "date": "2026-10-30",
     "label": "오늘",
     "dow": "금",
     "tmin": 11,
     "tmax": 21,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-10-31",
     "label": "내일",
     "dow": "토",
     "tmin": 8,
     "tmax": 20,
     "pop": 20,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-01",
     "label": "모레",
     "dow": "일",
     "tmin": 8,
     "tmax": 17,
     "pop": 30,
     "wx": "흐림",
     "icon": "☁️"
    },
    {
     "date": "2026-11-02",
     "label": "글피",
     "dow": "월",
     "tmin": 12,
     "tmax": 20,
     "pop": 70,
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
     "date": "2026-10-30",
     "label": "오늘",
     "dow": "금",
     "tmin": 10,
     "tmax": 21,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-10-31",
     "label": "내일",
     "dow": "토",
     "tmin": 8,
     "tmax": 20,
     "pop": 20,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-01",
     "label": "모레",
     "dow": "일",
     "tmin": 7,
     "tmax": 16,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-02",
     "label": "글피",
     "dow": "월",
     "tmin": 12,
     "tmax": 21,
     "pop": 70,
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
     "date": "2026-10-30",
     "label": "오늘",
     "dow": "금",
     "tmin": 9,
     "tmax": 20,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-10-31",
     "label": "내일",
     "dow": "토",
     "tmin": 7,
     "tmax": 20,
     "pop": 20,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-01",
     "label": "모레",
     "dow": "일",
     "tmin": 6,
     "tmax": 15,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-02",
     "label": "글피",
     "dow": "월",
     "tmin": 10,
     "tmax": 20,
     "pop": 70,
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
     "date": "2026-10-30",
     "label": "오늘",
     "dow": "금",
     "tmin": 9,
     "tmax": 21,
     "pop": 30,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-10-31",
     "label": "내일",
     "dow": "토",
     "tmin": 7,
     "tmax": 20,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-01",
     "label": "모레",
     "dow": "일",
     "tmin": 7,
     "tmax": 16,
     "pop": 30,
     "wx": "흐림",
     "icon": "☁️"
    },
    {
     "date": "2026-11-02",
     "label": "글피",
     "dow": "월",
     "tmin": 10,
     "tmax": 21,
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
     "date": "2026-10-30",
     "label": "오늘",
     "dow": "금",
     "tmin": 9,
     "tmax": 20,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-10-31",
     "label": "내일",
     "dow": "토",
     "tmin": 7,
     "tmax": 18,
     "pop": 0,
     "wx": "맑음",
     "icon": "☀️"
    },
    {
     "date": "2026-11-01",
     "label": "모레",
     "dow": "일",
     "tmin": 5,
     "tmax": 14,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-11-02",
     "label": "글피",
     "dow": "월",
     "tmin": 9,
     "tmax": 18,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    }
   ]
  }
 ]
};
