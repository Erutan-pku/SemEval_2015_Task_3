#coding=utf-8
#-*- coding: UTF-8 -*- 
import sys
sys.path.append('tools/')
import xgboost as xgb
from IO import writeList

if __name__ == '__main__':
    #"""
    dtrain = xgb.DMatrix('../data/train_taskA2.data')
    ddev = xgb.DMatrix('../data/dev_taskA2.data')
    dtest = xgb.DMatrix('../data/test_taskA2.data')
    """
    dtrain = xgb.DMatrix('../data/train_taskB.data')
    ddev = xgb.DMatrix('../data/dev_taskB.data')
    dtest = xgb.DMatrix('../data/test_taskB.data')
    #"""

    param = {
        'objective':'multi:softmax' ,
        'max_depth': 5 ,
        'num_class': 10 ,
        'nthread': 4 ,
        'eta': 0.2,
    }
    watchlist = [(dtrain, 'train'), (ddev, 'dev'), (dtest, 'test')]
    num_round = 50

    bst = xgb.train(param, dtrain, num_round, watchlist)
    
    preds_trn = bst.predict(dtrain)
    preds_dev = bst.predict(ddev)
    preds_tst = bst.predict(dtest)

    convert = lambda x : str(int(x))

    #"""
    writeList('../xgboost/predict.train2', preds_trn, convert=convert)
    writeList('../xgboost/predict.dev2'  , preds_dev, convert=convert)
    writeList('../xgboost/predict.test2' , preds_tst, convert=convert)
    """

    writeList('../xgboost/predict.trainB', preds_trn, convert=convert)
    writeList('../xgboost/predict.devB'  , preds_dev, convert=convert)
    writeList('../xgboost/predict.testB' , preds_tst, convert=convert)
    #"""

