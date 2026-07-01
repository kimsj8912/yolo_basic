import cv2
from ultralytics import YOLO

cap = cv2.VideoCapture(0)
model = YOLO('best.pt')

while True:
    success, frame = cap.read() # 웹 캠에서의 frame

    if not success: # 카메라가 꺼졌을 때 반복을 멈춘다.
        print("화면에 문제가 발생했습니다.")
        break

    # 받아온 frame을 yolo에 예측시켜서 결과를 반환받는다.
    results = model.predict(
        frame,
        conf=0.02,
        imgsz=[480,640],
        show=False,
        classes=[0],
        verbose=False
    )

    # 탐지한 결과가 반영된 frame을 받아 낸다.
    yolo_frame = results[0].plot()

    resize_frame = cv2.resize(yolo_frame, (480, 640))
    cv2.imshow('YOLO TEST', resize_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):   # 0.001초마다 키를 감지, q가 눌린다면
        break   # 탈출


cap.release()
cv2.destroyAllWindows()