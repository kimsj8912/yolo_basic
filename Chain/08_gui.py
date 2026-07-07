import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

st.title("실시간 챗봇🔥🔥")

# 1. 사용자 입력 받기
user_input = st.text_input("안녕난올라만데암거나물어바바\n")
# 2. 유저 입력이 있으면
if not user_input == '':
    # 3. 표시해주고
    with st.chat_message("user"):
        st.write(user_input)


# 말풍선 모양 UI 생성
if user_input:
    with st.chat_message("assistant"):
        # 4. 모델을 생성하여 전달
        model = ChatOllama(
            base_url="http://localhost:11434",
            model="llama3.2:3b",
            temperature=0,
        )
        prompt = ChatPromptTemplate.from_template("당신은 재미있는 대화상대 입니다. 질문에 재미있게 답해주세요.\n 질문: {question}")
        chain = prompt | model | StrOutputParser()
        # 5. 모델에서 나온 답변을 출력
        st.write_stream(chain.stream({'question': user_input}))

# session - 어떤 데이터를 브라우저가 켜져있는 동안 저장하는 장소

# st.session_state['messages'] = []
# 앱이 켜 있는 동안 무언가를 messages라는 이름으로 저장할 떄

# st.session_state["messages"]
# 앱이 켜 있는 동안 messages 라는 이름으로 무언가를 가져올 때