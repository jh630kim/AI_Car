정방향 2회, 역방향 2회 운전해서 Data 취득


-> 결과는 
   . (50회 학습)정방향은 잘 가는데 역방향에서 항상 길을 벗어난다.
   . (Train_2)길을 다시 찾아오도록 다른 Dataset으로 학습을 시켰는데...
     더 안좋아 졌다.
   . 추가 Dataset만 이용할 게 아니라 다 써야 하나?
     그럼... 추가된 이미지의 영향이 적을 것 같은데...
   . (130회 학습) 5_training_analysis는 99%가 나오는데도 불구하고
     길을 잘 못찾는다.


<<< 2_data_analysis.py >>>
Total data counts:  1374
Stop data counts:  0 , ratio(%):  0.0
Left data counts:  344 , ratio(%):  25.0
strait data counts:  686 , ratio(%):  49.9
Right data counts:  344 , ratio(%):  25.0
---------------------

<<< 4_train.py >>
epochs: 50

(회사) epochs: 130
Train Accuracy: 0.99
Validation Accuracy: 1.0
begin:  2019-10-04_11-18-46
end:     2019-10-04_11-39-10
(집) epochs: 50
Train Accuracy: 0.96
Validation Accuracy: 0.93
begin:  2019-10-03_16-44-52
end:     2019-10-03_17-58-27

<<< 5_training_analysis.py >>>
(Training_1을 이용해서 130회 학습)
i: 1374 correct_num:  1363 percentage:  99.19941775836972
left_num:  344 correct_left:  340 percentage: 98.8
forward_num:  686 correct_forward:  682 percentage: 99.4
right_num:  344 correct_right:  341 percentage: 99.1

(Training_1을 이용해서 50회 학습)
i: 1374 correct_num:  1188 percentage:  86.46288209606988
left_num:  344 correct_left:  327 percentage: 95.1
forward_num:  686 correct_forward:  536 percentage: 78.1
right_num:  344 correct_right:  325 percentage: 94.5


(training_1 50회, training_2를 이용해서 1회 학습)
i: 1374 correct_num:  1270 percentage:  92.43085880640466
left_num:  344 correct_left:  300 percentage: 87.2
forward_num:  686 correct_forward:  662 percentage: 96.5
right_num:  344 correct_right:  308 percentage: 89.5

그래도!!! Training_1을 이용해서 50회 학습만 한 것이 더 잘 된다.

--------------------------
* training_2는 역방향에서 길을 벗어나는 걸 다시 학습시키기 위해
  몇가지 특정 상황을 임의로 만들 data이다(data_1 처럼)

