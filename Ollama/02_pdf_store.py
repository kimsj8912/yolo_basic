# 1. 임베딩 함수 정의
import chromadb
import ollama
from PyPDF2 import PdfReader
from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter

ollama_ef = embedding_functions.OllamaEmbeddingFunction(
    url='http://localhost:11434/api/embeddings', # 올라마가 있는 주소, 어딧니 올라마야~
    model_name='nomic-embed-text:latest'   # 사용 모델
)

# 2. chromaDB 동작, collection 정의
client = chromadb.PersistentClient(path='./my_db')
collection = client.get_or_create_collection(
    name='store_novel',
    embedding_function=ollama_ef    # 임베딩 모델 지정
)



# text 안에는 소설 한 편이 다 들어있으므로 파악하기 좋게 쪼개주어야 함
def my_tokenizer(text):
    text = text.strip()  # trim() 처럼 앞뒤 공백 제거
    # 두 글자 미만은 사용 안 함 - 소설이기에 의미 없다고 판단
    if len(text) < 2:
        return 0

    resp = ollama.generate(
        model='exaone3.5:2.4b',
        prompt=text,
        options={'num_predict': 1}  # 답변은 한 글자만 해라(너한테 답변 듣자고 하는게아냐)
    )
    return resp.get('prompt_eval_count')

    # 3. 데이터 추가
def insert_data():
    path = 'data/운수좋은날.pdf'
    # 특정 위치에 있는 PDF 읽어오기
    reader = PdfReader(path)

    # 페이지별로 가져와 텍스트만 추출
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    print('텍스트 추출 완료')
    text_spliter = RecursiveCharacterTextSplitter(
            chunk_size=800,  # 한 기억 단위를 800자 씩
            chunk_overlap=50,  # 청크끼리 50자 씩 겹친다
            length_function=my_tokenizer  # len: (기본값) 무조건 글자수로 800을 잡음
        )

    print('chunking 작업 중...,,,')
    chunks = text_spliter.split_text(text)
    print(f"chunks: {len(chunks)}")
    ids = []    # 아이디 부여
    for i in range(len(chunks)):
        ids.append(f'idx_{i}')
    # chromaDB 에 저장
    collection.add(documents=chunks, ids=ids)
    print(f"저장 완료: {len(chunks)} 개 문맥 확보")

#
# insert_data()
# print(collection.get())



# 4. 질의문 작성
question = input('운수 좋은날에 대해 암거나 물어바여 -->\n')

def search_data():
    # 1. vector db에 질의문을 넣는다.
    result = collection.query(query_texts=[question], n_results=5)
    print(result)

    context = '\n\n'.join(result['documents'][0])

    # 2. 결과값을 가지고 prompt를 작성한다.
    prompt = f"""
            당신은 소설 분석 전문가 입니다. 제공된 [소설 본문 발췌]를 바탕으로 사용자의 [질문]에 답하세요,
            본문에 근거하여 인물의 심리, 사건의 배경, 복선 등을 상세히 분석해주세요
            [소설 본문 발췌]
            {context}
            
            [질문]
            {question}
            """

    # 3. 프롬프트의 결과값을 사용자에게 보여준다.
    resp = ollama.generate(model='exaone3.5:2.4b', prompt=prompt, stream=True)

    for chunk in resp:
        print(chunk['response'], end='', flush=True)

search_data()