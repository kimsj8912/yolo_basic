# 1. 임베딩 함수 정의
import os

import chromadb
import ollama
from PyPDF2 import PdfReader
from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter

ollama_ef = embedding_functions.OllamaEmbeddingFunction(
    url='http://127.0.0.1:11434/api/embeddings',
    model_name='nomic-embed-text:latest'
)

# 2. 벡터디비 설정
client = chromadb.PersistentClient(path='./my_db')
collection = client.get_or_create_collection(
    name='store_lecture',
    embedding_function=ollama_ef
)

# 3. 데이터 추가
def insert_data():
    path = 'data'
    for file in os.listdir(path):   # PDF 파일을 하나씩 불러서
        # print(file)
        print('-'*10 + f"{file}: start")
        print(f"roading,,, wait a minute")
        reader = PdfReader(path + '/' + file)   # 읽어온 다음
        text = ''
        for page in reader.pages:   # 페이지 별로
            text += page.extract_text() # 텍스트를 추출해서 합친다
        # print(text)

        text_spliter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=50,
            length_function=len
        )

        print(f"chunking!!!")
        chunks = text_spliter.split_text(text)
        print(f"{len(chunks)} 개 문맥 확보")

        filename = file.rsplit('.', 1)[0]   # 파일명만 추출해서 담는다.

        # ids 생성/삽입
        ids = [f'{filename}_{i}' for i in range(len(chunks))]  # 아이디 부여

        # documents 삽입
        # metadatas 생성/삽입
        metas = [{'subject': filename} for i in range(len(chunks))]
        print(metas)

        print('upsert,,,')
        collection.upsert(
            ids=ids,
            documents=chunks,
            metadatas=metas
        )
        print(f"{filename} 저장 완료!🎉🎉")
        # print(collection.get())
        print('\n')


# insert_data()

# print(collection.get(where={'subject':'scikit_learn'})["documents"])

# 4. 질의문 작성
def search_data(subject, query):
    print(f'먼저! {subject}: {query}에 해당하는 docs 가져오는 중...')
    results = collection.query(
        query_texts=[query],
        n_results=5,
        where={'subject': {'$eq':subject}}
    )
    docs = results["documents"][0]
    print(f"docs는 다음과 같이 찾앗어요 >> {docs}")
    context = '\n\n'.join(docs)

    prompt = f"""
            당신은 python과 머신러닝, fast api의 일타강사입니다.
            [참고 교재]를 바탕으로 사용자의 [질문]에 알기 쉽게 설명해 주세요.
            만약 모르는 내용이거나 [참고 교재]에 없는 내용은 모른다고 답해주세요.
            
            [참고 교재]
            {context} 
            
            [질문]
            {query}
            """
    print("올라마는 생각중.... 기다려바")
    resp = ollama.generate(model='exaone3.5:2.4b', prompt=prompt, stream=True)

    for chunk in resp:
        print(chunk['response'], end='', flush=True)

user_subject = input('물어보고 싶은 과목이 무엇인가요🤸🤸🤸>>\n1. FASTAPI\n2. pandas\n3. scikit_learn\n')
question = input('궁금한 건 무엇이든 대답해드립니다 허허🕵️\n')

search_data(user_subject, question)
