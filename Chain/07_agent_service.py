from datetime import datetime

from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_ollama import ChatOllama


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


tools = [check_weather, check_stock, now_data]

# 모델 불러오기
model = ChatOllama(
    base_url="http://localhost:11434",
    model="llama3.2:3b",
    temperature=0,
)

system_prom = """
        당신은 도구를 사용할 수 있는 비서입니다.
        질문에 답하기 위해 도구를 필요하다면 사용하세요
        [출력 규칙 - 반드시 준수할 것]
        1. 최종 답변은 반드시 한글로만 작성하세요
        2. 도구의 결과를 바탕으로 한글 문장으로 답하세요
"""

agent = create_agent(model, tools, system_prompt=system_prom)

message = input("올라마 비서한테 날씨/주가지수/현재시간을 물어바바\n")

# resp = agent.stream({'messages': [('user', message)]}, stream_mode="updates")
# print(f"resp: {resp}")
# for chunk in resp:
#     print(f"chunk: {chunk}")
resp = agent.invoke(
    {"messages": [("user", message)]}
)

for msg in resp["messages"]:
    if isinstance(msg, ToolMessage):
        print(msg.content)
