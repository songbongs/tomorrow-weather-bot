"""
날씨 비교 결과를 바탕으로 행동 지침(옷차림/추가 준비물) 추천
"""

class ClothingAdvisor:
    def get_advices(self, compare_result) -> list[str]:
        advices = []
        
        # 기온 비교 기준 멘트
        morning_diff = compare_result.morning_diff
        day_diff = compare_result.day_diff
        evening_diff = compare_result.evening_diff
        
        # 아침 기온 비교
        if morning_diff <= -3:
            advices.append("아침은 오늘보다 더 쌀쌀하니 겉옷을 준비하세요.")
        elif morning_diff >= 3:
            advices.append("아침은 오늘보다 덜 춥겠어요.")

        # 낮 기온 비교
        if day_diff >= 2:
            advices.append("낮에는 오늘보다 조금 더 가볍게 입어도 괜찮아요.")
        elif day_diff <= -2:
            advices.append("낮에도 쌀쌀할 수 있으니 따뜻하게 챙겨 입으세요.")

        # 저녁 기온 비교
        if evening_diff <= -2:
            advices.append("저녁에는 오늘보다 서늘할 수 있어요.")
            
        # 강수 여부
        tomorrow = compare_result.tomorrow_weather
        if tomorrow.pop >= 40 or tomorrow.pty > 0 or tomorrow.rn1 > 0:
            advices.append("우산을 챙기세요. (비/눈 예보 있음)")
            
        # 미세먼지
        air = compare_result.tomorrow_air_quality
        if air:
            if air.pm10_grade in ["나쁨", "매우나쁨"] or air.pm25_grade in ["나쁨", "매우나쁨"]:
                advices.append("마스크를 챙기세요. (공기질 나쁨 이상)")

        # 기본적인 조언이 없는 경우
        if not advices:
            advices.append("오늘과 비슷한 착장이면 충분할 것 같아요.")
            
        return advices
