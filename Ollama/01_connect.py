# 1. 대화 내용 입력
from ollama import chat

text = input('local llm에게 하고싶은 말이 잇나요\n올라마가 대답해줄게요0_0:\n')
# print(text)


# 2. LLM에 전달

# 한 번에 대답을 보내주는 방식 - 주로 시스템에서 내용을 받을 경우
def batch_style():
    print('생각중,,,...마떼루용')
    resp = chat(
        model='exaone3.5:7.8b',
        messages=[{'role':'user', 'content':text}]
    )
    print(resp.message.content)

# batch_style()

# 단어별로 실시간으로 보내주는 방식 - 주로 사용자에게 직접 내용을 보낼 때
def realtime_style():
    resp = chat(
        model='exaone3.5:7.8b',
        messages=[{'role': 'user', 'content': text}],
        stream=True
    )
    for chunk in resp:
        # end=''가 없으면 한 글자씩 줄바꿈 시킴
        # flush=True 이면 한 번에 밀어낸다
        print(chunk.message.content, end='', flush=True)

realtime_style()

# 3. 답변 출력