"""
날씨/공기질 비교 서비스
"""
from models import WeatherSummary, AirQualitySummary, CompareResult, LocationConfig
from services.clothing_advisor import ClothingAdvisor
from utils.logger import get_logger

logger = get_logger("compare_service")

class CompareService:
    def __init__(self):
        self.advisor = ClothingAdvisor()
        
    def compare(self, location: LocationConfig, today: WeatherSummary, tomorrow: WeatherSummary,
                tomorrow_air: AirQualitySummary) -> CompareResult:
        """오늘과 내일의 날씨 데이터를 비교하여 차이점과 행동 추천을 도출합니다."""
        
        def calc_diff(val_tomorrow, val_today):
            if val_tomorrow is not None and val_today is not None:
                return float(val_tomorrow) - float(val_today)
            return 0.0

        morning_diff = calc_diff(tomorrow.morning_temp, today.morning_temp)
        day_diff = calc_diff(tomorrow.day_temp, today.day_temp)
        evening_diff = calc_diff(tomorrow.evening_temp, today.evening_temp)
        max_diff = calc_diff(tomorrow.max_temp, today.max_temp)
        min_diff = calc_diff(tomorrow.min_temp, today.min_temp)
        
        result = CompareResult(
            location=location,
            today_weather=today,
            tomorrow_weather=tomorrow,
            tomorrow_air_quality=tomorrow_air,
            morning_diff=morning_diff,
            day_diff=day_diff,
            evening_diff=evening_diff,
            max_diff=max_diff,
            min_diff=min_diff,
            advisor_messages=[]
        )
        
        advisor_messages = self.advisor.get_advices(result)
        result.advisor_messages = advisor_messages
        
        return result

    def parse_air_quality(self, data: dict) -> AirQualitySummary:
        """AirKorea 응답 데이터를 파싱합니다."""
        if not data:
            return None
            
        def get_grade_str(grade):
            mapping = {"1": "좋음", "2": "보통", "3": "나쁨", "4": "매우나쁨"}
            return mapping.get(str(grade), "알수없음")
            
        return AirQualitySummary(
            pm10_value=data.get("pm10Value", "-"),
            pm10_grade=get_grade_str(data.get("pm10Grade", "")),
            pm25_value=data.get("pm25Value", "-"),
            pm25_grade=get_grade_str(data.get("pm25Grade", ""))
        )
