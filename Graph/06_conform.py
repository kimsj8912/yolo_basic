import uuid
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langgraph.graph import add_messages, StateGraph, END
from langgraph.checkpoint.memory import MemorySaver


# 1. 저장소 생성
class EmailState(BaseModel):
    title: str=""
    email_detail: str=""

# 2. 모델 호출
llm = ChatOllama(
    base_url="http://localhost:11434",
    model="exaone3.5:7.8b",
    temperature=2,
)

# 3. 노드 생성
def write_email_node(state: EmailState) -> EmailState:
    """주어진 제목으로 이메일을 작성하는 노드"""
    print(f"--- 1. 이메일 작성중,,,")
    prompt = f"""
        당신은 이메일 작성 전문가입니다.
        다음의 이메일 제목을 바탕으로 정중하고 전문적인 이메일을 작성해주세요.
        설명이나 팁 없이 오직 메일 문장만 출력해주세요.
        [이메일 제목]
        : {state.title}
        [출력 형식]
        <이메일 내용을 이 칸에 채워주세요>
    """
    res = llm.invoke(prompt)
    state.email_detail = res.content.strip()
    print(f"✅ 이메일 작성 완료: {state.email_detail}")
    return state

def send_email_node(state: EmailState) -> EmailState:
    """작성된 이메일을 전송하는 노드"""
    print(f"--- 2. 이메일 전송됨!!!")
    prompt = f"""
        당신은 사내 이메일 작성 담당자입니다.
        다음의 이메일 내용을 전송하는 시뮬레이션을 수행해주세요.
        [이메일 내용]
        : {state.email_detail}
    """
    res = llm.invoke(prompt)
    return state

# 1. 저장소 등록
wf = StateGraph(EmailState)

# 2. 노드 등록
wf.add_node("write_email", write_email_node)
wf.add_node("send_email", send_email_node)

# 3. 엣지 등록(흐름제어)
wf.set_entry_point("write_email")
wf.add_edge("write_email", "send_email")
wf.add_edge("send_email", END)

# 1. 컴파일(memory, interrupt_before)

# checkpoint=True를 사용하면 이전 상태를 저장하고 재실행 시 이어서 실행 가능
check = MemorySaver()
# interrupt_before를 사용하면 특정 노드 실행 전 인터럽트 발생
app = wf.compile(checkpointer=check, interrupt_before=["send_email"])
# 2. 실행
config = {'configurable': {'thread_id': uuid.uuid4()}}

title = input("이메일 제목을 입력해주세요: ")
app.invoke({'title': title}, config=config)

state_snapshot = app.get_state(config=config)
print(f"대기 중인 노드들: {state_snapshot.next}")
# print(f"현재 데이터 상태: {state_snapshot.values}")


# 사람이 개입하여 진행 여부를 판단 및 제어
yn = input("이메일 전송을 진행하시겠습니까? (y/n): ")
if yn.lower().strip() == 'y':
    print("✅ 승인 완료! 이메일 전송을 진행합니다...")
    # 하던거 계속, 다시 값을 넣어주면 처음부터 다시 시작하기 때문에 안 돼!!!
    # memory에 저장된 내용으로 어디까지 진행되었는지 파악해서 이후 진행
    app.invoke(None, config=config)
else:
    print("😢 💦 거부되었습니다. 이메일 전송을 중단합니다...")
