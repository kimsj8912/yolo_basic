import uuid
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver


# 1. 저장소 생성
class EmailState(BaseModel):
    title: str = ""
    email_detail: str = ""
    is_approved: bool = False  # 승인 여부 플래그 추가


# 2. 모델 호출
llm = ChatOllama(
    base_url="http://localhost:11434",
    model="exaone3.5:7.8b",
    temperature=0.5,
)


# 3. 노드 생성
def write_email_node(state: EmailState) -> EmailState:
    """주어진 제목으로 이메일을 작성하는 노드"""
    print(f"\n--- 1. 이메일 작성 중,,, ---")
    prompt = f"""
        당신은 이메일 작성 전문가입니다.
        다음의 이메일 제목을 바탕으로 정중하고 전문적인 이메일을 한글로 작성해주세요.
        설명이나 팁 없이 오직 메일 내용만 출력해주세요.
        [이메일 제목]
        : {state.title}
        [출력 형식]
        <이메일 내용을 이 칸에 채워주세요>
    """
    res = llm.invoke(prompt)
    state.email_detail = res.content.strip()
    print(f"✅ 이메일 작성 완료:\n{state.email_detail}")
    return state


def send_email_node(state: EmailState) -> EmailState:
    """작성된 이메일을 전송하는 노드"""
    print(f"\n--- 2. 이메일 전송됨!!! ---")
    prompt = f"""
        당신은 사내 이메일 작성 담당자입니다.
        다음의 이메일 내용을 전송하는 시뮬레이션을 수행해주세요.
        [이메일 내용]
        : {state.email_detail}
    """
    res = llm.invoke(prompt)
    print(f"✅ 이메일 전송 완료: {res.content.strip()}")
    return state


def route_by_approval(state: EmailState) -> str:
    """승인 여부에 따라 send_email로 가거나 write_email(재작성)로 순환하는 조건부 함수"""
    while True:
        yn = input("이메일을 그대로 전송하시겠습니까? (y: 승인 / n: 재작성 요구): ").lower().strip()
        if yn not in ['y', 'n']:
            print("잘못된 입력입니다. 'y' 또는 'n'을 입력해주세요.")
            continue
        break

    if yn == 'y':
        state.is_approved = True
        return "go_send_email"
    else:
        # 거부되었을 경우 다시 작성 노드로
        return "go_write_email"


# 1. 저장소 등록
wf = StateGraph(EmailState)

# 2. 노드 등록
wf.add_node("write_email", write_email_node)
wf.add_node("send_email", send_email_node)

# 3. 엣지 등록(흐름제어 - 조건부 엣지로 루프 구현)
wf.set_entry_point("write_email")

# write_email 실행 후 approval 조건에 따라 분기 (승인->send_email, 거부->write_email 재작성)
wf.add_conditional_edges(
    "write_email",
    route_by_approval,
    {
        "go_send_email": "send_email",
        "go_write_email": "write_email",
    },
)
wf.add_edge("send_email", END)


# 1. 컴파일 (memory, interrupt_before)
# write_email 직후에 인간의 검토를 받기 위해 interrupt_before 설정
check = MemorySaver()
app = wf.compile(checkpointer=check, interrupt_before=["send_email"])


# 2. 실행
config = {'configurable': {'thread_id': uuid.uuid4()}}

title = input("이메일 제목을 입력해주세요: ")
app.invoke({'title': title}, config=config)
