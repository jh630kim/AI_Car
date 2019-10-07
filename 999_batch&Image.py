import tensorflow as tf
import _config as cfg
import scipy.misc
import csv
import numpy as np
import matplotlib.pyplot as plt

xs = []

with open(cfg.dataFile, newline='') as csvfile:
    f_read = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in f_read:
        xs.append(row[0])
        
train_total = len(xs)

''' tf를 이용해서 list 읽기 '''
# 1) list를 이용해서 queue 생성
filename_queue = tf.train.string_input_producer(
        string_tensor=[cfg.dataFile], shuffle=True, seed=5)

# 2) queue에서 next record pair를 제공
key, value = tf.TextLineReader().read(filename_queue)

# 3) record default와 같은 형태의 tensor를 return
xy = tf.decode_csv(value,
                   record_defaults=[['N/A_1'], ['N/A_2']],
                   field_delim=',')

# 4) output을 batch_size 만큼씩 자르기
xb_img_name, yb_steering = tf.train.batch([xy[0:-1], xy[-1:]],
                                          batch_size=cfg.batch_size)

''' place holder '''
xs = tf.placeholder(tf.float32, shape=[None, 150, 320, 3])
y_ = tf.placeholder(tf.float32, shape=[None, 1])

'''''''''''''''''''''''''''''''''''''''
model
'''''''''''''''''''''''''''''''''''''''
sess = tf.Session()
sess.run(tf.global_variables_initializer())

# 5) batch 상용구
coord = tf.train.Coordinator()
threads = tf.train.start_queue_runners(sess=sess, coord=coord)

for step in range(cfg.epochs * int(train_total / cfg.batch_size)):
    print("step: ", step)
    # 6) batch size만큼 가져오기
    x_batch, y_batch = sess.run([xb_img_name, yb_steering])

    # xs_img 생성, xb_img_name은 image의 이름이다!!!
    x_img = []  # 초기화
    for i in range(cfg.batch_size):
        file_path = cfg.trainData + '/' + x_batch[i].astype(str)[0]
        full_image = scipy.misc.imread(file_path, mode="RGB")
        x_img.append(scipy.misc.imresize(full_image[cfg.trim_height:],
                                         [150, 320]) / 255.0)

    # image 그리기
    for i in range(cfg.batch_size):
        plt.subplot(4, 2, i+1)
        plt.imshow(x_img[i], cmap='Greys')

    plt.show()

# 7) batch 상용구
coord.request_stop()
coord.join(threads)
