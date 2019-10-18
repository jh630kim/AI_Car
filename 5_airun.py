import tensorflow as tf
import numpy as np
import scipy.misc

import cv2
import time

import _config as cfg
import _driver_OPi as d
# import _driver_Win as d

import _model_2_100x30 as model

''' ===<< 확인사항 >> +========== '''
'''
    1) config: dataDir
    2) driver: Win vs OPi
    3) airun: 적용 model
'''
''' ============================= '''


if __name__ == '__main__':
    ''' global 변수 '''
    start_flag = False
    run_flag = cfg.run_mode

    pre_wheel_speed = wheel_speed = 0
    steering = 3
    servo_angle = cfg.servo_angle[steering]

    fwriter = ''

    # PWM Start
    d.startPWM()

    ''' 학습 데이터 읽기 '''
    sess = tf.InteractiveSession()

    saver = tf.train.Saver()
    saver.restore(sess, cfg.saveData + "/model.ckpt")

    c = cv2.VideoCapture(0)
    c.set(cv2.CAP_PROP_FRAME_WIDTH, cfg.cam_width)
    c.set(cv2.CAP_PROP_FRAME_HEIGHT, cfg.cam_height)
    print('---------------------------------')
    print("### Data Set:", cfg.dataDir, "###")
    print('---------------------------------')

    while(True):
        ''' Image Capture & Display from Camera '''
        _, full_image = c.read()
        image = scipy.misc.imresize(full_image[cfg.trim_height:],
                                    [model.img_height, model.img_width]
                                    ) / 255.0
        '''
        disp = scipy.misc.imresize(full_image[cfg.trim_height:],
                                   [model.img_height*2, model.img_width*2]
                                   ) / 255.0
        '''
    
        cv2.imshow("view of AI", image)

        ''' steering 방향 계산 '''
        steering = model.Y_.eval(session=sess,
                                 feed_dict={model.X: [image],
                                            model.keep_prob: 1.0})

        steering = np.argmax(steering, axis=1)
        steering = steering[0]
        print('Steering by AI is',
              cfg.str_steering[1][steering], ':', servo_angle)

        ''' Key 입력 '''
        k = cv2.waitKey(5)
        if k == ord('q'):  # 'q' key to stop program
            break

        """ Toggle Start/Stop motor movement """
        if k == ord('a'):
            if start_flag is False:
                start_flag = True
            else:
                start_flag = False
            print('start flag:', start_flag)

        """ AI Run """
        if start_flag is True:
            # 초음파 센서, 장애물이 있는 경우 Stop
            length = d.get_distance()
            if length < 15:
                wheel_speed = 0
                print('Stopped by UltraSonic sensor')
                time.sleep(0.2)
            # 아닌 경우 Start
            else:
                wheel_speed = pre_wheel_speed
                pre_wheel_speed = wheel_speed = cfg.normal_speed

                servo_angle = cfg.servo_angle[steering]
        else:
            pre_wheel_speed = wheel_speed = 0
            steering = 3
            servo_angle = cfg.servo_angle[steering]

        d.setMotor(d.CH1, wheel_speed)
        d.setMotor(d.CH2, wheel_speed)
        d.setServo(servo_angle)

d.stopGPIO()
cv2.destroyAllWindows()
