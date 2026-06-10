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
        tomorrow = compare_result.tomorrow_weather
        if tomorrow.morning_temp is not None:
            if tomorrow.morning_temp <= 5: # 추운 겨울 날씨
                if morning_diff <= -3:
                    advices.append("아침에 오늘보다 더 추워져요! 두꺼운 패딩 필수 ❄️")
                elif morning_diff >= 3:
                    advices.append("아침 기온이 오늘보다 오르지만, 여전히 추우니 따뜻하게 입으세요 🧣")
                else:
                    advices.append("아침에 꽤 쌀쌀해요! 겉옷 꼭 챙기세요 🧥")
            elif tomorrow.morning_temp >= 22: # 더운 여름 날씨
                if morning_diff >= 3:
                    advices.append("아침부터 오늘보다 더워요, 가벼운 옷차림이 좋습니다 ☀️")
            else: # 일반 날씨
                if morning_diff <= -3:
                    advices.append("아침에 꽤 쌀쌀해요! 겉옷 꼭 챙기세요 🧥")
                elif morning_diff >= 3:
                    advices.append("아침은 오늘보다 포근할 거예요 😊")

        # 낮 기온 비교
        if tomorrow.day_temp is not None:
            if tomorrow.day_temp <= 10: # 낮에도 추운 경우
                if day_diff <= -2:
                    advices.append("낮에도 오늘보다 기온이 내려가 쌀쌀해요 🧣")
                else:
                    advices.append("낮에도 쌀쌀하니 옷차림 든든히 하세요 🧥")
            elif tomorrow.day_temp >= 28: # 낮에 폭염/더운 경우
                if day_diff >= 2:
                    advices.append("낮에 오늘보다 더 더워집니다! 얇은 반팔 입으세요 👕")
                else:
                    advices.append("낮에는 더운 여름 날씨가 이어져요 ☀️")
            else: # 일반 날씨
                if day_diff >= 2:
                    advices.append("낮에는 좀 더 가볍게 입어도 괜찮아요 👍")
                elif day_diff <= -2:
                    advices.append("낮에도 쌀쌀하니 따뜻하게 입으세요 🧣")

        # 저녁 기온 비교
        if tomorrow.evening_temp is not None:
            if tomorrow.evening_temp <= 8:
                if evening_diff <= -2:
                    advices.append("저녁에는 오늘보다 훨씬 더 쌀쌀해져요 🧣")
                else:
                    advices.append("저녁에는 꽤 추워지니 도톰한 외투를 입으세요 🧥")
            else:
                if evening_diff <= -2:
                    advices.append("저녁엔 오늘보다 서늘해요, 겉옷 챙기세요!")
            
        # 강수 여부
        tomorrow = compare_result.tomorrow_weather
        if tomorrow.pop >= 40 or tomorrow.pty > 0 or tomorrow.rn1 > 0:
            advices.append("우산 챙기세요! ☂️ (비/눈 예보 있어요)")
            
        # 미세먼지
        air = compare_result.tomorrow_air_quality
        if air:
            if air.pm10_grade in ["나쁨", "매우나쁨"] or air.pm25_grade in ["나쁨", "매우나쁨"]:
                advices.append("마스크 챙기세요! 😷 (공기가 안 좋아요)")

        # 기본적인 조언이 없는 경우
        if not advices:
            advices.append("오늘이랑 비슷하게 입으면 딱이에요! 👌")
            
        return advices
