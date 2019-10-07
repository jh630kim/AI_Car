정방향 2회, 역방향 2회 운전해서 Data 취득
-> 결과는 Success
*** 단, model.py를 원본을 사용해야 한다!!!
    _model.py는 구조에 이름을 붙여 수정했다.

<<< 2_data_analysis.py >>>
Total data counts:  1540
Stop data counts:  0 , ratio(%):  0.0
Left data counts:  403 , ratio(%):  26.2
strait data counts:  734 , ratio(%):  47.7
Right data counts:  403 , ratio(%):  26.2

<<< 4_train.py >>
epochs: 130

(회사)
Train Accuracy: 0.99
Validation Accuracy: 0.99
begin:  2019-10-02_12-06-18
end:    2019-10-02_12-30-17

(집)
Train Accuracy: 1.0
Validation Accuracy: 0.91
begin:  2019-10-03_00-13-32
end:    2019-10-03_03-57-22

<<< 5_training_analysis.py >>>
i: 1540 correct_num:  1510 percentage:  98.05194805194806
left_num:  403 correct_left:  396 percentage: 98.3
forward_num:  734 correct_forward:  718 percentage: 97.8
right_num:  403 correct_right:  396 percentage: 98.3

--------------------------
정상 동작되도록 학습한 데이터(data_2)를 이용해서
내가 임의로 배치하고 사진을 찍은 결과(data_1)를 보니...
정확도가 50% 정도로 보인다.
즉, 그때 그렇게 제어하면 안된다는 얘기인가???
뭐지?

i: 130 correct_num:  70 percentage:  53.84615384615385
left_num:  37 correct_left:  20 percentage: 54.1
forward_num:  56 correct_forward:  34 percentage: 60.7
right_num:  37 correct_right:  16 percentage: 43.2
