import chromadb

client = chromadb.PersistentClient(path='./my_db')
collection = client.get_or_create_collection(name='study')


def add_data():
    collection.add(
        ids=['doc1', 'doc2'],
        documents=[
            '파이썬 기초 문법 가이드',
            '자바 고급 성능 최적화'
        ],
        metadatas=[
            {'lang':'python', 'level':'beginner', 'version':'3.14'},
            {'lang':'java', 'level':'advanced', 'version':25},

        ]
    )

# add_data()
# result = collection.get()
# print(result)


results = collection.query(
    query_texts=["공부할 내용을 추천해줘"],
    n_results=1,
    # 언어는 파이썬이고, 난이도는 초급 중에서 추천해줘
    where={
        '$and': [
            {'lang': {'$eq': 'python'}},
            {'level': {'$eq': 'beginner'}},
        ]
    }
)

print(results)
print('\n')
print('---분리---')

print(f"doc: {results['documents'][0][0]}")
print(f"meta: {results['metadatas'][0][0]}")
print(f"dis: {results['distances'][0][0]}")

