from typing import TypedDict, Dict
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, END

# 1. 데이터 저장소 준비
class SimpleState(TypedDict):
    ori_query: str
    refined_query: str
    response: str

# 2. 모델 준비
llm = ChatOllama(
    base_url="http://localhost:11434",
    model="llama3.2:3b",
    temperature=0.3,
)

# 3. 노드에 등록할 함수 준비
def refine_text_node(state: SimpleState) -> Dict:
    """ 유저의 질문을 정중하고 명확하게 다듬는 노드"""
    print(f"유저의 질문을 정중하고 명확하게 다듬는중,,,")
    prompt = f"다음의 문장을 정중하고 명확한 질문 형태로 다듬어줘 {state['ori_query']}"
    res = llm.invoke(prompt)
    return {'refined_query': res.content.strip()}

def call_llm_node(state: SimpleState) -> Dict:
    """ 다듬어진 질문을 LLM에게 전달하여 최종 답변을 받는 노드"""
    print(f"다듬어진 질문을 LLM에게 전달하여 최종 답변을 받는중,,,")
    res = llm.invoke(state['refined_query'])
    return {'response': res.content}

# 4. 저장소 등록
work_flow = StateGraph(SimpleState)

# 5. 노드 등록
work_flow.add_node("refiner", refine_text_node)
work_flow.add_node("generator", call_llm_node)

# 6. 엣지 구성
work_flow.set_entry_point("refiner")
work_flow.add_edge("refiner", "generator")
work_flow.add_edge("generator", END)
