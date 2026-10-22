// 영업소 권역 날씨 — .github/scripts/update_weather.py가 매시간 자동 갱신 (기상청 단기예보)
const WEATHER = {
 "updated": "2026-10-23 04:18",
 "base": "10/23 02:00",
 "source": "기상청 단기예보",
 "regions": [
  {
   "office": "부산",
   "city": "부산",
   "days": [
    {
     "date": "2026-10-23",
     "label": "오늘",
     "dow": "금",
     "tmin": 13,
     "tmax": 22,
     "pop": 30,
     "wx": "흐림",
     "icon": "☁️"
    },
    {
     "date": "2026-10-24",
     "label": "내일",
     "dow": "토",
     "tmin": 17,
     "tmax": 20,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-10-25",
     "label": "모레",
     "dow": "일",
     "tmin": 18,
     "tmax": 22,
     "pop": 80,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-10-26",
     "label": "글피",
     "dow": "월",
     "tmin": 18,
     "tmax": 22,
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
     "date": "2026-10-23",
     "label": "오늘",
     "dow": "금",
     "tmin": 12,
     "tmax": 22,
     "pop": 30,
     "wx": "흐림",
     "icon": "☁️"
    },
    {
     "date": "2026-10-24",
     "label": "내일",
     "dow": "토",
     "tmin": 15,
     "tmax": 19,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-10-25",
     "label": "모레",
     "dow": "일",
     "tmin": 17,
     "tmax": 22,
     "pop": 80,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-10-26",
     "label": "글피",
     "dow": "월",
     "tmin": 17,
     "tmax": 21,
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
     "date": "2026-10-23",
     "label": "오늘",
     "dow": "금",
     "tmin": 9,
     "tmax": 22,
     "pop": 30,
     "wx": "흐림",
     "icon": "☁️"
    },
    {
     "date": "2026-10-24",
     "label": "내일",
     "dow": "토",
     "tmin": 15,
     "tmax": 19,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-10-25",
     "label": "모레",
     "dow": "일",
     "tmin": 16,
     "tmax": 22,
     "pop": 80,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-10-26",
     "label": "글피",
     "dow": "월",
     "tmin": 17,
     "tmax": 22,
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
     "date": "2026-10-23",
     "label": "오늘",
     "dow": "금",
     "tmin": 8,
     "tmax": 21,
     "pop": 30,
     "wx": "흐림",
     "icon": "☁️"
    },
    {
     "date": "2026-10-24",
     "label": "내일",
     "dow": "토",
     "tmin": 13,
     "tmax": 18,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-10-25",
     "label": "모레",
     "dow": "일",
     "tmin": 15,
     "tmax": 22,
     "pop": 70,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-10-26",
     "label": "글피",
     "dow": "월",
     "tmin": 16,
     "tmax": 21,
     "pop": 30,
     "wx": "구름많음",
     "icon": "⛅"
    }
   ]
  },
  {
   "office": "경북동부",
   "city": "포항",
   "days": [
    {
     "date": "2026-10-23",
     "label": "오늘",
     "dow": "금",
     "tmin": 13,
     "tmax": 21,
     "pop": 30,
     "wx": "흐림",
     "icon": "☁️"
    },
    {
     "date": "2026-10-24",
     "label": "내일",
     "dow": "토",
     "tmin": 14,
     "tmax": 20,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-10-25",
     "label": "모레",
     "dow": "일",
     "tmin": 16,
     "tmax": 21,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-10-26",
     "label": "글피",
     "dow": "월",
     "tmin": 17,
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
     "date": "2026-10-23",
     "label": "오늘",
     "dow": "금",
     "tmin": 7,
     "tmax": 21,
     "pop": 30,
     "wx": "구름많음",
     "icon": "⛅"
    },
    {
     "date": "2026-10-24",
     "label": "내일",
     "dow": "토",
     "tmin": 13,
     "tmax": 18,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-10-25",
     "label": "모레",
     "dow": "일",
     "tmin": 15,
     "tmax": 21,
     "pop": 60,
     "wx": "비",
     "icon": "🌧️"
    },
    {
     "date": "2026-10-26",
     "label": "글피",
     "dow": "월",
     "tmin": 16,
     "tmax": 20,
     "pop": 30,
     "wx": "흐림",
     "icon": "☁️"
    }
   ]
  }
 ]
};
