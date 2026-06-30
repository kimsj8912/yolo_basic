# 1. 모델 불러오기
from ultralytics import YOLO
import matplotlib.pyplot as plt

model = YOLO('runs/classify/train/weights/best.pt')

# 2. 테스트할 이미지 준비
test_img = 'fashion_mnist/test/Shirt/4.jpg'

# 3. 예측시키기
results = model.predict(
    source=test_img,
    save=True,
    project='predict',
    name='test_result',
    exist_ok=True
)
print('예측 결과를 runs/classfy/predict/test_result/ 에 저장했습니다.')

idx = results[0].probs.top1
plt.title(results[0].names[idx])
plt.imshow(results[0].orig_img)
plt.axis('off')
plt.show()

print(f"확률이 가장 높은 인덱스 번호: {idx}")
print(f"1등의 확률 : {results[0].probs.top1conf}")
print(f"1등 ~ 5등 : {results[0].probs.top5}")
print(f"1등 ~ 5등의 확률 : {results[0].probs.top5conf.tolist()}")
print(f"클래스 이름들 : {results[0].names}")
print(f"원본이미지(numpy) : {results[0].orig_img.shape}")
