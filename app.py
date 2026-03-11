"""
메인 애플리케이션 실행 파일 (진입점)
"""
import sys
from clients.kma_forecast_client import KmaForecastClient
from clients.airkorea_client import AirKoreaClient
from clients.telegram_client import TelegramClient
from services.location_service import LocationService
from services.weather_merge_service import WeatherMergeService
from services.compare_service import CompareService
from services.message_builder import MessageBuilder
from utils.date_utils import get_today_str, get_tomorrow_str, get_base_date_time_for_short_term
from utils.logger import get_logger

logger = get_logger("app")

def main():
    logger.info("Starting Tomorrow Weather Briefing Bot...")
    
    location_service = LocationService()
    locations = location_service.get_locations()
    
    if not locations:
        logger.error("No locations found to process. Exiting.")
        sys.exit(1)
        
    kma_client = KmaForecastClient()
    air_client = AirKoreaClient()
    telegram_client = TelegramClient()
    
    weather_merger = WeatherMergeService()
    compare_service = CompareService()
    message_builder = MessageBuilder()
    
    today_str = get_today_str()
    tomorrow_str = get_tomorrow_str()
    base_date, base_time = get_base_date_time_for_short_term()
    
    for loc in locations:
        try:
            logger.info(f"Processing location: {loc.name}")
            
            # 1. 기상청 단기예보 조회
            items = kma_client.get_forecast(loc.nx, loc.ny, base_date, base_time)
            
            # 2. 오늘 날씨 요약 추출
            today_weather = weather_merger.parse_forecast(today_str, True, items)
            
            # 3. 내일 날씨 요약 추출
            tomorrow_weather = weather_merger.parse_forecast(tomorrow_str, False, items)
            logger.info(f"[{loc.name}] 날씨 수집 완료")
            
            # 4. 내일 공기질 조회 (AirKorea)
            try:
                air_data = air_client.get_air_quality(loc.station)
                tomorrow_air = compare_service.parse_air_quality(air_data)
                logger.info(f"[{loc.name}] 공기질 수집 완료")
            except Exception as e:
                logger.warning(f"[{loc.name}] 공기질 데이터 수집 실패: {e}")
                tomorrow_air = None # fallback
                
            # 5. 비교 및 조언 생성
            compare_result = compare_service.compare(loc, today_weather, tomorrow_weather, tomorrow_air)
            
            # 6. 메시지 생성
            message = message_builder.build(compare_result)
            
            # 7. 텔레그램 발송
            telegram_client.send_message(message)
            logger.info(f"[성공] {loc.name} 텔레그램 발송 완료")
            
        except Exception as e:
            logger.error(f"[실패] {loc.name} 처리 중 오류 발생: {e}")
            # 한 지역이 실패해도 다른 지역은 계속 처리합니다.

    logger.info("Processing finished.")

if __name__ == "__main__":
    main()
