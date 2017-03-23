#coding=utf-8
#-*- coding: UTF-8 -*- 
import sys
sys.path.append('tools/')
import numpy as np
import pandas as pd
from IO import *
import lxml.etree


def loadData(dataPath, goldPath=None, goldYNPath=None) :
    assert ((goldPath is None) is (goldYNPath is None))
    if not goldPath is None :
        goldPath = {line.split('\t')[0]:line.split('\t')[1] for line in loadLists(goldPath,ignoreEndingLength=2)}
        goldYNPath = {line.split('\t')[0]:line.split('\t')[1] for line in loadLists(goldYNPath,ignoreEndingLength=2)}

    doc = lxml.etree.parse(dataPath)
    Questions = []
    for node in doc.xpath('//Question') :
        Question_t = {}
        Question_t['QID']       = node.xpath('@QID')[0]
        Question_t['QCATEGORY'] = node.xpath('@QCATEGORY')[0]
        Question_t['QDATE']     = node.xpath('@QDATE')[0]
        Question_t['QUSERID']   = node.xpath('@QUSERID')[0]
        Question_t['QTYPE']     = node.xpath('@QTYPE')[0]
        Question_t['QSubject']  = node.xpath('QSubject/text()')[0]
        Question_t['QBody']     = node.xpath('QBody/text()')[0]
        if Question_t['QTYPE'] == 'YES_NO' :
            Question_t['QGOLD_YN'] = node.xpath('@QGOLD_YN')[0] if goldYNPath is None else goldYNPath[Question_t['QID']]

        comment_all = []
        for comment in node.xpath('Comment') :
            comment_t = {}
            comment_t['CID']      = comment.xpath('@CID')[0]
            comment_t['CUSERID']  = comment.xpath('@CUSERID')[0]
            comment_t['CSubject'] = comment.xpath('CSubject/text()')[0]
            comment_t['CBody']    = comment.xpath('CBody/text()')[0]
            comment_t['CGOLD_YN'] = comment.xpath('@CGOLD_YN')[0] if goldPath is None else goldPath[comment_t['CID']]
            comment_all.append(comment_t)
        Question_t['comments'] = comment_all
        
        Questions.append(Question_t)
    return Questions

if __name__ == '__main__':
    trn_data = loadData('../data/raw/CQA-QL-train.xml')
    dev_data = loadData('../data/raw/CQA-QL-devel-input.xml','../data/raw/CQA-QL-devel-gold.txt','../data/raw/CQA-QL-devel-gold-yn.txt')
    tst_data = loadData('../data/raw/test_task3_English.xml','../data/raw/CQA-QL-test-gold.txt','../data/raw/CQA-QL-test-gold-yn.txt')

    print len(trn_data)
    print len(dev_data)
    print len(tst_data)

    writeListofDict('../data/train.json', trn_data, mainKey='QID')
    writeListofDict('../data/dev.json', dev_data, mainKey='QID')
    writeListofDict('../data/test.json', tst_data, mainKey='QID')







