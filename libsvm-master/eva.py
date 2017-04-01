#coding=utf-8
#-*- coding: UTF-8 -*- 
import sys
sys.path.append('../src/')
sys.path.append('../src/tools/')
from IO import *
from evaluator import *




if __name__ == '__main__':
    trn_data = loadListofDict('../data/train.json', output_type='list')
    dev_data = loadListofDict('../data/dev.json', output_type='list')
    tst_data = loadListofDict('../data/test.json', output_type='list')

    svm_result_trn_C = loadSVMResult_A('../data/train.json', 'predict.train2')
    svm_result_dev_C = loadSVMResult_A('../data/dev.json'  , 'predict.dev2'  )
    svm_result_tst_C = loadSVMResult_A('../data/test.json' , 'predict.test2' )

    svm_result_trn_Q = loadSVMResult_B('../data/train.json', 'predict.trainB')
    svm_result_dev_Q = loadSVMResult_B('../data/dev.json'  , 'predict.devB'  )
    svm_result_tst_Q = loadSVMResult_B('../data/test.json' , 'predict.testB' )

    trn_result = evaluator(trn_data, QGOLD_YN=svm_result_trn_Q, CGOLD=svm_result_trn_C)
    dev_result = evaluator(dev_data, QGOLD_YN=svm_result_dev_Q, CGOLD=svm_result_dev_C)
    tst_result = evaluator(tst_data, QGOLD_YN=svm_result_tst_Q, CGOLD=svm_result_tst_C)

    #print json.dumps(trn_result, ensure_ascii=False, indent=4)
    print json.dumps(dev_result, ensure_ascii=False, indent=4)
    print json.dumps(tst_result, ensure_ascii=False, indent=4)