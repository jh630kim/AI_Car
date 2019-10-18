import tensorflow as tf
import numpy as np
import cv2
import os
import matplotlib.pyplot as plt

import _config as cfg
import _util as util
import _model_2_100x30 as model

'''
    1) config.py: dataDir
    2) util.py: 적용 model
    2) train_result.py: 적용 model
'''

''' ============================= '''
''' test set 읽기(목록!!!) '''
''' ============================= '''
# 전체 Data 읽기
testSet = util.ReadCSV(cfg.testFile)
testSet = np.array(testSet)
test_num = len(testSet)

''' ============================= '''
''' 초기 설정 '''
''' ============================= '''
# Logging Type 지정
# tf.logging.set_verbosity(tf.logging.ERROR)

# 학습 데이터 저장소
saver = tf.train.Saver()

# sess = tf.InteractiveSession()
sess = tf.Session()
sess.run(tf.global_variables_initializer())

# 학습 결과 data를 읽음
saver.restore(sess, cfg.saveData + "/model.ckpt")
print('---------------------------------')
print("### Load save Data ###")
print('---------------------------------')

''' ============================= '''
''' Test '''
''' ============================= '''
num = np.zeros(cfg.nb_classes, dtype=np.int32)  # nb_classes = 6
correct = np.zeros(cfg.nb_classes, dtype=np.int32)
num_total = 0
correct_total = 0

# 초기 Directory가 없다면 새로 생성
if not os.path.exists(cfg.trainData + '/PASS/'):
    os.makedirs(cfg.trainData + '/PASS/')
if not os.path.exists(cfg.trainData + '/FAIL/'):
    os.makedirs(cfg.trainData + '/FAIL/')

''' 각 방향별 정확도 확인 '''
for i in range(test_num):
    image = util.LoadImgData(testSet[i:i+1])
    steering = int(testSet[i, 1])

    predict = model.Y_.eval(session=sess,
                            feed_dict={model.X: image, model.keep_prob: 1.0})
    predict = np.argmax(predict)

    num[steering] += 1

    # 성공을 count하고, 성공과 실패에 따라 이미지 저장
    if predict == steering:
        correct[predict] += 1
        cv2.imwrite(cfg.trainData + '/PASS/' + cfg.str_steering[0][predict] +
                    '(-' + testSet[i:i+1, 0][0],
                    image[0] * 255)  # cv2로 저장할때는 255를... scipy와 다르다.
    else:
        cv2.imwrite(cfg.trainData + '/FAIL/' + cfg.str_steering[0][predict] +
                    '(-' + testSet[i:i+1, 0][0],
                    image[0] * 255)  # cv2로 저장할때는 255를... scipy와 다르다.

''' 각 방향별 정확도 출력 '''
for i in range(1, cfg.nb_classes):
    print("%s: %d/%d, accuracy: %.2f%%"
          % (cfg.str_steering[0][i], correct[i], num[i],
             correct[i]/num[i].astype(float)*100))
    num_total += num[i]
    correct_total += correct[i]

''' 평균 정확도 출력 '''
print("Total: %d/%d, accuracy: %.2f%%"
      % (correct_total, num_total,
         correct_total/num_total.astype(float)*100))

'''
    # image 그리기
    for i in range(cfg.batch_size):
        plt.subplot(4, 2, i+1)
        plt.imshow(x_img[i], cmap='Greys')

    plt.show()
'''
