"""
-t 0 -c 0.5
Accuracy = 81.25% (182/224) (classification)
Accuracy = 47.0588% (16/34) (classification)
Accuracy = 51.7241% (15/29) (classification)

-t 0 -c 1
Accuracy = 83.0357% (186/224) (classification)
Accuracy = 55.8824% (19/34) (classification)
Accuracy = 51.7241% (15/29) (classification)

-t 0 -c 2
Accuracy = 87.5% (196/224) (classification)
Accuracy = 50% (17/34) (classification)
Accuracy = 51.7241% (15/29) (classification)

-t 1 -c 1
Accuracy = 100% (224/224) (classification)
Accuracy = 44.1176% (15/34) (classification)
Accuracy = 55.1724% (16/29) (classification)

-t 2 -c 1
Accuracy = 98.2143% (220/224) (classification)
Accuracy = 50% (17/34) (classification)
Accuracy = 62.069% (18/29) (classification)

taskA:2
-t 0 -c 0.5
Accuracy = 81.25% (182/224) (classification)
Accuracy = 47.0588% (16/34) (classification)
Accuracy = 51.7241% (15/29) (classification)

-t 0 -c 1
Accuracy = 83.0357% (186/224) (classification)
Accuracy = 55.8824% (19/34) (classification)
Accuracy = 51.7241% (15/29) (classification)

-t 0 -c 2
Accuracy = 87.5% (196/224) (classification)
Accuracy = 50% (17/34) (classification)
Accuracy = 51.7241% (15/29) (classification)

-t 1 -c 1
Accuracy = 100% (224/224) (classification)
Accuracy = 44.1176% (15/34) (classification)
Accuracy = 55.1724% (16/29) (classification)

-t 2 -c 1
Accuracy = 98.2143% (220/224) (classification)
Accuracy = 50% (17/34) (classification)
Accuracy = 62.069% (18/29) (classification)


"""

./svm-train -t 0 -c 1 train_taskB.data modelB.train
./svm-predict train_taskB.data modelB.train predict.trainB
./svm-predict dev_taskB.data modelB.train predict.devB
./svm-predict test_taskB.data modelB.train predict.testB

