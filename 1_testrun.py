"""
    19.10.1
    Steering wheel을 부드럽게 움직이게 하는 코드(analog 방식)
    그러나, 여전히 왼쪽 오른족은 2, 3으로만 저장한다.
    학습을 시켜도 동작시킬 방법이 없다.

    학습은 조금 더 생각 해 보고...
    일단은, 좌 우 고정 각도로 wheel을 움직이는 코드를 짜 보자.

    servo를 stop 시키고 다시 start 시키면 wheel이 이상한 방향으로 꺽인다.
    원인을 알 수 없어서 구동 모터만 start/stop 시키고,
    servo는 항상 on 시켜둔다.
    -> 이거 원인 수정된 거 같은데... 그냥 두자.    
"""
import time
import cv2
import csv

import _config as cfg
import _driver_OPi as d
# mport _driver_Win as d

''' global 변수 '''
img_cnt = 0
start_flag = False
rec_flag = False


def save_image(steering, fwriter):
    ''' Steering wheel이 stop(0)이 아닌 경우 이미지 저장 '''
    global img_cnt
    global start_flag

    if start_flag is True:
        myfile = cfg.str_steering[0][steering] + '_' + time.strftime('%Y-%m-%d_%H-%M-%S')\
                + '_' + str(img_cnt) + '.jpg'
        print(myfile)

        # lsit.csv 파일에 이미지 이름과 wheel 방향을 저장
        fwriter.writerow((myfile, steering))

        # 현재 이미지를 파일로 저장
        cv2.imwrite(cfg.trainData + '/' + myfile, full_image)

        # 이미지의 일련번호 증가
        img_cnt += 1


if __name__ == '__main__':

    ''' 초기값 설정 '''
    # 차량 속도(wheel speed) 와 Steering 방향(sevo_angle) 설정
    run_flag = cfg.run_mode
    pre_wheel_speed = wheel_speed = 0
    steering = 3
    servo_angle = cfg.servo_angle[steering]
    print(cfg.str_steering[1][steering], ':', servo_angle)
    fwriter = ''

    # PWM Start
    d.startPWM()

    # 화면 Sizefmf 320 x 240으로 설정
    c = cv2.VideoCapture(0)
    c.set(cv2.CAP_PROP_FRAME_WIDTH, cfg.cam_width)  # 320
    c.set(cv2.CAP_PROP_FRAME_HEIGHT, cfg.cam_height)  # 240

    print("Check Data Set: ", cfg.dataDir)
    while(True):
        # roop time 확인
        # print("time :", time.time() - start)
        # start =time.time()

        # 이미지 capture 및 Display
        _, full_image = c.read()
        cv2.imshow('frame', full_image)

        # Key 입력 read
        k = cv2.waitKey(5)

        # help
        if k == ord('h'):
            print("h : r -> s for recoring, s for test run\r\n"
                  "s : start/stop vehichl\r\n"
                  "r : record image on/off\r\n"
                  "q : quit\r\n")

        # 종료
        if k == ord('q'):
            break

        """ Toggle Start/Stop motor movement """
        if k == ord('s'):
            if start_flag is False:
                start_flag = True
            else:
                start_flag = False
            print('start flag:', start_flag)

        """ Toggle Record On/Off  """
        if k == ord('r'):
            if rec_flag is False:
                rec_flag = True
                img_cnt = 0
                f = open(cfg.trainData+'/list.csv', 'a')
                fwriter = csv.writer(f)
            else:
                rec_flag = False
                f.close()
            print('record flag:', rec_flag)

        """ 주행 중이 아닌 경우 Capture one image"""
        if start_flag is False and rec_flag is True:
            # R1, R2, S3, L4, L5
            if k == 83:  # 1
                if steering > 1:
                    steering -= 1
                save_image(steering, fwriter)
            if k == 81:  # 3
                if steering < 5:
                    steering += 1
                save_image(steering, fwriter)
            if k == 82:
                steering = 3
                save_image(steering, fwriter)

        """ Run """
        if start_flag is True:
            if rec_flag is True and wheel_speed != 0:  # 이미지 파일 저장
                save_image(steering, fwriter)
                print('img count : ', img_cnt)
            # 초음파 센서, 장애물이 있는 경우 Stop
            length = d.get_distance()
            if length < 15:
                wheel_speed = 0
                print('Stopped by UltraSonic sensor')
                time.sleep(0.2)
            else:
                wheel_speed = pre_wheel_speed
                # Left arrow: 81, Right arrow: 83, Up arrow: 82, Down arrow: 84
                if k == 83:
                    pre_wheel_speed = wheel_speed = cfg.normal_speed
                    if steering > 1:
                        steering -= 1
                    servo_angle = cfg.servo_angle[steering]
                    print(cfg.str_steering[1][steering], ':', servo_angle)

                if k == 81:
                    pre_wheel_speed = wheel_speed = cfg.normal_speed
                    if steering < 5:
                        steering += 1
                    servo_angle = cfg.servo_angle[steering]
                    print(cfg.str_steering[1][steering], ':', servo_angle)

                if k == 82:
                    pre_wheel_speed = wheel_speed = cfg.normal_speed
                    steering = 3
                    servo_angle = cfg.servo_angle[steering]
                    print(cfg.str_steering[1][steering], ':', servo_angle)

            '''
            d.setMotor(d.CH1, wheel_speed)
            d.setMotor(d.CH2, wheel_speed)
            d.setServo(servo_angle)
            '''
        # 정지
        else:
            pre_wheel_speed = wheel_speed = 0
            steering = 3
            servo_angle = cfg.servo_angle[steering]

        d.setMotor(d.CH1, wheel_speed)
        d.setMotor(d.CH2, wheel_speed)
        d.setServo(servo_angle)

d.stopGPIO()
cv2.destroyAllWindows()
