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

    def get_forecast_region_from_location(self, location_name: str) -> str:
        """지역명을 기상청 예보 권역명으로 매핑합니다."""
        if "서울" in location_name:
            return "서울"
        if "인천" in location_name:
            return "인천"
        if "부산" in location_name:
            return "부산"
        if "대구" in location_name:
            return "대구"
        if "대전" in location_name:
            return "대전"
        if "광주" in location_name:
            return "광주"
        if "울산" in location_name:
            return "울산"
        if "세종" in location_name:
            return "세종"
        if "제주" in location_name:
            return "제주"
        
        if "충남" in location_name or "충청남도" in location_name:
            return "충남"
        if "충북" in location_name or "충청북도" in location_name:
            return "충북"
        if "전남" in location_name or "전라남도" in location_name:
            return "전남"
        if "전북" in location_name or "전라북도" in location_name or "전북특별자치도" in location_name:
            return "전북"
        if "경남" in location_name or "경상남도" in location_name:
            return "경남"
        if "경북" in location_name or "경상북도" in location_name:
            return "경북"
            
        if "강원" in location_name or "강원특별자치도" in location_name:
            yeongdong_cities = ["강릉", "동해", "삼척", "속초", "태백", "고성", "양양"]
            for city in yeongdong_cities:
                if city in location_name:
                    return "강원영동"
            return "강원영서"
            
        if "경기" in location_name or "경기도" in location_name:
            bukbu_cities = ["고양", "파주", "의정부", "양주", "포천", "동두천", "연천", "구리", "남양주", "가평"]
            for city in bukbu_cities:
                if city in location_name:
                    return "경기북부"
            return "경기남부"
            
        return "서울"

    def parse_air_quality_forecast(self, forecast_items: list, region: str, target_date: str) -> AirQualitySummary:
        """대기질 예보 응답 데이터를 파싱합니다."""
        if not forecast_items:
            return None
            
        formatted_date = target_date
        if len(target_date) == 8 and target_date.isdigit():
            formatted_date = f"{target_date[:4]}-{target_date[4:6]}-{target_date[6:8]}"
            
        pm10_grade = "알수없음"
        pm25_grade = "알수없음"
        
        found = False
        for item in forecast_items:
            inform_data = item.get("informData", "")
            if inform_data != formatted_date:
                continue
                
            inform_code = item.get("informCode", "")
            inform_grade_str = item.get("informGrade", "")
            
            region_grades = {}
            if inform_grade_str:
                parts = inform_grade_str.split(",")
                for part in parts:
                    if ":" in part:
                        r, g = part.split(":")
                        region_grades[r.strip()] = g.strip()
            
            grade = region_grades.get(region, "알수없음")
            
            if inform_code == "PM10":
                pm10_grade = grade
                found = True
            elif inform_code == "PM25":
                pm25_grade = grade
                found = True
                
        if not found:
            logger.warning(f"No air quality forecast found for target date: {formatted_date}")
            return None
            
        return AirQualitySummary(
            pm10_value="-",
            pm10_grade=pm10_grade,
            pm25_value="-",
            pm25_grade=pm25_grade
        )

