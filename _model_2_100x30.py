import tensorflow as tf
# import numpy as np
import _config as cfg


model_name = 'model_JHK'
img_width = 100  # 200  # 320  # 320 # Resized Video width to be handled
img_height = 30  # 66  # 150  # 150 # Resized Video height to be handled


def weight(name, shape, w_type = 0):
    if w_type == 1:
        w = tf.get_variable(name=name, shape=shape,
                            initializer=tf.contrib.layers.xavier_initializer())
    elif w_type == 2:
        pass
    else:
        w = tf.Variable(tf.random_normal(shape, stddev=0.01))
    return w


def bias(name, shape, b_type = 0):
    if b_type == 1:
        b = tf.Variable(tf.random_normal(shape=shape), name=name)
    elif b_type == 2:
        pass
    else:
        b = tf.Variable(tf.constant(0.1, shape=shape), name=name)
    return b

    
''' ============================= '''
''' 변수 설정 '''
''' ============================= '''
# 출력
nb_classes = cfg.nb_classes  #0, R1, R2, S3, L4, L5
# Learning
learning_rate = cfg.learning_rate  #  0.5e-3    # 1e-3

# 입출력
# X = image수 x 가로 이미지 x 세로 이미지 x 색상
X = tf.placeholder(tf.float32, 
#                   shape=[None, cfg.img_height, cfg.img_width, 3],
                   shape=[None, img_height, img_width, 3],
                   name='X')
# Y(목표값, 1 ~ 5) -> Yoh(Onehot 방식의 목표값 표시, 
# ex:Y = 3 -> Yoh = [0,0,0,1,0,0]
# Y = tf.placeholder(tf.float32, shape=[None, 1])
Y = tf.placeholder(tf.int32, shape=[None, 1], name='Y')
Yoh = tf.one_hot(indices=tf.reshape(tf.cast(Y, tf.int32), [-1]),
                 depth=nb_classes)
# dropout rate
keep_prob = tf.placeholder(tf.float32, name="keep_prob")

''' ============================= '''
''' 모델 설정 '''
''' ============================= '''
# (1) layer 1의 scope 지정
# Img In shape = (?, 150, 320, 3)
with tf.name_scope("CNN_1") as scope:
    shape = [3, 3, 3, 32]  # 가로필터 x 세로필터 x 색상 x 필터수
    W1 = weight(name="W1", shape=shape, w_type = 0)
    
    L1 = tf.nn.conv2d(X, W1, strides=[1, 2, 2, 1], padding='SAME')
    L1 = tf.nn.relu(L1)
    L1 = tf.nn.max_pool(L1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1],
                        padding='SAME')
    L1 = tf.nn.dropout(L1, keep_prob=keep_prob)
    '''
    X.shape         = (?, 150, 320,  3)
    conv2d.shape    = (?,  75, 160, 32)
    L1.MaxPool.shape   = (?,  38,  80, 32)
    '''

# Img In shape = L1.MaxPool.shape
with tf.name_scope("CNN_2") as scope:
    shape = [3, 3, 32, 64]  # 가로필터 x 세로필터 x 색상 x 필터수
    W2 = weight(name="W2", shape=shape, w_type = 0)
    
    L2 = tf.nn.conv2d(L1, W2, strides=[1, 2, 2, 1], padding='SAME')
    L2 = tf.nn.relu(L2)
    L2 = tf.nn.max_pool(L2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1],
                        padding='SAME')
    L2 = tf.nn.dropout(L2, keep_prob=keep_prob)
    '''
    L1.shape        = (?, 38,  80, 32)
    conv2d.shape    = (?, 19,  40, 64)
    L2.MaxPool.shape   = (?, 10,  20, 64)
    '''

# Img In shape = L2.MaxPool.shape
with tf.name_scope("CNN_3") as scope:
    shape = [3, 3, 64, 128]  # 가로필터 x 세로필터 x 색상 x 필터수
    W3 = weight(name="W3", shape=shape, w_type = 0)
    
    L3 = tf.nn.conv2d(L2, W3, strides=[1, 1, 1, 1], padding='SAME')
    L3 = tf.nn.relu(L3)
    L3 = tf.nn.max_pool(L3, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1],
                        padding='SAME')
    L3 = tf.nn.dropout(L3, keep_prob=keep_prob)
    '''
    L2.shape        = (?, 10,  20,  64)
    conv2d.shape    = (?, 10,  20, 128)
    MaxPool.shape   = (?,  5,  10, 128)
    '''
    L3_flat = tf.reshape(L3, [-1, 1 * 4 * 128])

with tf.name_scope("FCL_1") as scope:
    shape = [1 * 4 * 128, 625]  # L3의 모든 pixel x 중간 노드
    W4 = weight(name="W4", shape=shape, w_type = 0)
    shape = [625]  # 중간 노드
    b4 = bias('b4', shape, b_type=1)
    
    L4 = tf.matmul(L3_flat, W4) + b4
    L4 = tf.nn.dropout(L4, keep_prob=keep_prob)
    '''
    L4.shape        = (?, 4*10*128)
    matmul.shape    = (???, ???)
    '''
    
with tf.name_scope("FCL_2") as scope:
    shape = [625, nb_classes]  # 중간 노드 x 출력 노드
    W5 = weight(name="W5", shape=shape, w_type = 0)
    shape = [nb_classes]  # 출력 node
    b5 = bias('b5', shape, b_type=1)
    
    L5 = tf.matmul(L4, W5) + b5
# 마지막 Layer...
# H = L5  # logits
Y_ = L5

''' ============================= '''
''' cost, train, accuracy 설정 '''
''' ============================= '''
cost = tf.reduce_mean(
        tf.nn.softmax_cross_entropy_with_logits(logits=Y_, labels=Yoh))
train = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

''' 정확도 측정 '''
is_correct = tf.equal(tf.argmax(Yoh, 1), tf.argmax(Y_, 1))
accuracy = tf.reduce_mean(tf.cast(is_correct, tf.float32))


# create a summary to monitor cost tensor
tf.summary.scalar("cost", cost)
tf.summary.scalar("accuracy", accuracy)
# tf.summary.scalar("accuracy", accuracy)
merged_summary = tf.summary.merge_all()
summary_writer = tf.summary.FileWriter(cfg.logData,
                                       graph=tf.get_default_graph())

print('---------------------------------')
print('### New Model Read Completed. ###')
print('---------------------------------')
