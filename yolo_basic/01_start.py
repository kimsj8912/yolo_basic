# print('hello world')

import torch
import torchvision
from torch.distributed import config
from ultralytics import YOLO

# print(f"pytorch version: {torch.__version__}")
# print(f"GPU 사용 가능 여부: {torch.cuda.is_available()}")
#
# if torch.cuda.is_available():
#     print(f"사용 중인 GPU 장치 이름: {torch.cuda.get_device_name(0)}")


model = YOLO('yolo26n.pt')  # 가장 최신의 경량화 모델(분류, 위치 탐지)

# save: 결과 파일 저장 여부
# conf: 정확도 기준(0.5 이상만 보여줘)
# exist_ok: 같은 폴더가 있을 경우 덮어쓴다.

model.predict("C:\DEEP\yolo_basic\cats.jpg",
              save=True,
              conf=0.5,
              project="MyProject",
              name="result",
              exist_ok=True)
print("예측 결과 이미지가 runs/detect/MyProject/result 폴더에 저장 되었습니다.")