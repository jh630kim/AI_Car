""" 디렉토리 선언 """
epochs = 1
batch_size = 200

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

""" L1, L2, S3, R4, R5 """
run_mode = 'digital'    # analog : Steering wheel을 부드럽게 이동
                        # digital : 직진, 좌, 우 중에 선택

# PWM frequency 50Hz 경우의 값
# analog 방식
servo_right = 10
servo_stright = 7.5
servo_left = 5
servo_step = 0.2
# digital 방식
str_steering = [['', 'L1', 'L2', 'S3', 'R4', 'R5'],
                ['', 'LEFT 1', 'LEFT 2', 'STRAIGHT 3', 'RIGHT 4', 'RIGHT 5']]
servo_angle = [0, 5.0, 6.5, 7.5, 8.5, 10.0]
'''
str_steering = [['', 'R1', 'S2', 'L3', 'L4', 'L5'],
                ['', 'RIGHT', 'STARAIGHT', 'LEFT', 'LEFT 4', 'LEFT 5']]
servo_angle = [0, 8.5, 7.5, 6.5, 6.5, 5]

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
