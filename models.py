"""
데이터 구조 정의
"""
from dataclasses import dataclass
from typing import Optional, List, Dict, Any

@dataclass
class LocationConfig:
    name: str
    nx: int
    ny: int
    station: str

@dataclass
class WeatherSummary:
    date_str: str  # YYYYMMDD
    is_today: bool
    max_temp: Optional[float]
    min_temp: Optional[float]
    pop: int  # 강수확률
    pty: int  # 강수형태 (0: 없음, 1: 비, 2: 비/눈, 3: 눈, 4: 소나기)
    rn1: float # 예상 강수량 (문자열 파싱을 통해 숫자로 변환)
    morning_temp: Optional[float] # 08시 기온
    day_temp: Optional[float]     # 14시 기온
    evening_temp: Optional[float] # 20시 기온

@dataclass
class AirQualitySummary:
    pm10_value: str
    pm10_grade: str
    pm25_value: str
    pm25_grade: str

@dataclass
class CompareResult:
    location: LocationConfig
    today_weather: WeatherSummary
    tomorrow_weather: WeatherSummary
    tomorrow_air_quality: Optional[AirQualitySummary]
    
    # 비교 수치 (내일 - 오늘)
    morning_diff: float
    day_diff: float
    evening_diff: float
    max_diff: float
    min_diff: float
    
    # 안내 문구 (의상/행동 추천)
    advisor_messages: List[str]
