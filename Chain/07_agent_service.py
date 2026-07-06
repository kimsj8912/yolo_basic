from datetime import datetime

from langchain_core.tools import tool


@tool
def check_weather(location:str) -> str:
    """특정 지역의 현재 날씨를 확인하고 알려주는 도구"""
    print(f"{location} 지역 날씨 데이터 크롤링")
    return f'요청하신 지역인 {location}은/는 현재 비가 내리고 있습니다!!'

@tool
def check_stock() -> str:
    """현재 주가 정보를 API를 통해 불러와 확인하고 알려주는 도구"""
    print(f"네이버 주식 페이지 크롤링")
    return "오늘의 주식 시세입니다. 오르거나 내리거나 하겟죠머"


@tool
def now_data() -> str:
    """현재(오늘)의 날짜와 시간을 확인해주는 도구"""
    curr_datetime = datetime.now()
    formatted_datetime = curr_datetime.strftime("%Y-%m-%d")
    return formatted_datetime