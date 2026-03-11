"""
기상청 데이터 파싱 및 요약 생성 서비스
"""
from typing import List, Optional
from models import WeatherSummary
from utils.logger import get_logger

logger = get_logger("weather_merge_service")

class WeatherMergeService:
    def parse_forecast(self, target_date: str, is_today: bool, items: List[dict]) -> WeatherSummary:
        """기상청 단기예보 아이템에서 특정 날짜의 데이터를 추출하고 요약합니다."""
        
        max_temp: Optional[float] = None
        min_temp: Optional[float] = None
        pop: int = 0
        pty: int = 0
        rn1: float = 0.0
        
        morning_temp: Optional[float] = None
        day_temp: Optional[float] = None
        evening_temp: Optional[float] = None
        
        for item in items:
            fcst_date = item.get("fcstDate")
            if fcst_date != target_date:
                continue
                
            category = item.get("category")
            fcst_time = item.get("fcstTime")
            val = item.get("fcstValue", "")
            
            try:
                if category == "TMX": # 일 최고기온
                    max_temp = float(val)
                elif category == "TMN": # 일 최저기온
                    min_temp = float(val)
                elif category == "TMP": # 1시간 기온
                    temp_val = float(val)
                    if fcst_time == "0800":
                        morning_temp = temp_val
                    elif fcst_time == "1400":
                        day_temp = temp_val
                    elif fcst_time == "2000":
                        evening_temp = temp_val
                elif category == "POP": # 강수확률
                    pop = max(pop, int(val))
                elif category == "PTY": # 강수형태
                    if int(val) > 0:
                        pty = int(val)
                elif category == "PCP": # 1시간 강수량 (단기예보에서는 PCP)
                    if val != "강수없음" and val != "적설없음":
                        # "1.0mm" 같은 문자열에서 숫자 추출 (단순화)
                        num_str = ''.join(c for c in val if c.isdigit() or c == '.')
                        if num_str:
                            rn1 = max(rn1, float(num_str))
            except ValueError:
                continue

        # TMX/TMN이 없는 발표 시각일 경우, TMP의 최대/최소값을 대용으로 사용
        if max_temp is None or min_temp is None:
            temps = []
            for item in items:
                if item.get("fcstDate") == target_date and item.get("category") == "TMP":
                    try:
                        temps.append(float(item.get("fcstValue", "0")))
                    except:
                        pass
            if temps:
                if max_temp is None: max_temp = max(temps)
                if min_temp is None: min_temp = min(temps)

        return WeatherSummary(
            date_str=target_date,
            is_today=is_today,
            max_temp=max_temp,
            min_temp=min_temp,
            pop=pop,
            pty=pty,
            rn1=rn1,
            morning_temp=morning_temp,
            day_temp=day_temp,
            evening_temp=evening_temp
        )
