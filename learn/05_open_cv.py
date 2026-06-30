import cv2
from pip._internal.commands import show
from ultralytics import YOLO

print(f"open CV : {cv2.__version__}")


cap = cv2.VideoCapture('sample.mp4')
model = YOLO('yolo26n.pt')

# 1/1000 초 마다 키 확인, q를 누르면
while True:
    success, frame = cap.read() # 성공 여부, 프레임
    if not success:
        print('영상이 손상되었습니다.')
        break

    results = model.predict(
        frame,
        conf=0.5,
        verbose=False,
        show=False,
        classes=[0,2],   # 특정한 분류만 보여줘, 0-사람 / 2-차량
    )

    yolo_frame = results[0].plot()   # YOLO에서 그린 프레임 가져오기
    # openCV로 화면에 표시
    resize_frame = cv2.resize(yolo_frame, (480,640))
    cv2.imshow('YOLO 실시간 추적', resize_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break   # 탈출 문

print("프로그램 종료")

# 사용한 캡쳐와 창 자원 반납하기
cap.release()
cv2.destroyAllWindows()