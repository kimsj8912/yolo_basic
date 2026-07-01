import os
import random
import shutil

from ultralytics import YOLO


# 1. 폴더 생성
    # dataset/train/images
    # dataset/train/labels
    # dataset/val/images
    # dataset/val/labels

def split_data(root_dir='dataset', train_ratio=0.8):
    train_img_path=f'{root_dir}/train/images'
    train_label_path=f'{root_dir}/train/labels'
    val_img_path=f'{root_dir}/val/images'
    val_label_path=f'{root_dir}/val/labels'

    os.makedirs(train_img_path, exist_ok=True)
    os.makedirs(train_label_path, exist_ok=True)
    os.makedirs(val_img_path, exist_ok=True)
    os.makedirs(val_label_path, exist_ok=True)

    # 2. dataset/source 에 있는 txt와 jpg를 섞은 다음 분산 저장
    files = []   # 파일 명을 담아서 흔들어 섞을 리스트
    for file in os.listdir(f'{root_dir}/source'):
        # print(file)
        if file.lower().endswith('.jpg'):
            files.append(file)

    random.shuffle(files)
    # print(files)
    # 80:20으로 분리
    train_files = files[:int(len(files)*train_ratio)]
    val_files = files[int(len(files)*train_ratio):]

    # 분산 저장
    for train in train_files:
        # rsplit('.',1) 오른쪽에서부터 찾은 . 첫번째를 기준으로 쪼개라
        name = train.rsplit('.', 1)[0]
        shutil.copy(f'{root_dir}/source/{train}', f'{train_img_path}/{train}')
        shutil.copy(f'{root_dir}/source/{name}.txt', f'{train_label_path}/{name}.txt')

    for val in val_files:
        name = val.rsplit('.', 1)[0]
        shutil.copy(f'{root_dir}/source/{val}', f'{val_img_path}/{val}')
        shutil.copy(f'{root_dir}/source/{name}.txt', f'{val_label_path}/{name}.txt')


# split_data()


# 2. YOLO 를 이용해 학습
model = YOLO('yolo26n.pt')

results = model.train(
    data='dataset/data.yaml',
    exist_ok=True,
    epochs=5,
    imgsz=[480,640],
    batch=64,
    workers=4
)
print('모델 학습 종료')
print(f'정밀도: {results.results_dict['metrics/precision(B)']:.4f}')
print(f'재현율: {results.results_dict['metrics/recall(B)']:.4f}')
print(f"result: {results.results_dict}")
