import logging
import langchain
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_ollama import ChatOllama

# TRACE > DEBUG > INFO > WARN > ERROR
logging.basicConfig(level=logging.DEBUG)
langchain.debug = True

@tool
def plus(a:int, b:int) -> int:
    """두 수를 더하는 도구 입니다."""
    return a + b

@tool
def minus(a:int, b:int) -> int:
    """두 수를 빼는 도구 입니다."""
    return a - b

@tool
def multiply(a:int, b:int) -> int:
    """두 수를 곱하는 도구 입니다."""
    return a * b

@tool
def devide(a:int, b:int) -> int:
    """두 수를 나누는 도구 입니다."""
    return int(a / b)


# 사용할 툴 등록
tools = [plus, minus, multiply, devide]
# 모델 불러오기(exaone은 tool을 인식할 수 없음) 따라서 llama3.1:latest를 설치
# ollama run llama3.1:latest

model = ChatOllama(model='llama3.1:latest', temperature=0)
agent = create_agent(model, tools)

# 질문 받기
messages = input("사칙연산시캬ㅂㅏ\n")
print('열심히계산중....,,')
resp = agent.invoke({'message': [('user', messages)]})
for i, msg in enumerate(resp['message']):
    print(f'{i}. {msg}')
print(f'최종 답변: {resp['message'][-1].content}')
