### 스스로 해보기
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_ollama import ChatOllama
#
# # 1. 모델 호출
# model = ChatOllama(model='exaone3.5:7.8b')
#
# # 2. 프롬프트 제작
# template = ChatPromptTemplate.from_messages([
#     ('system','당신은 인공지능 모델 전문가 입니다. 질문에 대해 간결하게 대답해 주세요.'),
#     ('user','{topic}에 대해서 설명해 주세요.')
# ])
#
# # 2-1. 프롬프트 템플릿 + 모델 => 실행객체
# # pipeline(chain) : LCEL(Lang Chain Express Languege)
# chain = template | model
#
# # 3. 명령내리기
# topic = input('인공지능에 대하여 궁금한 점 물어보기 !')
# # result = chain.invoke({'topic': topic}) # batch - 한방에 대답(답답할 수 있다.)
# for ch in chain.stream({'topic': topic}):
#     print(ch.content,end='',flush=True)
#
# # 4. 응답 출력
# # print(result.content)

################### 수업내용 ####################
#간단한 묻고 답하기 만들기 #연속지질문 가능하게

# 간단한 묻고 답하기 만들기
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage

# 1. 모델 생성
model = ChatOllama(model='exaone3.5:7.8b')

conversation_history = [] # 대화 저장 리스트


# 3. 프롬프트 만들기
temp = ChatPromptTemplate.from_messages([
    ('system','당신은 답변 전문 AI 입니다. 주어진 질문에 대해서 간단하게 답변해 주세요.'),
    MessagesPlaceholder(variable_name="history"),# 대화 내용을 history 라는 이름으로 줄테니 참고해라
    ('user','{query}')
])
chain = temp | model # 4. 조립


while True:
    # 2. 질문 받기
    query = input('아무거나 질문 하세요!\n')

    if query == 'exit':
        print('대화 종료')
        break

    ###방법1.
    # 5. 출력
    # full_response = ''
    # for chunk in chain.stream({'query':query,'history':conversation_history}):
    #     print(chunk.content,end='', flush=True) # end 다음 공백을 줘야 줄바꿈이 가능함
    # print('\n')
    # conversation_history.append(HumanMessage(content=query)) # 사용자가 물어본 내용
    # conversation_history.append(AIMessage(content='')) # 시스템이 답변한 내용
    # print(f'history: {len(conversation_history)}')

 ###방법2.
    # 5. 출력
    # answer = ''
    # for chunk in chain.stream({'query': query, 'history': conversation_history}):
    #     print(chunk.content, end='', flush=True)  # end 다음 공백을 줘야 줄바꿈이 가능함
    #     answer += chunk.content
    # print('\n')
    # conversation_history.append(HumanMessage(content=query))  # 사용자가 물어본 내용
    # conversation_history.append(AIMessage(content=answer))  # 시스템이 답변한 내용
    # print(f'history: {len(conversation_history)}')



# ESC 로 종료
    if query == '\x1b':  # ESC 키
        print('대화 종료')
        break
