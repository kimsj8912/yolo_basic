# 1. 모델 호출
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

model = ChatOllama(model='exaone3.5:2.4b')

# 2. 프롬프트 제작
template = ChatPromptTemplate.from_messages([
    ('system', '당신은 인공지능 모델 전문가 입니다. 질문에 대해 간결하게 대답해 주세요.'),
    ('user', '{topic}에 대해서 설명해 주세요.')
])

# 2-1. 프롬프트 템플릿 + 모델 => 실행할 객체
# pipeline(chain) : LCEL(Lang Chain Express Language)
chain = template | model

# 3. 명령내리기
topic = input('🧠인공지능💡에 대해서 암거나 물어바바 --> 단어로만 입력해\n')
print("🐢생각중..🐢....🐢..")
# result = chain.invoke({'topic': topic}) # batch - 한 방에 대답
# 4. 응답 출력
# print(result.content)

for ch in chain.stream({'topic': topic}):   # stream - 실시간
    print(ch.content, end='', flush=True)

