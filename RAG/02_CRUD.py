import chromadb

client = chromadb.PersistentClient('./my_db')
collection = client.get_or_create_collection('user_guide')

def add_data():
    collection.add(
        documents=[
            "로그인 하려면 우측 상단의 버튼을 누르세요",
            "비밀번호를 잊으셨나요? 이메일 인증을 진행하세요",
            "환경설정에서 다크모드를 지원합니다.",
        ],
        metadatas=[
            {'category': 'auth', 'importance':1},
            {'category': 'auth', 'importance':2},
            {'category': 'settings', 'importance':1},
        ],
        ids=["doc1", "doc2", "doc3"]
    )
    print("data 생성 완료")

# add_data()

# 데이터 조회
# get()의 경우 정확한 id 혹은 데이터를 통해 가져올 때 사용
results = collection.get()
print(f"---collection.get()--- \n{results}\n")

def use_id():
    id_result = collection.get(ids=["doc1", "doc3"])
    print(f"---collection.get() with use_id()---")
    for doc in id_result["documents"]:
        print(f"doc: {doc}")

use_id()
print('\n')

# query의 경우 의미에 기반한 검색
def use_query():
    query_result = collection.query(
        query_texts=["비밀번호 찾는 방법 알려줘"],
        n_results=2
    )
    print("---collection.query()---")
    # for doc in query_result["documents"][0]:
    #     print(f"doc: {doc}")
    #
    # for dis in query_result["distances"][0]:
    #     print(f"distance: {dis}")

    for i in range(len(query_result["documents"][0])):
        print(f"doc: {query_result["documents"][0][i]}")
        print(f"dis: {query_result["distances"][0][i]}")
    print('\n')

use_query()

# 데이터 수정 - 특정 id의 문서를 수정(내용, 메타데이터)
def update_data():
    collection.update(
        ids=["doc1"],
        documents=['로그인 방법: 우측 상단 로그인 버튼 클릭 후 아이디 입력'],
        metadatas=[{'importance':3}]
    )
    print('수정완료')
    result = collection.get(ids=["doc1"])
    meta = result['metadatas']

    # 결과 출력
    print("---collection.update()---")

    for i in range(len(result['documents'])):
        print(f"doc: {result['documents'][i]}") # documents

        # metadatas
        print(f"importance: {meta[i]['importance']}")
        print(f"category: {meta[i]['category']}")
    print('\n')

update_data()


# delete - 데이터 삭제
# 특정 아이디를 삭제하거나 특정 조건에 해당하는 데이터를 삭제
def delete_data():
    collection.delete(ids=['doc3']) # 특정한 아이디 삭제
    results = collection.get()

    print("---collection.delete()---")
    for i in range(len(results['ids'])):
        print(f"id: {results['ids'][i]}")

    print('\n')

delete_data()