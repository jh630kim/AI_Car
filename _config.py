""" 디렉토리 선언 """
epochs = 150
batch_size = 100

append_saveData = True      # False: save data를 지우고 새로 생성
                             # True : 기존 save data에 이어서 학습

dataDir = './data_model2/'

trainData = dataDir + 'training'   # trainingDir
logData = dataDir + 'logs'
saveData = dataDir + 'save'

dataFile = trainData + '/list.csv'
trainFile = trainData + '/train.csv'
testFile = trainData + '/test.csv'

# 출력
nb_classes = 6  # 0, R1, R2, S3, L4, L5
# Learning
learning_rate = 0.5e-3    # 1e-3

""" R1, R2, S3, L4, L5 """
run_mode = 'digital'    # analog : Steering wheel을 부드럽게 이동
                        # digital : 직진, 좌, 우 중에 선택

# PWM frequency 50Hz 경우의 값
# analog 방식
servo_right = 10
servo_stright = 7.5
servo_left = 5
servo_step = 0.2
# digital 방식
str_steering = [['', 'R1', 'R2', 'S3', 'L4', 'L5'],
                ['', 'RIGHT 1', 'RIGHT2', 'STRAIGHT 3', 'LEFT 4', 'LEFT 5']]
servo_angle = [0, 10.0, 8.5, 7.5, 6.5, 5]
'''
str_steering = [['', 'R1', 'S2', 'L3', 'L4', 'L5'],
                ['', 'RIGHT', 'STARAIGHT', 'LEFT', 'LEFT 4', 'LEFT 5']]
servo_angle = [0, 8.5, 7.5, 6.5, 6.5, 5]

'''
'''
servo_right_d1 = 10.0
servo_right_d2 = 8.5
servo_stright_d3 = 7.5
servo_left_d4 = 6.5
servo_left_d5 = 5
'''

""" image size """
trim_height = 60
cam_width = 320  # Video width from camera
cam_height = 240  # Video height from camera

""" motor speed """
normal_speed = 20  # 40


'''
# analog 방식 확장에 쓸 참조 코드
if k == 83:
    if run_mode == 'analog'
        if servo_angle < g.servo_right:
        servo_angle += g.servo_step

if k == 81:
    if run_mode == 'analog'
        if servo_angle > g.servo_left:
        servo_angle -= g.servo_step
'''
