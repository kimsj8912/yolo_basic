from typing import TypedDict, Dict
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END

# 1. 데이터 저장소 준비
class SimpleState(TypedDict):
    ori_query: str
    refined_query: str
    response: str

# 2. 모델 준비
llm = ChatOllama(
    base_url="http://localhost:11434",
    model="exaone3.5:7.8b",
    temperature=0.3,
)

chain = llm | StrOutputParser()


# 3. 노드에 등록할 함수 준비
def refine_text_node(state: SimpleState) -> Dict:
    """ 유저의 질문을 정중하고 명확하게 다듬는 노드"""
    print(f"--- 1. 유저의 질문을 정중하고 명확하게 다듬는중,,,")
    prompt = f"""
            다음의 [유저의 문장]을 정중하고 명확한 질문 형태로 다듬어서 [출력 형식]을 준수하여 출력해
            [출력 형식 - 반드시 준수할 것]
            - 출력 형식은 다듬어진 질문 문장만 단독으로 출력하고 사족을 붙이지 마 
            [유저의 문장]
            : {state['ori_query']}"""
    res = llm.invoke(prompt)
    return {'refined_query': res.content.strip()}

def call_llm_node(state: SimpleState) -> Dict:
    """ 다듬어진 질문을 LLM에게 전달하여 최종 답변을 받는 노드"""
    print(f"--- 2. 다듬어진 질문을 LLM에게 전달하여 최종 답변을 받는중,,,")
    
    # llm.stream()을 사용
    # StrOutputParser를 거쳐 chunk 단위로
    res = chain.stream(state['refined_query'])
    
    full_response = ""
    
    for chunk in res:
        print(chunk, end="", flush=True)
        full_response += chunk
        
    print("\n===============여기까지 스트리밍이엇습니다============\n\n\n") # 스트리밍 종료선
    return {'response': full_response}

# 4. 저장소 등록
work_flow = StateGraph(SimpleState)

# 5. 노드 등록
work_flow.add_node("refiner", refine_text_node)
work_flow.add_node("generator", call_llm_node)

# 6. 엣지 구성
work_flow.set_entry_point("refiner")
work_flow.add_edge("refiner", "generator")
work_flow.add_edge("generator", END)


# 7. 컴파일 후 실행
app = work_flow.compile()

query = input("암거나 물어바바\n")

# 각 노드 별로 어떤 결과가 나오는 지를 알 수 있다
# for node in app.stream({'ori_query': query}, stream_mode="updates"):
#     for nade_name, output in node.items():
#         print(f"{nade_name}: {output["refined_query" if nade_name == "refiner" else "response"]}")

# print("=== 최종 결과 ===")
# print(f"유저 질문: {result['ori_query']}")
# print(f"1차 다듬어진 질문: {result['refined_query']}")
# print(f"최종 답변: {result['response']}")


### 실시간으로 표현하는 방법??
for node in app.stream({'ori_query': query}, stream_mode="messages"):
    print(node)
