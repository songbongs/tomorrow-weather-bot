"""
출력 문자열 포맷터
"""

def format_temp(temp: float) -> str:
    if temp is None:
        return "-"
    return f"{temp:.1f}°C"

def format_temp_diff(diff: float) -> str:
    if diff is None:
        return "-"
    if diff > 0:
        return f"오늘보다 {diff:.1f}도 높아요."
    elif diff < 0:
        return f"오늘보다 {abs(diff):.1f}도 낮아요."
    else:
        return "오늘과 비슷해요."
