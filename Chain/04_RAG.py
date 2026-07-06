import chromadb
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_text_splitters import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
from langchain_core.prompts import ChatPromptTemplate

# 1. Chromadb 호출
client = chromadb.PersistentClient(path='my_db')

# 2. embedding 함수 생성
embed_func = OllamaEmbeddings(base_url='http://localhost:11434', model='nomic-embed-text:latest')

# 3. 컬렉션 준비
store = Chroma(
    client=client,
    collection_name='pandas',
    embedding_function=embed_func
)


# 4. 데이터 추가
def add_data():
    path = 'data/pandas.pdf'
    text = ''
    for page in PdfReader(path).pages:
        text += page.extract_text()

    # 특정한 chunk 단위로 자른다.
    text_spliter = RecursiveCharacterTextSplitter(
        chunk_size=150,
        chunk_overlap=30,
        length_function=len
    )
    # 잘 잘라 졌는지 출력
    docs = []
    for chunk in text_spliter.split_text(text):
        # doc = Document(id='doc1', page_content=chunk,metadata={})
        # id 를 지정하지 않으면 UUID 를 통해 알아서 만든다.
        doc = Document(page_content=chunk)
        docs.append(doc)  # 개별 문서를 리스트에 담은 다음에

    store.add_documents(docs)  # 여기에 일괄로 추가
    print('저장완료')
    print(f'저장내용 : {store.get()}')


add_data()

# LLM 모델 생성
model = ChatOllama(model='exaone3.5:7.8b', temperature=2)
# 질문을 받는다.
question = input('PANDAS 에 대해서 궁금한 점을 물어보세요\n')

# 프롬프트 템플릿 생성
temp = ChatPromptTemplate.from_template("""
    당신은 pandas 를 가르치는 강사입니다. 아래 [참고문서]의 내용만을로 답변하세요.
    [참고문서]에 없는 내용은 "참고문서에 없는 내용이라 답변이 어렵습니다." 라고 대답하세요.

    [참고문서]
    {context}

    [질문]
    {question}
""")
# RAG 로부터 검색 -> 검색모드로 전환
result = store.as_retriever(search_kwargs={'k': 5})

# 검색 내용을 프롬프트에 적용 후 질문
# context : 검색기에서 나온 내용을 전달
# question : 뭔지 모르겠지만 그냥 두라는 뜻
# StrOutputParser() : 문자열로 변환해서 내보내라(chunk.content 를 안써도 됨)
chain = {'context': result, 'question': RunnablePassthrough()} | temp | model | StrOutputParser()

for chunk in chain.stream(question):
    print(chunk, end='', flush=True)