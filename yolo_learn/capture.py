# 동영상으로 부터 이미지를 추출한다.
import cv2
import os

cap = cv2.VideoCapture('선풍기.mp4')
save_dir = 'dataset/source'
img_cnt = 0 # 몇번째 이미지인지
cap_cnt = 0 # 파일명으로 사용할 번호

if not os.path.exists(save_dir):
    os.makedirs(save_dir)
    print('폴더 생성')

while True:
    success, frame = cap.read()

    if not success or frame is None:
        print("영상이 끝났거나 더 이상 프레임이 없습니다.")
        break
    # 크기가 너무 클 경우 리사이즈 해서 줄여준다.
    resize_frame = cv2.resize(frame, (480, 640))
    cv2.imshow('movie',resize_frame)

    if img_cnt % 5 == 0:
        file_name = f'{save_dir}/{cap_cnt}.jpg'
        cv2.imwrite(file_name, resize_frame)
        print(f'{file_name} 이 저장됨')
        cap_cnt += 1

    img_cnt += 1

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break



cap.release()
cv2.destroyAllWindows()