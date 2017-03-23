#coding=utf-8
#-*- coding: UTF-8 -*- 
import sys
sys.path.append('tools/')
from IO import *

"""
QGOLD_YN and CGOLD should be dicts
#"""
def evaluator(data, QGOLD_YN=None, CGOLD=None):
    data = labelAllGood(data, QGOLD_YN, CGOLD)

    QGOLD_YN_label = ['Yes', 'No', 'Unsure']
    #CGOLD_label = ['Good', 'Bad', 'Potential', 'Dialogue', 'Not English', 'Other']
    CGOLD_label = ['Good', 'Bad', 'Pot.']

    Qlength, QcountTrue, Clength, CcountTrue = 0, 0, 0, 0
    QGOLD_YN_count = {label:{'TP':0,'FP':0,'FN':0} for label in QGOLD_YN_label}
    CGOLD_count = {label:{'TP':0,'FP':0,'FN':0} for label in CGOLD_label}

    for question in data :
        if question['QTYPE'] == 'YES_NO' :
            Qlength += 1
            if question['QGOLD_YN_pre'] == question['QGOLD_YN'] :
                QcountTrue += 1
                QGOLD_YN_count[question['QGOLD_YN']]['TP']+=1
            else :
                for label in QGOLD_YN_label:
                    if question['QGOLD_YN_pre'] == label :
                        QGOLD_YN_count[label]['FP']+=1
                    if question['QGOLD_YN'] == label :
                        QGOLD_YN_count[label]['FN']+=1
        for comment in question['comments'] :
            Clength += 1
            if comment['CGOLD_pre'] == comment['CGOLD'] :
                CcountTrue += 1
                CGOLD_count[comment['CGOLD']]['TP']+=1
            else :
                for label in CGOLD_label:
                    if comment['CGOLD_pre'] == label :
                        CGOLD_count[label]['FP']+=1
                    if comment['CGOLD'] == label :
                        CGOLD_count[label]['FN']+=1

    Acc_Q = QcountTrue * 100.0 / Qlength
    Acc_C = CcountTrue * 100.0 / Clength
    average     = lambda x : float(sum(x)) / len(x)
    precision   = lambda r : 0.0 if r['TP'] == 0 else r['TP']*100.0/(r['TP']+r['FP'])
    recall      = lambda r : 0.0 if r['TP'] == 0 else r['TP']*100.0/(r['TP']+r['FN'])
    F1_Score    = lambda p, r : 0.0 if p * r == 0 else 2.0 * p * r / (p + r) 

    macro_F1_Q = average([F1_Score(precision(r), recall(r)) for r in dict2list(QGOLD_YN_count)])
    macro_F1_C = average([F1_Score(precision(r), recall(r)) for r in dict2list(CGOLD_count)])

    detail = {
        'Qlength':Qlength,
        'QcountTrue':QcountTrue,
        'Clength':Clength,
        'CcountTrue':CcountTrue,
        'QGOLD_YN_count':QGOLD_YN_count,
        'CGOLD_count':CGOLD_count
    }
    result = {'macro_F1_Q':macro_F1_Q, 'macro_F1_C':macro_F1_C, 'Acc_Q':Acc_Q, 'Acc_C':Acc_C, 'detail':detail}
    return result

# Used to test the 'all good' baseLine
def labelAllGood(data, QGOLD_YN=None, CGOLD=None) :
    convert = {
        'Good':'Good',
        'Bad':'Bad', 
        'Potential':'Pot.', 
        'Dialogue':'Bad', 
        'Not English':'Bad', 
        'Other':'Bad', 
        'direct':'Good', 
        'related':'Pot.', 
        'irrelevant':'Bad'
    }
    for question in data :
        if question['QTYPE'] == 'YES_NO' :
            question['QGOLD_YN_pre'] = 'Unsure' if QGOLD_YN is None else QGOLD_YN[question['QID']]
        for comment in question['comments'] :
            comment['CGOLD_pre'] = 'Good' if CGOLD is None else CGOLD[comment['CID']]
            #"""
            comment['CGOLD_pre'] = convert[comment['CGOLD_pre']]
            comment['CGOLD'] = convert[comment['CGOLD']]
            #"""
    return data

if __name__ == '__main__':
    trn_data = loadListofDict('../data/train.json', output_type='list')
    dev_data = loadListofDict('../data/dev.json', output_type='list')
    tst_data = loadListofDict('../data/test.json', output_type='list')

    print len(trn_data)
    print len(dev_data)
    print len(tst_data)

    print json.dumps(evaluator(trn_data), ensure_ascii=False, indent=4)
    print json.dumps(evaluator(dev_data), ensure_ascii=False, indent=4)
    print json.dumps(evaluator(tst_data), ensure_ascii=False, indent=4)