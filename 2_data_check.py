import numpy as np

import cv2
import csv

import _config as cfg
import _util as util


''' dataFile을 읽어서 각 steering의 갯수를 count '''
data_list = util.ReadCSV(cfg.dataFile)
steering_sum = np.zeros(6)
total_num = 0
for raw in data_list:
    steering_sum[int(raw[1])] += 1
    total_num += 1

for i in range(1, 6):
    print('{:3}: {:4}/{:4}, {:7.2%}'.
          format(cfg.str_steering[0][i], int(steering_sum[i]), total_num,
                 steering_sum[i]/total_num))

''' mirror image른 만들어서 data set 확장 '''
k = input('Copy a mirror image?(y/n)')
steering_mirror = [0, 5, 4, 3, 2, 1]

if k.upper() == 'Y':
    ''' data File을 읽어서 mirror image를 만듦 '''
    with open(cfg.dataFile, 'a', newline='') as csvfile:
        fwriter = csv.writer(csvfile, delimiter=',', quotechar='|')
        for raw in data_list:
            full_image = cv2.imread(cfg.trainData + '/' + raw[0],
                                    cv2.IMREAD_COLOR)
            full_image = cv2.flip(full_image, 1)
            myfile = cfg.trainData + '/' + '_' + raw[0]
            cv2.imwrite(myfile, full_image)
            fwriter.writerow(('_' + raw[0], steering_mirror[int(raw[1])]))

    ''' dataFile을 읽어서 각 steering의 갯수를 count '''
    data_list = util.ReadCSV(cfg.dataFile)
    steering_sum = np.zeros(6)
    total_num = 0
    for raw in data_list:
        steering_sum[int(raw[1])] += 1
        total_num += 1

    for i in range(1, 6):
        print('{:3}: {:4}/{:4}, {:7.2%}'.
              format(cfg.str_steering[0][i], int(steering_sum[i]), total_num,
                     steering_sum[i]/total_num))
