"""
지역 정보 파싱 및 유효성 검사 서비스
"""
import json
from typing import List
from models import LocationConfig
from config import LOCATIONS, LOCATIONS_JSON
from utils.logger import get_logger

logger = get_logger("location_service")

class LocationService:
    def get_locations(self) -> List[LocationConfig]:
        """환경변수에서 지역 정보를 파싱합니다."""
        locations = []
        
        if LOCATIONS_JSON:
            try:
                data = json.loads(LOCATIONS_JSON)
                for item in data:
                    locations.append(LocationConfig(
                        name=item["name"],
                        nx=item["nx"],
                        ny=item["ny"],
                        station=item.get("station", item["name"].split()[-1]) # 기본값 처리
                    ))
                logger.info(f"Loaded {len(locations)} locations from LOCATIONS_JSON")
                return locations
            except Exception as e:
                logger.error(f"Failed to parse LOCATIONS_JSON: {e}")
                
        if LOCATIONS:
            # 단순 문자열 방식 (이름만 있는 경우 nx, ny, station은 기본값 채우거나 조회해야 하지만 MVP에서는 이름 기반 단순 파싱)
            # 여기서는 예시로 고정값이나 더미 값을 넣습니다. 실제 서비스 시에는 Geocoding API 연동이 필요할 수 있습니다.
            items = LOCATIONS.split(",")
            for item in items:
                name = item.strip().strip("'\"")
                if not name:
                    continue
                # JSON 방식 권장. 문자열 방식은 임시 더미 좌표 적용
                locations.append(LocationConfig(
                    name=name,
                    nx=60, # 기본 임시값
                    ny=127,
                    station=name.split()[-1]
                ))
            logger.info(f"Loaded {len(locations)} locations from LOCATIONS string")
            return locations
            
        logger.warning("No locations configured.")
        return locations
