
#./svm-train -t 0 -c 0.5 train.data model.train
#./svm-predict train_taskA.data model.train predict.train
#./svm-predict dev.data model.train predict.dev
#./svm-predict test.data model.train predict.test



./svm-train -t 0 -c 0.5 train_taskA2.data model2.train
./svm-predict train_taskA2.data model2.train predict.train2
./svm-predict dev_taskA2.data model2.train predict.dev2
./svm-predict test_taskA2.data model2.train predict.test2
