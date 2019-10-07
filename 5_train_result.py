import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

import _model_2 as model
import _config as cfg
import _util as util

''' ===<< 확인사항 >> +========== '''
'''
    1) config.py dataDir
    2) util.py 적용 model
'''
''' ============================= '''


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

for i in range(test_num):
    image = util.LoadImgData(testSet[i:i+1])
    predict = model.Y_.eval(session=sess,
                            feed_dict={model.X: image, model.keep_prob: 1.0})
    predict = np.argmax(predict)
    steering = int(testSet[i, 1])

    for j in range(cfg.nb_classes):
        if steering == j:
            num[j] += 1
            if predict == steering:
                correct[j] += 1

steering_name = ['', 'R1', 'R2', 'S3', 'L4', 'L5']
for i in range(1, cfg.nb_classes):
    print("%s: %d/%d, accuracy: %.2f%%"
          % (steering_name[i], correct[i], num[i],
             correct[i]/num[i].astype(float)*100))
    num_total += num[i]
    correct_total += correct[i]

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