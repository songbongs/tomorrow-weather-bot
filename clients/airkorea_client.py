"""
AirKorea 미세먼지 API 클라이언트
"""
import requests
from config import AIRKOREA_SERVICE_KEY
from utils.retry import retry_request
from utils.logger import get_logger

logger = get_logger("airkorea_client")

class AirKoreaClient:
    BASE_URL = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty"
    FORECAST_URL = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMinuDustFrcstDspth"
    
    @retry_request(max_retries=3, delay=2.0)
    def get_air_quality(self, station_name: str) -> dict:
        """측정소명으로 미세먼지 데이터 조회"""
        params = {
            "serviceKey": AIRKOREA_SERVICE_KEY,
            "returnType": "json",
            "numOfRows": "1",
            "pageNo": "1",
            "stationName": station_name,
            "dataTerm": "DAILY",
            "ver": "1.0"
        }
        
        response = requests.get(self.BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("response", {}).get("header", {}).get("resultCode") != "00":
            error_msg = data.get("response", {}).get("header", {}).get("resultMsg", "Unknown Error")
            logger.error(f"AirKorea API Error: {error_msg}")
            raise ValueError(f"AirKorea API Error: {error_msg}")
            
        items = data.get("response", {}).get("body", {}).get("items", [])
        if not items:
            return {}
            
        return items[0]

    @retry_request(max_retries=3, delay=2.0)
    def get_air_quality_forecast(self, search_date: str) -> list:
        """대기질 예보 정보 조회"""
        formatted_date = search_date
        if len(search_date) == 8 and search_date.isdigit():
            formatted_date = f"{search_date[:4]}-{search_date[4:6]}-{search_date[6:8]}"
            
        params = {
            "serviceKey": AIRKOREA_SERVICE_KEY,
            "returnType": "json",
            "numOfRows": "100",
            "pageNo": "1",
            "searchDate": formatted_date,
            "ver": "1.1"
        }
        
        logger.info(f"Calling AirKorea Forecast API for date: {formatted_date}")
        response = requests.get(self.FORECAST_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("response", {}).get("header", {}).get("resultCode") != "00":
            error_msg = data.get("response", {}).get("header", {}).get("resultMsg", "Unknown Error")
            logger.error(f"AirKorea Forecast API Error: {error_msg}")
            raise ValueError(f"AirKorea Forecast API Error: {error_msg}")
            
        return data.get("response", {}).get("body", {}).get("items", [])

