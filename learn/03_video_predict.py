# 1. 모델 불러오기
from ultralytics import YOLO

model = YOLO('yolo26n.pt')

# 2. 동영상 분석 및 결과 저장
results = model.predict(
    source='sample.mp4',
    conf=0.5,
    show=True,
    save=False,
    exist_ok=True,
    verbose=False,   # 프레임 로그 출력 여부
    imgsz=[480, 640],
    stream=True
)


for result in results:
    boxes = result.boxes
    print(f"탐지 정보: {boxes}")