from typing import TypedDict, Dict
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from typing_extensions import Annotated
from langchain_ollama import ChatOllama
from langchain_core.tools import tool

# 1. 저장소 정의
class AgentState(TypedDict):
    # [데이터 타입, 규칙]
    # Lang graph는 메시지를 덮어쓰는 것을 기본으로 하고 있다
    # Annotation을 사용하여 특정한 데이터 타입에 특정한 규칙(메시지 추가)을 명시한 것
    # 어노테이션: 컴파일러에게 미리 힌트를 주는 개념
    messages: Annotated[list[BaseMessage], add_messages]

# 모델 정의
llm = ChatOllama(
    base_url="http://localhost:11434",
    model="exaone3.5:7.8b",
    temperature=0.3,
)

# 툴 등록
@tool
def multiply(a: int, b: int) -> int:
    """
    두 정수를 곱하는 계산기 도구입니다. 곱셈이 필요할 때 이 도구를 사용하세요
    
    Args:
        :param a (int): 곱셈에 사용할 첫 번째 정수
        :param b (int): 곱셈에 사용할 두 번째 정수
    returns:
        a와 b의 곱셈 결과를 반환합니다.
    
    """
    print(f"--- {a} * {b}를 하는 도구 실행 ---")
    return a * b

# 모델에 툴 추가
tools = [multiply]
model = llm.bind_tools(tools)


# 2. 노드 정의
def agent_node(state: AgentState) -> Dict:
    """사용자의 질문을 받아 응답을 하는 노드"""
    print(f"💭 사용자 메시지 분석 및 다음 행동 결정 중...")
    resp = model.invoke(state["messages"])
    """
    HumanMessage: 사용자 메시지(content)
    AIMessage: LLM이 생성한 응답 메시지(content, tool_calls)
    ToolMessage: tool이 수행 후 반환하는 메시지(content, tool_call_id)
    """
    return {"messages": [resp]}

def tool_node(state: AgentState) -> Dict:
    """에이전트 요청에 따라 필요한 툴을 실행하는 노드"""
    # 가장 마지막 메시지 추출
    # 거기서 필요한 툴 내역을 가져옴(tool_calls)
    # 해당 툴을 호출한다.
    # 툴 실행 후 반환받은 값을 전달
    resp = model.invoke(state["messages"])
    return {"messages": [resp]}


# 3. 라우터 정의

# 4. tool 등록


# 5. 저장소 등록

# 6. 노드 등록

# 7. 엣지 구성


# 8. 컴파일 후 실행