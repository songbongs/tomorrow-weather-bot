"""
기상청 초단기실황 API 클라이언트 (확장 가능 구조용)
"""
import requests
from config import KMA_SERVICE_KEY
from utils.retry import retry_request
from utils.logger import get_logger

logger = get_logger("kma_observation_client")

class KmaObservationClient:
    BASE_URL = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"
    
    @retry_request(max_retries=3, delay=2.0)
    def get_observation(self, nx: int, ny: int, base_date: str, base_time: str) -> dict:
        """초단기실황 데이터 조회"""
        params = {
            "serviceKey": KMA_SERVICE_KEY,
            "pageNo": "1",
            "numOfRows": "100",
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
            logger.warning(f"KMA Observation API Error: {error_msg}")
            # 실황은 필수 요소가 아닐 수 있으므로 예외 대신 빈 리스트 반환
            return []
            
        return data.get("response", {}).get("body", {}).get("items", {}).get("item", [])
