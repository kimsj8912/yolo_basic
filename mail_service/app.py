from http import client

import streamlit as st
from click import prompt
from google import genai
import os


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# streamlit run app.py
st.title('✏️ AI 자동 이메일 초안 작성기\n작성자: lyrical_1002 🪼')
api_key = st.sidebar.text_input('Gemini API Key', type='password')
context = st.text_area("어떤 메일을 보내야 하나요?", placeholder="예: 오늘 중식 메뉴 변경 안내 메일 작성해줘")
tone = st.selectbox("이메일 어조 선택", ['정중하고 격식있는', '친근하고 부드러운', '간결하게 핵심만'])
if st.button("이메일 초안 생성"):
    if not api_key:
        st.warning("API 키를 입력해주세요!!!")
    elif not context:
        st.warning("작성할 이메일 내용을 넣어주세요!!!")
    else:
        # print(f'api key: {api_key}')
        # print(f'tone: {context}')
        # print(f'tone: {tone}')

        with st.spinner('AI가 이메일을 작성 중입니다.'):
            client = genai.Client(api_key=api_key)
            prompt = f'다음 상황에 맞는 이메일을 {tone} 어조로 작성해줘 \n상황: {context}'
            resp = client.models.generate_content(
                model='gemini-3.1-flash-lite',
                contents=prompt
            )
            st.success("작성이 완료되었습니다🎉")
            st.text_area('생성된 이메일', value=resp.text, height=300)