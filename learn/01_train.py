import os.path
from os.path import exists

from tqdm import tqdm
from torchvision import datasets
from ultralytics import YOLO

class_names = ["T-shirt", "Trouser", "Pullover", "Dress", "Coat",
               "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]

# 1. fashion MNIST를 다운로드 받아온다.
def download_image(split='train'):
    is_train = True if split == 'train' else False

    dataset = datasets.FashionMNIST(root='./data', train=is_train, download=True)

    # fashion_mnist/train/[아이템명]/0.jpg 형태로 저장
    for idx in tqdm(range(len(dataset))):
        image, label = dataset[idx]
        label_name = class_names[label]
        save_dir = os.path.join('fashion_mnist', split, label_name)
        os.makedirs(save_dir, exist_ok=True)
        image.save(f"{save_dir}/{idx}.jpg")

    print(f"{split} 이미지 저장 완료")

# download_image('train')
# download_image('test')


# 학습
# 1. 모델을 불러온다.
model = YOLO('yolo26n-cls.pt')

# 2. 모델을 학습 시킨다.
model.train(
    data='fashion_mnist',   # 학습할 데이터의 최상위 폴더 경로 지정
    exist_ok=True,      # 이게 없으면 result 폴더가 계속 늘어난다.
    epochs=10,       # 전체 이미지를 총 10번 돌며 학습
    imgsz=28,       # 이미지 크기 28X28
    batch=64,       # 한 번에 처리할 미니배치 크기
    workers=4,      # 데이터 로딩에 사용할 CPU 스레드 수
)
print("모델 학습 완료")

