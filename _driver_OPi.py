'''
뭐가 문제인지는 모르겠지만...
터미널에서 gpio reset 명령을 주지 않으면
PA18(pin28)이 TWI2_SCK로 사스템에서 사용중이라고 나온다.
한번 gpio reset명령을 주면 괜찮은데...
원인을 모르겠다.
# from pyA20.gpio import gpio as GPIO2
# from pyA20.gpio import port
의 잔재인가???
왜 orangepi를 booting시키면 항상 lesson4의 터미널이 열릴까?
'''

import OPi.GPIO as GPIO
import time

# 모터 채널
CH1 = 0
CH2 = 1

# 실제 핀 정의
# Servo PWM
SERVO = 8   # PA13
# ServoOne = SERVO_PWM(port.PA13, 50, False, "servo_one")

# Motor 1
IN1 = 38  # PG6
IN2 = 36  # PG9
ENA = 40  # PG7
# MotorOne = L298NMDc(port.PG6, port.PG9, port.PG7, 50, False, "motor_one")

# Motor 2
IN3 = 32  # PG8
IN4 = 28  # PA18
ENB = 26  # PA21
# MotorTwo = L298NMDc(port.PG8, port.PA18, port.PA21, 50, False, "motor_two")

# Ultra Sonic
ECHO = 13  # PA0, Echo = port.PA0
TRIG = 11  # PA1, Trig = port.PA1


# PWM 제어를 위한 GPIO 설정
GPIO.setboard(GPIO.PCPCPLUS)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(SERVO, GPIO.OUT)  # PA13, for servo PWM

GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)   # for motor1 IN1
GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)   # for motor1 IN2
GPIO.setup(ENA, GPIO.OUT)   # for motor1 PWM

GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)   # for motor2 IN3
GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)   # for motor2 IN4
GPIO.setup(ENB, GPIO.OUT)   # for motor2 PWM

GPIO.setup(TRIG, GPIO.OUT, initial=GPIO.LOW)  # for ultra sonic TIRG
GPIO.setup(ECHO, GPIO.IN)   # for ultra sonic ECHO

PWM_servo = GPIO.PWM(SERVO, 50)  # channel=8 frequency=50Hz
PWM_motor1 = GPIO.PWM(ENA, 50)  # channel=40 frequency=50Hz
PWM_motor2 = GPIO.PWM(ENB, 50)  # channel=26 frequency=50Hz

print("init GPIO done")


def startPWM():
    # PWM 시작
    PWM_servo.start(0)
    PWM_motor1.start(0)
    PWM_motor2.start(0)


# 모터 제어 함수
def setMotorContorl(pwm, INA, INB, speed):
    # 모터 속도 제어 PWM
    if speed > 0:
        GPIO.output(INA, GPIO.HIGH)
        GPIO.output(INB, GPIO.LOW)
        pwm.ChangeDutyCycle(speed)
    # 뒤로
    elif speed < 0:
        GPIO.output(INA, GPIO.LOW)
        GPIO.output(INB, GPIO.HIGH)
        pwm.ChangeDutyCycle(-speed)
    # 정지
    else:
        GPIO.output(INA, GPIO.LOW)
        GPIO.output(INB, GPIO.LOW)
        pwm.ChangeDutyCycle(-speed)


# 모터 제어함수 간단하게 사용하기 위해 한번더 래핑(감쌈)
def setMotor(ch, speed):
    if ch == CH1:
        # pwmA는 핀 설정 후 pwm 핸들을 리턴 받은 값이다.
        setMotorContorl(PWM_motor1, IN1, IN2, speed)
    else:
        # pwmB는 핀 설정 후 pwm 핸들을 리턴 받은 값이다.
        setMotorContorl(PWM_motor2, IN3, IN4, speed)


# 서보 제어
def setServo(servo_angle):
    PWM_servo.ChangeDutyCycle(servo_angle)


def get_distance():
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG, GPIO.LOW)

    while GPIO.input(ECHO) == 0:
        pass
    start = time.time()

    while GPIO.input(ECHO) == 1:
        pass
    end = time.time()

    elapsed = end - start

    distance_cm = elapsed * 34000
    distance_cm = distance_cm / 2

    # print( "Distance : %.1f" % distance_cm)
    return distance_cm


def stopGPIO():
    GPIO.cleanup()


if __name__ == '__main__':
    startPWM()

    # 모터 정회전 확인, 서보 오른족
    setMotor(CH1, 40)
    setMotor(CH2, 40)
    setServo(10)
    time.sleep(3)

    # 모터 정지
    setMotor(CH1, 0)
    setMotor(CH2, 0)
    setServo(7.5)
    time.sleep(3)

    # 모터 역회전, 서보 왼쪽
    setMotor(CH1, -40)
    setMotor(CH2, -40)
    setServo(5)
    time.sleep(3)

    # 모터 정지
    setMotor(CH1, 0)
    setMotor(CH2, 0)
    setServo(7.5)

    while(True):
        # 초음파 센서 확인
        cm = get_distance()
        print("Distance : %.1f" % cm)
        time.sleep(1)
        k = input("q to quit, other to read distance again:")
        if k == 'q':
            break

    stopGPIO()

    exit()
