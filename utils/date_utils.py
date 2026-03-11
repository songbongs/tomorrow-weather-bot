"""
한국 시간 기준 날짜 유틸리티
"""
from datetime import datetime, timedelta
import pytz
from config import TIMEZONE

def get_seoul_time() -> datetime:
    tz = pytz.timezone(TIMEZONE)
    return datetime.now(tz)

def get_today_str() -> str:
    return get_seoul_time().strftime("%Y%m%d")

def get_tomorrow_str() -> str:
    tomorrow = get_seoul_time() + timedelta(days=1)
    return tomorrow.strftime("%Y%m%d")

def get_base_date_time_for_short_term():
    """
    단기예보용 base_date, base_time 계산
    단기예보는 0200, 0500, 0800, 1100, 1400, 1700, 2000, 2300 에 발표됩니다.
    발표 후 API 제공까지 약 10분 이상 소요될 수 있으므로, 보수적으로 최근 발표 시각을 찾습니다.
    """
    now = get_seoul_time()
    
    # KMA 단기예보 발표 시각
    # 0200, 0500, 0800, 1100, 1400, 1700, 2000, 2300
    base_times = ["0200", "0500", "0800", "1100", "1400", "1700", "2000", "2300"]
    
    current_time_int = int(now.strftime("%H%M"))
    
    # 02:10 이전이라면 전날 23:00 예보를 사용
    if current_time_int < 210:
        base_date = (now - timedelta(days=1)).strftime("%Y%m%d")
        base_time = "2300"
    else:
        base_date = now.strftime("%Y%m%d")
        base_time = "0200" # 기본값
        for bt in base_times:
            # 발표시간 + 10분(안전여유) 보다 현재 시간이 크면 해당 시간을 base_time으로 사용
            if current_time_int >= int(bt) + 10:
                base_time = bt
                
    return base_date, base_time

def get_base_date_time_for_today_minmax():
    """
    오늘의 TMX/TMN(일 최고·최저기온) 확보용 base_date, base_time 반환.
    0200 발표 예보에는 오늘 하루 전체의 TMX/TMN이 포함됩니다.
    새벽 02:10 이전이라면 전날 0200을 반환합니다.
    """
    now = get_seoul_time()
    current_time_int = int(now.strftime("%H%M"))

    if current_time_int < 210:
        base_date = (now - timedelta(days=1)).strftime("%Y%m%d")
    else:
        base_date = now.strftime("%Y%m%d")

    return base_date, "0200"
def format_date_korean(date_str: str) -> str:
    """YYYYMMDD -> YYYY.MM.DD (요일)"""
    dt = datetime.strptime(date_str, "%Y%m%d")
    weekdays = ["월", "화", "수", "목", "금", "토", "일"]
    weekday = weekdays[dt.weekday()]
    return f"{dt.year}.{dt.month:02d}.{dt.day:02d} ({weekday})"
