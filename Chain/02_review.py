#클래스는 무조건 대문자 Blackcolor <- 파스칼 표기법
#black_color <- 스네이크표기법(의미가 있는 단어사이에 언더바를 넣는 방식)
#blackColor <- 카멜표기법(의미가 있는 단어의 첫글자를 대문자로 표기하는 방식) , 단 맨 앞글자는 쓰면 안됨
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from pydantic import BaseModel
from pydantic import BaseModel, Field

review_text = input('후기를 입력 하세요\n')
print(review_text)

# 1. 출력 구조를 담당할 클래스
class ReviewAnalysis(BaseModel):
    sentiment:str = Field(description='긍정,중립,부정 중 하나')  #class 배웠을때 description은 생성자임
    score:int = Field(description='1점부터 5점까지의 만족도 점수, 절대 1보다 작지 않고 5보다 크지 않아야 함')
    summary:str = Field(description='리뷰 핵심 내용을 한줄로 요약')

#2. 모델 지정
model = ChatOllama(model='exaone3.5:7.8b') #한글을 제일 잘 알아들음

#3. 출력구조 지정
structured_model = model.with_structured_output(ReviewAnalysis) # 여긴 어떻게 class 가 들어가지,? 라는 의문을 가져보기

#4. 프롬프트 생성
template = ChatPromptTemplate.from_messages([
    ('system','당신은 리뷰 분석가 입니다. 주어진 리뷰를 바탕으로 지정된 형식으로 답변하세요. score 는 최고 5점입니다.'), # 페르소나를 줄 수 있는 구간임
    ('human','{review}'),
])

# 5. 파이프라인으로 조립(LCEL)
chain = template | structured_model

# 6. 실행(invoke,stream)
resp = chain.invoke({'review':review_text})
print(resp)