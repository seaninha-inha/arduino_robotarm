import cv2
import numpy as np
import serial

ser = serial.Serial('COM3', 9600)
# VideoCapture 객체 생성
cap = cv2.VideoCapture(0)
# 물체 탐지 여부
object_detected = False

while True:

    ret, frame = cap.read()
    # 프레임 읽기 오류 처리
    if not ret:
        break

    # HSV 변환
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    detected_color = ""

    # RED
    lower_red1 = np.array([0,120,70])
    upper_red1 = np.array([10,255,255])

    lower_red2 = np.array([170,120,70])
    upper_red2 = np.array([180,255,255])

    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)

    mask_red = mask_red1 + mask_red2

    contours, _ = cv2.findContours(
        mask_red,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    for cnt in contours:

        area = cv2.contourArea(cnt)

        if area < 1000:
            continue

        perimeter = cv2.arcLength(cnt, True)

        if perimeter == 0:
            continue

        circularity = 4 * np.pi * area / (perimeter * perimeter)

        if circularity > 0.75:

            detected_color = "R"
    
    # GREEN
    lower_green = np.array([40,70,70])
    upper_green = np.array([80,255,255])

    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    contours, _ = cv2.findContours(
        mask_green,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    for cnt in contours:

        area = cv2.contourArea(cnt)

        if area < 1000:
            continue

        perimeter = cv2.arcLength(cnt, True)

        if perimeter == 0:
            continue

        circularity = 4 * np.pi * area / (perimeter * perimeter)

        if circularity > 0.75:

            detected_color = "G"
    
    # BLUE
    lower_blue = np.array([100,150,50])
    upper_blue = np.array([140,255,255])

    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    contours, _ = cv2.findContours(
        mask_blue,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    for cnt in contours:

        area = cv2.contourArea(cnt)

        if area < 1000:
            continue

        perimeter = cv2.arcLength(cnt, True)

        if perimeter == 0:
            continue

        circularity = 4 * np.pi * area / (perimeter * perimeter)

        if circularity > 0.75:

            detected_color = "B"

    # 새 물체 등장 시 아두이노로 한 번만 전송
    if detected_color != "":
        # 새 물체 등장
        if object_detected == False:
            ser.write(detected_color.encode())
            object_detected = True
            cv2.waitKey(3000)
    # 물체 사라짐
    else:
        object_detected = False

    cv2.imshow("camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
ser.close()
cv2.destroyAllWindows()