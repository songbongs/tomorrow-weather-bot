"""
기상청 단기예보 API 클라이언트
"""
import requests
from config import KMA_SERVICE_KEY
from utils.retry import retry_request
from utils.logger import get_logger

logger = get_logger("kma_forecast_client")

class KmaForecastClient:
    BASE_URL = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
    
    @retry_request(max_retries=3, delay=2.0)
    def get_forecast(self, nx: int, ny: int, base_date: str, base_time: str) -> dict:
        """단기예보 데이터 조회"""
        params = {
            "serviceKey": KMA_SERVICE_KEY,
            "pageNo": "1",
            "numOfRows": "1000",
            "dataType": "JSON",
            "base_date": base_date,
            "base_time": base_time,
            "nx": nx,
            "ny": ny
        }
        
        response = requests.get(self.BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("response", {}).get("header", {}).get("resultCode") != "00":
            error_msg = data.get("response", {}).get("header", {}).get("resultMsg", "Unknown Error")
            logger.error(f"KMA API Error: {error_msg}")
            raise ValueError(f"KMA API Error: {error_msg}")
            
        return data.get("response", {}).get("body", {}).get("items", {}).get("item", [])
