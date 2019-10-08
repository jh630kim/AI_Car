import numpy as np
import scipy.misc

import csv

import _config as cfg

import _model_2_100x30 as model


def LoadImgData(dataSet):
    # dataSet ([0]img_file, [1]steering)을 이용해 img_data를 Load
    img_list = []
    for i in range(len(dataSet)):
        file_path = cfg.trainData + '/' + dataSet[i].astype(str)[0]
        full_image = scipy.misc.imread(file_path, mode="RGB")
        img_list.append(scipy.misc.imresize
                        (full_image[cfg.trim_height:],  # image
                         [model.img_height, model.img_width])  # img size
                        / 255.0)  # 정규화 (0 ~ 1)
    img_list = np.array(img_list)  # accuracy에 feed로 넣기 위해 nparray로 변환
    return img_list


def ReadCSV(file_name):
    # csv file에서 목록을 읽어 datalist로 반환
    datalist = []
    with open(file_name, newline='') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in filereader:
            datalist.append(row)
    return datalist


def WriteCSV(file_name, datalist):
    # datalist를 csv file에 저장
    with open(file_name, 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|')
        filewriter.writerows(datalist)


def AppendCSV(file_name, datalist):
    # datalist를 csv file에 저장
    with open(file_name, 'a', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|')
        filewriter.writerows(datalist)


def current_steering(steering):
    ''' 현재 steering의 위치에 따른 servo_angle 변환 '''
    servo_angle = cfg.servo_angle[steering]
    str_steering = cfg.str_steering[[0], [steering]]
    print(cfg.str_steering[[1], [steering]])

    return servo_angle, str_steering
