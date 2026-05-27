#include <Servo.h>

Servo servo1; // 하단 모터
Servo servo2;
Servo servo3;
Servo servo5; // 엔드 이펙터

int tt=8;
// 시작 자세 각도
int natural = 90;

// 박스 위치 각도
int RED_POS   = 120;    // 왼쪽 30도
int GREEN_POS = 270;    // 정면
int BLUE_POS  = 60;   // 오른쪽 30도

void setup() {

  Serial.begin(9600);

  servo1.attach(3);
  servo2.attach(5);
  servo3.attach(6);
  servo5.attach(10);

  // 초기 자세
  servo1.write(natural);
  servo2.write(natural);
  servo3.write(natural);
  servo5.write(natural);

  delay(2000);
}

void loop() {
  // Python 데이터 도착 확인
  if(Serial.available()) {
    char color = Serial.read();

    // RED
    if(color == 'R') {
      moveBase(RED_POS);
      openEndEffector();
      closeEndEffector();
      moveBase(natural);
    }

    // GREEN
    else if(color == 'G') {
      moveBase(GREEN_POS);
      openEndEffector();
      closeEndEffector();
      moveBase(natural);
    }

    // BLUE
    else if(color == 'B') {
      moveBase(BLUE_POS);
      openEndEffector();
      closeEndEffector();
      moveBase(natural);
    }
  }
}

// 메소드 정의

// 하단 모터 이동
void moveBase(int target) {

  int current = servo1.read();

  // 오른쪽 이동
  if(current < target) {
    for(int x = current; x <= target; x++) {
      servo1.write(x);
      delay(tt);
    }
  }

  // 왼쪽 이동
  else {
    for(int x = current; x >= target; x--) {
      servo1.write(x);
      delay(tt);
    }
  }

  delay(500);
}


// 엔드 이펙터 열기
void openEndEffector() {
  
  for(int b = 90; b >= 0; b--) {
    servo5.write(b);
    delay(tt);
  }

  delay(1000);
}


// 엔드 이펙터 닫기
void closeEndEffector() {

  for(int b = 0; b <= 90; b++) {
    servo5.write(b);
    delay(tt);
  }

  delay(1000);
}
