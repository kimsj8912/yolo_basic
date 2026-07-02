import chromadb

# 1. 클라이언트 생성(데이터를 로컬에 영구 저장하도록 설정)
client = chromadb.PersistentClient(path='./my_db')

# 2. 컬렉션 생성 - 데이터 꾸러미 공간
collection = client.get_or_create_collection(name='my_collection')

# 3. 데이터(문서) 추가 - AI model 사용됨
# 별도로 지정하지 않으면 기본모델(all-MiniLM-L6-v2)을 사용
collection.add(
    documents=[
        "RAG는 외부 데이터를 참조하여 답변을 생성하는 기술입니다.",
        "벡터 DB는 의미적 유사도를 바탕으로 데이터를 검색합니다.",
        "파이썬은 데이터 과학과 AI 분야에서 널리 쓰이는 언어입니다."
    ],  # 입력할 내용
    ids=["id1", "id2", "id3"]  # 입력된 문서에 대한 고유 번호
)

# 4. 검색 - 질문과 유사한 데이터 2개 가져와
results = collection.query(
    query_texts=["RAG가 뭐야?"],
    n_results=2
)

# 5. 결과 출력
# print(f'검색 결과: {results["documents"]}')

for sentence in results["documents"][0]:
    print(sentence)
