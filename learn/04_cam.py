# 1. 모델 가져오기
from ultralytics import YOLO

model = YOLO('yolo26n.pt')

# 2. 예측
results = model.predict(
    source=0,
    conf=0.5,
    show=True,
    save=False,
    exist_ok=True,
    verbose=False,
    stream=True,
)

for result in results:
    boxes = result.boxes
    print(f"탐지 정보: {boxes}")