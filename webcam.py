import cv2
import numpy as np
import serial
import time

# 설정값
SERIAL_PORT = 'COM3'
BAUD_RATE = 9600
COOLDOWN_SEC = 3.0
KERNEL = np.ones((5, 5), np.uint8)

# HSV 색상 범위 (색상, 채도, 명도)
COLOR_RANGES = {
    "R": [
        (np.array([0, 120, 70]),   np.array([10, 255, 255])),
        (np.array([170, 120, 70]), np.array([180, 255, 255])),
    ],
    "G": [
        (np.array([40, 70, 70]),   np.array([80, 255, 255])),
    ],
    "B": [
        (np.array([100, 150, 50]), np.array([140, 255, 255])),
    ],
}


# HSV 색상 범위를 이용해 마스크 생성
def build_mask(hsv, ranges):
    mask = None
    for lower, upper in ranges:
        partial = cv2.inRange(hsv, lower, upper)
        mask = partial if mask is None else cv2.bitwise_or(mask, partial)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, KERNEL)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, KERNEL)
    return mask


# HSV 이미지에서 가장 큰 원형 객체의 색상을 감지
def detect_color(hsv):
    largest_color = ""
    largest_area = 0
    for color, ranges in COLOR_RANGES.items():
        mask = build_mask(hsv, ranges)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 1000: # 너무 작은 객체는 무시
                continue
            perimeter = cv2.arcLength(cnt, True)
            if perimeter == 0:
                continue
            circularity = 4 * np.pi * area / (perimeter ** 2)
            if circularity > 0.75 and area > largest_area:
                largest_color = color
                largest_area = area
    return largest_color


def main():
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
    time.sleep(2)  # 아두이노 리셋 대기 (없으면 첫 명령이 유실됨)

    cap = cv2.VideoCapture(0)
    object_detected = False
    last_send_time = 0.0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            color = detect_color(hsv)

            now = time.time()
            if color:
                if not object_detected and (now - last_send_time) > COOLDOWN_SEC:
                    ser.write(color.encode())
                    print(f"[전송] {color}")
                    object_detected = True
                    last_send_time = now
            else:
                object_detected = False

            cv2.imshow("camera", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        ser.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()