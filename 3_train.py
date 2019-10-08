import tensorflow as tf
import numpy as np

import os
import time
import random

import _config as cfg
import _util as util

import _model_2_100x30 as model

''' ===<< 확인사항 >> +========== '''
'''
    1) config.py: dataDir, append_saveData
    2) util.py: 적용 model
    2) train.py: 적용 model
'''
''' ============================= '''

''' ============================= '''
''' 시작 시간 기록 '''
''' ============================= '''
begin = time.strftime('%Y-%m-%d_%H-%M-%S')

''' ============================= '''
''' training set과 test set의 분리 '''
''' ============================= '''
# 전체 Data 읽기
dataSet = util.ReadCSV(cfg.dataFile)
total_num = len(dataSet)

# Data 섞기
random.shuffle(dataSet)

# Train Dataset
trainSet = np.array(dataSet[:int(total_num * 0.8)])
train_num = len(trainSet)
util.WriteCSV(file_name=cfg.trainFile, datalist=trainSet)

# Test Dataset
testSet = np.array(dataSet[-int(total_num * 0.2):])
test_num = len(testSet)
util.WriteCSV(file_name=cfg.testFile, datalist=testSet)

# 한번에 전체 이미지를 로드하면 시스템이 죽는다!!!
# x_img_train = util.LoadImgData(trainSet)  # img 추출
# x_img_test = util.LoadImgData(testSet)  # img 추출

''' ============================= '''
''' 초기 설정 '''
''' ============================= '''
# Logging Type 지정
tf.logging.set_verbosity(tf.logging.ERROR)

# 학습 데이터 저장소
saver = tf.train.Saver(write_version=tf.train.SaverDef.V2)

# sess = tf.InteractiveSession()
sess = tf.Session()
sess.run(tf.global_variables_initializer())

# 이전 학습 데이터 Restore 후 이어서 학습(if append_saveData is True)
if cfg.append_saveData and os.path.exists(cfg.saveData):
    saver.restore(sess, cfg.saveData + "/model.ckpt")  # 이전 결과 Restore
    print('---------------------------------')
    print("### Load save Data ###")
    print('---------------------------------')

# 초기 Directory가 없다면 새로 생성
if not os.path.exists(cfg.saveData):
    os.makedirs(cfg.saveData)
if not os.path.exists(cfg.logData):
    os.makedirs(cfg.logData)

''' ============================= '''
''' tf를 이용해서 trainFile 읽기 '''
''' ============================= '''
# 1) list를 이용해서 queue 생성
filename_queue = tf.train.string_input_producer(
         string_tensor=[cfg.trainFile], shuffle=False)

# 2) queue에서 next record pair를 제공
key, value = tf.TextLineReader().read(filename_queue)

# 3) record default와 같은 형태의 tensor를 return
xy = tf.decode_csv(value,
                   record_defaults=[['NA_1'], ['NA_2']],
                   field_delim=',')

# 4) output을 batch_size 만큼씩 가져온다.
xb_img_name, yb_steering = tf.train.batch([xy[0:-1], xy[-1:]],
                                          batch_size=cfg.batch_size)

# 5) batch 상용구
coord = tf.train.Coordinator()
threads = tf.train.start_queue_runners(sess=sess, coord=coord)

''' ============================= '''
''' 학습시작 '''
''' ============================= '''
''' Training 시작 '''
for epoch in range(cfg.epochs):
    avg_cost = 0
    sum_accuracy = 0.0
    train_batch = int(train_num/cfg.batch_size)
    # batch 반복
    for i in range(train_batch):
        # 6) batch size만큼 가져오기
        x_batch, y_batch = sess.run([xb_img_name, yb_steering])

        # xs_img 생성, xb_img_name은 image의 이름이다!!!
        x_img_batch = util.LoadImgData(x_batch)

        # cost, train 실행
        c, _ = sess.run([model.cost, model.train],
                        feed_dict={model.X: x_img_batch, model. Y: y_batch,
                                   model.keep_prob: 0.7})

        a = sess.run(model.accuracy,
                     feed_dict={model.X: x_img_batch, model. Y: y_batch,
                                model.keep_prob: 1.0})

        # 평균 cost 계산
        avg_cost += c / train_batch
        sum_accuracy += a

        # (4) summary를 writer에 추가 - TensorBoard 기록을 위한 logs 기록
        s = sess.run(model.merged_summary,
                     feed_dict={model.X: x_img_batch, model.Y: y_batch,
                                model.keep_prob: 1.0})
        global_step = epoch * train_batch + i
        model.summary_writer.add_summary(s, global_step=global_step)

        # 각 batch에 대한 cost print(중간결과)
        print("- Epoch: %04d, Step: %04d, cost: %.7f, accuracy: %3d%%"
              % (epoch + 1, i, c, a*100))
    avg_accuracy = sum_accuracy * 100 / train_batch
    # 각 epoch에 대한 cost print(중간결과)
    print('Epoch: %04d, avg_cost: %.7f, avg_accuracy: %.2f%%'
          % (epoch + 1, avg_cost, avg_accuracy))

    # 1회 배치 학습이 끝나면 모델 저장
    checkpoint_path = os.path.join(cfg.saveData, "model.ckpt")
    filename = saver.save(sess, checkpoint_path)
    print("Model saved in file: %s" % filename)

''' 소요시간 기록 '''
end = time.strftime('%Y-%m-%d_%H-%M-%S')
print('begin: ', begin)
print('end: ', end)

''' TensorBoard 사용법 기록 '''
print("Run the command line:\n"
      "--> tensorboard --logdir=./logs --port=6006"
      "\nThen open localhost:6006/ into your web browser")
