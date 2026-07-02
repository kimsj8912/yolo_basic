import cv2
from pyparsing import results
from ultralytics import YOLO

# 1. 웹캠 켜기
cap = cv2.VideoCapture(0)
model = YOLO('best.pt')

# 2. 카메라로 부터 프레임 받아오기
while True:
    ret, frame = cap.read()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("quit")
        break
    if not ret:
        print("fail")
        break

    # 3. 프레임을 YOLO에게 전달 및 predict
    results = model.predict(
        frame,
        conf=0.5,
        imgsz=[480,960],
        show=False,
        verbose=False,
        classes=[0]
    )

    # 4. 결과물에서 frame 추출
    yolo_frame = results[0].plot()

    # 5. 사이즈 조정(선택)
    resize_frame = cv2.resize(yolo_frame, (480, 640))

    # 6. opencv를 통해 화면에 표출
    cv2.imshow('face detect', resize_frame)

# 7. 종료 시 카메라와 창 모두 닫기
cap.release()
cv2.destroyAllWindows()