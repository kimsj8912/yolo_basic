# 1. 저장소 생성
from typing import TypedDict, NotRequired, Dict
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama
import json


class WritingState(TypedDict):
    topic:str   # 글의 주제
    draft:str   # 글의 초안
    feedback:str   # 피드백
    status:str   # 통과(PASS), 재시도(RETRY)
    count:int   # 시도 횟수(일정 횟수가 넘으면 중지 할 수 있도록)

# 2. 모델 호출
model = ChatOllama(
    base_url="http://localhost:11434", 
    model="exaone3.5:7.8b", 
    temperature=1.6
    )

# 3. 노드에 등록할 함수 준비
def writer_node(state: WritingState) -> Dict:
    """주제에 맞는 글을 작성하는 노드"""

    # 내부 변수로 현재 상태의 count를 가져옴
    current_count = state.get('count', 0)

    if not state['draft']:  # draft가 없으면 글을 작성
        print(f"--- 1. 주제에 맞는 초안을 작성하는중,,,")
        prompt = f"""
            당신은 간결하고 멋진 광고 카피를 작성하는 카피라이터입니다.
            주제 {state['topic']}에 대헤 한 문장으로 멋진 광고 카피를 한글로 작성해주세요.
            불필요한 설명 없이 오직 카피 문구만 출력하세요
            - 여러가지 버전 금지, 한 번에 하나만
            - 이유 설명 금지, 카피 문구만 출력
        """
        current_count = 1
    else:  # draft가 있으면 글을 수정
        print(f"--- 1-1. 글을 수정하는중,,,")
        prompt = f"""
            피드백을 수용하여 작성된 광고카피를 반영하여 다시 작성해주세요.
            - 여러가지 버전 금지, 한 번에 하나만
            - 이유 설명 금지, 카피 문구만 출력
            피드백: {state['feedback']}
            작성된 광고카피: {state['draft']}
        """
        current_count += 1
        
    print(f"--> {current_count}차 재시도")
    res = model.invoke(prompt)
    
    # 🎯 핵심: 변경된 draft와 count를 '함께' return하여 상태를 동기화합니다.
    return {
        'draft': res.content.strip(),
        'count': current_count
    }


def critic_node(state: WritingState) -> Dict:
    """작성된 글을 평가하고 피드백을 주는 노드"""
    print(f"--- 2. 검토하고 평가하고 피드백을 작성하는 중,,,")

    # 가상의 협격 조건: 혁신 또는 미래라는 키워드가 반드시 들어가야 함
    prompt = f"""
        당신은 광고 카피를 평가하는 전문가입니다.
        작성된 광고 카피를 평가하고 개선할 점이 있으면 피드백을 주세요.
        작성된 광고 카피: {state['draft']}
        피드백은 한글로 작성해주세요.

        [합격 조건]
        - 광고 카피에 반드시 '혁신' 또는 '미래'라는 키워드 포함되어야 함
        - 다른 설명 필요 없이 아래의 JSON 포맷으로만 응답하세요
        - 다른 설명 절대 금지
        ```json{{
            "status": "오직 "PASS" 또는 "RETRY"만 표기",
            "feedback": "status가 RETRY일 경우 조건을 만족하지 못하는 이유, PASS일 경우 칭찬"
        }}```
    """
    res = model.invoke(prompt)
    content = res.content.strip()
    # LLM이 JSON을 코드로 인식해 '''로 인식했을때의 대비
    if '```json' in content:
        content = content.split('```json')[1].split('```')[0].strip() 
    elif '```' in content:
        content = content.split('```')[1].split('```')[0].strip()
    
    try:
        result = json.loads(content)  # JSON 문자열을 파이썬 딕셔너리로 변환
        print(f"검토 결과: {result['status']}")
        return {
            'status': result['status'],
            'feedback': result['feedback']
        }
    except Exception as e:
        print(f"error: {e}")
        return{
            'status': 'RETRY',
            'feedback': f"JSON 파싱 오류: {e}. LLM 응답: {content}"
        }


def route_by_review(state: WritingState) -> str:
    if state['status'] == "PASS":
        print("[router_by_review] ✅ 광고 카피 작성 성공")
        return "go_end"
    elif state['count'] >= 3:
        print("[router_by_review] ❌ 3회 이상 재시도로 작성 실패:")
        return "go_end"
    else:
        print(f"[router_by_review] 🔄 재시도\nfeedback: {state['feedback']}")
        return "go_retry"

# 1. 저장소 등록
wf = StateGraph(WritingState)

# 2. 노드 등록
wf.add_node("writer", writer_node)
wf.add_node("critic", critic_node)

# 3. 엣지 구성(조건부 엣지)
wf.set_entry_point("writer")
wf.add_edge("writer", "critic")
wf.add_conditional_edges(
    "critic",
    route_by_review,
    {
        "go_retry": "writer",
        "go_end": END
    }
)

# 4. 컴파일 후 실행
app = wf.compile()
topic = input("무얼 팔고 싶으세여?\n")
result = app.stream({'topic': topic, 'draft': '', 'feedback': '', 'status': '', 'count': 0})

print(result)