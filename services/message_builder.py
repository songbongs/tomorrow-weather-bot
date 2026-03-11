"""
결과 모델을 텔레그램 메시지로 변환하는 빌더
"""
from models import CompareResult
from utils.date_utils import format_date_korean
from utils.formatters import format_temp, format_temp_diff

class MessageBuilder:
    def build(self, result: CompareResult) -> str:
        loc_name = result.location.name
        
        today = result.today_weather
        tomorrow = result.tomorrow_weather
        air = result.tomorrow_air_quality
        
        lines = []
        lines.append(f"📍 <b>{loc_name}</b>\n")
        
        # 오늘 날씨
        lines.append(f"📅 <b>오늘 ({format_date_korean(today.date_str)})</b>")
        lines.append(f"🌡️ 최고: {format_temp(today.max_temp)} / 최저: {format_temp(today.min_temp)}")
        lines.append(f"💧 강수량: {today.rn1}mm (확률: {today.pop}%)\n")
        
        # 내일 날씨
        lines.append(f"📅 <b>내일 ({format_date_korean(tomorrow.date_str)})</b>")
        lines.append(f"🌡️ 최고: {format_temp(tomorrow.max_temp)} / 최저: {format_temp(tomorrow.min_temp)}")
        lines.append(f"💧 강수량: {tomorrow.rn1}mm (확률: {tomorrow.pop}%)")
        
        if air:
            lines.append(f"🔹 미세먼지: 미세({air.pm10_grade}/{air.pm10_value}), 초미세({air.pm25_grade}/{air.pm25_value})\n")
        else:
            lines.append("🔹 미세먼지: 정보 없음\n")
            
        # 비교 부분
        lines.append("🗣️ <b>오늘 vs 내일 비교</b>")
        lines.append(f"🔹 아침 기온: {format_temp_diff(result.morning_diff)}")
        lines.append(f"🔹 낮 기온: {format_temp_diff(result.day_diff)}")
        lines.append(f"🔹 저녁 기온: {format_temp_diff(result.evening_diff)}")
        
        for adv in result.advisor_messages:
            lines.append(f"🔹 {adv}")
            
        return "\n".join(lines)
