# 1. 저장소 준비
from typing import TypedDict, NotRequired, Dict
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama

class SupportState(TypedDict):
    query: NotRequired[str]
    department: NotRequired[str]
    response: NotRequired[str]


# 2. 모델 준비
llm = ChatOllama(
    base_url="http://localhost:11434",
    model="exaone3.5:7.8b",
    temperature=0,
)

# 3. 노드에 등록할 함수 준비
def analyzer_node(state: SupportState) -> Dict:
    """고객 문의를 받아서 어느 부서의 문의인지 분류해주는 노드"""

    print(f"--- 1. 고객 문의 분석중,,,")
    prompt = f"""
        당신은 고객 문의 분류 전문가 입니다.
        다음 고객의 문의를 분석하여 'billing' 또는 'technical' 중 하나로 대답해주세요.
        - billing: 결제, 요금, 환불, 청구, 영수증, 가격 관련 문의
        - technical: 기술적 문제, 오류, 버그, 네트워크 문제, 시스템 장애 관련 문의
        반드시 다른 설명이나 문장 없이 딱 한 단어 'billing' 또는 'technical'로만 대답하세요.
        [고객 문의]
        : {state['query']}
    """
    resp = llm.invoke(prompt)
    dept = resp.content.strip()

    if 'billing' in dept:
        dept = 'billing'
    elif 'technical' in dept or 'tech' in dept:
        dept = 'technical'
    
    print(f"✅ 고객 문의 분석 완료: {dept} 부서로 분류됨")

    return {'department': dept}

def billing_node(state: SupportState) -> Dict:
    """결제 관련 문의 답변을 생성하는 노드"""
    return {'response': f"결제 관련 문의에 대한 답변입니다. 고객님의 문의 사항: {state['query']}"}

def technical_node(state: SupportState) -> Dict:
    """기술적 문제 관련 문의 답변을 생성하는 노드"""
    return {'response': f"기술적 문제 관련 문의에 대한 답변입니다. 고객님의 문의 사항: {state['query']}"}

def route_by_department(state: SupportState) -> str:
    """부서에 따라 다음 노드로 라우팅하는 조건부 함수"""
    node_name = 'go_to_tech'

    if state.get('department') == 'billing':
        node_name = 'go_to_bill'
    elif state.get('department') == 'technical':
        node_name = 'go_to_tech'

    return node_name

# 1. 저장소 등록
wf = StateGraph(SupportState)

# 2. 노드 등록
wf.add_node("analyzer", analyzer_node)
wf.add_node("bill", billing_node)
wf.add_node("tech", technical_node)

# 3. 엣지 등록(조건부)
wf.set_entry_point("analyzer")
wf.add_conditional_edges(
    "analyzer",
    route_by_department,
    {
        "go_to_bill": "bill",
        "go_to_tech": "tech"
    }
)

# 어느 엣지로 오든지 종료
wf.add_edge("bill", END)
wf.add_edge("tech", END)

# 4. 컴파일
app = wf.compile()
# 5. 실행
query = input("고객 문의를 입력하세요: \n")
result = app.invoke({'query': query})
# print(result)
print("\n=== 최종 결과 ===")
print(f"유저 질문: {result['query']}")
print(f"분류된 부서: {result['department']}")
print(f"최종 답변: {result['response']}")