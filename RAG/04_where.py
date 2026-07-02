import chromadb

client = chromadb.PersistentClient(path='./my_db')
coll = client.get_or_create_collection(name='study')

def add_data(doc, meta, id):
    coll.upsert(
        documents=[doc],
        metadatas=[meta],
        ids=[id]
    )
    data = coll.get(ids=[id])
    print(f'ids:{data['ids']} / documents: {data['documents'][0]} / meta: {data['metadatas'][0]}')

# add_data('파이썬 완벽 가이드', {'lang':'python', 'year':2024, 'official':True}, 'id1')
# add_data('자바의 성능 최적화', {'lang':'java', 'year':2022, 'official':True}, 'id2')
# add_data('리액트 기초 실습', {'lang':'java', 'year':2023, 'official':False}, 'id3')


# 단순 조건 - 2023년 이후 데이터만 검색
resp = coll.query(
    query_texts=['공부할 자료를 찾아줘'], # 검색 질의문
    n_results=2,    # 반환받을 데이터 수
    where={         # 메타데이터 검색 조건
        'year':{'$gte':2023}
    }
)
print('단일 조건'+'-'*20)
for i in range(len(resp['documents'][0])):
    print(f'{resp['ids'][0][i]} / documents: {resp['documents'][0][i]} / meta: {resp['metadatas'][0][i]}')
print('\n')


# and 조건 - official 이 True이고 lang이 python인 데이터 검색
print('AND 조건'+'-'*20)
resp = coll.query(
    query_texts=['공부할 자료를 찾아줘'],
    n_results=2,
    where={
        '$and':[
            {'official':{'$eq':True}},
            {'lang':{'$eq':'python'}}
        ]
    }
)
for i in range(len(resp['documents'][0])):
    print(f'{resp['ids'][0][i]} / documents: {resp['documents'][0][i]} / meta: {resp['metadatas'][0][i]}')
print('\n')


# or 조건 - official 이 False이거나 lang이 python인 데이터 검색
print('OR 조건'+'-'*20)
resp = coll.query(
    query_texts=['공부할 자료를 찾아줘'],
    n_results=2,
    where={
        '$or':[
            {'official':{'$eq':False}},
            {'lang':{'$eq':'python'}}
        ]
    }
)
for i in range(len(resp['documents'][0])):
    print(f'{resp['ids'][0][i]} / documents: {resp['documents'][0][i]} / meta: {resp['metadatas'][0][i]}')
print('\n')
