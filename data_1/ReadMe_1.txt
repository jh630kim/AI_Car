임의로 자동차를 배치, 그에 따른 조작값 입력
여러가지 가능한 경우의 수를 생각해서 배치함
선에서 벗어나는 경우도 고려해서 조작값 입력

-> 결과는 Fail

<<< 2_data_analysis.py >>>
Total data counts:  130
Stop data counts:  0 , ratio(%):  0.0
Left data counts:  37 , ratio(%):  28.5
strait data counts:  56 , ratio(%):  43.1
Right data counts:  37 , ratio(%):  28.5

<<< 4_train.py >>
epochs: 130
Train Accuracy: 0.94
Validation Accuracy: 0.73
begin:  2019-10-03_13-44-50
end:    2019-10-03_14-10-51

<<< 5_training_analysis.py >>>
i: 130 correct_num:  33 percentage:  25.384615384615383
left_num:  37 correct_left:  0 percentage: 0.0
forward_num:  56 correct_forward:  33 percentage: 58.9
right_num:  37 correct_right:  0 percentage: 0.0