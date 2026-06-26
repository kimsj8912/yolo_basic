from matplotlib import patches
from ultralytics import YOLO
import matplotlib.pyplot as plt

model = YOLO('yolo26n.pt')
results = model.predict(
    "https://ultralytics.com/images/bus.jpg",
    conf=0.5,
    save=False,
    project="Myproject",
    name="result",
    exist_ok=True
)

print(f'원본 이미지 경로: {results[0].path}')
print(f'원본 데이터 크기: {results[0].orig_shape}')
print(f'분류 번호: {results[0].names}')
print(f'저장 위치: {results[0].save_dir}')
# print(f'박스들: {results[0].boxes}')
fig, ax = plt.subplots(figsize=(10, 8))

for box in results[0].boxes:
    x1, y1, x2, y2, conf, cls_id = box.data.tolist()[0]
    x, y, w, h = box.xywh.tolist()[0]

    cls_name = results[0].names[cls_id]
    label_text = f'{cls_name}: {conf:.2f}'

    colors = {0:'pink', 5:'lime'}

    bus_color = 'lime'
    person_color = 'pink'

    rect = patches.Rectangle((x1, y1), w, h,
                             linewidth=1,
                             edgecolor=colors[cls_id],
                             facecolor='none')
    ax.add_patch(rect)

    # 위치, 글자, 색상, 크기, 두께
    ax.text(
        x1, y1-10,
        label_text,
        color='white',
        fontsize=12,
        weight='bold',
        backgroundcolor=colors[cls_id],
    )

ax.imshow(results[0].orig_img)
plt.axis('off')
plt.show()  # YOLO는 BGR을 사용한다.