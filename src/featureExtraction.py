#coding=utf-8
#-*- coding: UTF-8 -*- 
import sys
sys.path.append('tools/')
from IO import *
import nltk
import re
import math
from evaluator import *
"""


t = nltk.word_tokenize('I\'ve done it once at the Sharq Village & Spa ... It\'s great\n\n?!')
t = nltk.word_tokenize('></a>\n\nhttp://www.qatarliving.com/node/31449')
print t

t = nltk.pos_tag(t)
print t
t = nltk.ne_chunk(t)
print t
print type(t)
for i in range(len(t)) :
    print t[i]
print t[6]
print type(t[6]) is tuple
print len(t[6])
"""

global QCATEGORY
QCATEGORY = {}

# 25 features
def getWordFeatures(sentence, post, ner) :
    if len(sentence) == 0 :
        return [0.0]*25

    ret_f = []

    count_left  = sum([(1 if w=='<' else 0) for w in sentence])
    count_right = sum([(1 if w=='>' else 0) for w in sentence])
    ret_f.append(min([count_left, count_right]))

    word_len = [len(word) for word in sentence]
    # length of the max length word
    ret_f.append(max(word_len))
    # average word length
    ret_f.append(float(max(word_len))/len(word_len))
    # word number
    ret_f.append(len(sentence))
    # capital word number
    ret_f.append(sum([(1 if not w[0]==w[0].lower() else 0) for w in sentence]))
    # some word count
    ret_f.append(sum([(1 if w.lower()=='no' else 0) for w in sentence]))
    ret_f.append(sum([(1 if w.lower()=='yes' else 0) for w in sentence]))
    ret_f.append(sum([(1 if w.lower()in['thank','thanks'] else 0) for w in sentence]))
    ret_f.append(sum([(1 if w.lower()=='please' else 0) for w in sentence]))
    ret_f.append(sum([(1 if w.lower()in['may','might','could','can','would','will'] else 0) for w in sentence]))
    ret_f.append(sum([(1 if w.lower()=='?' else 0) for w in sentence]))
    ret_f.append(sum([(1 if w.lower()=='!' else 0) for w in sentence]))

    sentences_num = 0 if sentence[-1] in ['.','?','!'] else 1
    sentences_num += sum([(1 if w in ['.','?','!'] else 0) for w in sentence])
    #average sentence length
    ret_f.append(float(len(word_len))/sentences_num)
    #sentence number.
    ret_f.append(sentences_num)

    # nltk.help.upenn_tagset()
    wh   = ['WDT','WP','WP$','WRB']
    verb = ['VBZ','VBP','VBN','VBG','VBD','VB']
    noun = ['NN','NNP','NNPS','NNS']
    pron = ['PRP','PRP$']
    fw   = ['FW']
    posts = [wh, verb, noun, pron, fw]
    posts_count = [sum([(1 if wp[1] in post_t else 0) for wp in post]) for post_t in posts]
    posts_freq  = [float(x)/len(word) for x in posts_count]
    ret_f += posts_count
    ret_f += posts_freq

    # number of name entity
    ret_f.append(sum([(0 if type(node)is tuple else 1) for node in ner]))
    #rint len(ret_f)
    return ret_f

def getNGrams(sentence):
    unigram = {}
    bigram  = {}
    trigram = {}

    last_big = '_start_\t_start_' 
    last_uni = '_start_'
    for word in sentence :
        # punctuation
        if len(word) == 1 and not word.isalnum():
            last_big = '_start_\t_start_' 
            last_uni = '_start_'
            continue

        uni_t = word
        big_t = last_uni+'\t'+word
        tri_t = last_big+'\t'+word
        if not uni_t in unigram :
            unigram[uni_t] = 0
        if not big_t in bigram :
            bigram[big_t] = 0
        if not tri_t in trigram :
            trigram[tri_t] = 0
        last_big = big_t
        last_uni = uni_t
        unigram[uni_t] += 1
        bigram[big_t] += 1
        trigram[tri_t] += 1
    return unigram, bigram, trigram
def combineNGrams(sentence, unigram, bigram, trigram) :
    uni_t, big_t, tri_t = getNGrams(sentence)
    combineCountDict(unigram, uni_t)
    combineCountDict(bigram, big_t)
    combineCountDict(trigram, tri_t)
def countDcit2list(DictName, leastFrequency = 0) : 
    ret_list = []
    for key in DictName.keys() :
        value = DictName[key]
        if value >= leastFrequency :
            ret_list.append([value, key])
    return ret_list

def getFeatures(question, comment, c_nid) :
    img_label  = re.compile(r'(src=\")?http[^"]*\.(jpg|gif)(\")?')
    http_label = re.compile(r'((src|href)=\")?http[^"]*("| )')

    CBody, c_imgNum = re.subn(img_label, '', comment['CBody'])
    CBody, c_srcNum = re.subn(http_label, '', comment['CBody'])
    QBody, q_imgNum = re.subn(img_label, '', question['QBody'])
    QBody, q_srcNum = re.subn(http_label, '', question['QBody'])

    Features = [c_imgNum, c_srcNum, q_imgNum, q_srcNum]
    words_question = nltk.word_tokenize(QBody)
    words_comment  = nltk.word_tokenize(CBody)
    post_question = nltk.pos_tag(words_question)
    post_comment  = nltk.pos_tag(words_comment)
    ner_question = nltk.ne_chunk(post_question)
    ner_comment  = nltk.ne_chunk(post_comment)

    Features += getWordFeatures(words_question, post_question, ner_question)   # + 25
    Features += getWordFeatures(words_comment, post_comment, ner_comment)      # + 25

    # whether the answer is first, whether the answer is last
    isFirst = (c_nid == 0)
    isLast  = (c_nid == len(question['comments'])-1)
    Features.append(1 if isFirst else 0)
    Features.append(1 if isLast else 0)

    # User id features:
    Features.append(1 if question['QUSERID']==comment['CUSERID'] else 0)
    Features.append(1 if not isFirst and question['comments'][c_nid-1]['CUSERID']==question['QUSERID'] else 0)
    Features.append(1 if not isLast  and question['comments'][c_nid+1]['CUSERID']==question['QUSERID'] else 0)

    # QTYPE
    Features.append(1 if question['QTYPE']=='GENERAL' else 0)
    # QCATEGORY, QCATEGORY_len = 27
    QCATEGORY_len = len(QCATEGORY)
    for i in range(QCATEGORY_len) :
        Features.append(1 if i == QCATEGORY[question['QCATEGORY']] else 0)

    # title
    Features.append(1 if comment['CSubject'] == 'RE: '+question['QSubject'] else 0)

    # nswer and question correlative features
    uni_qu, big_qu, tri_qu = getNGrams(words_question)
    uni_cm, big_cm, tri_cm = getNGrams(words_comment)
    countCross = lambda x,y : sum([0 if not word in y else 1 for word in x])
    dottCross = lambda x,y : sum([0 if not word in y else x[word]*y[word] for word in x])
    pairs = [(uni_qu, uni_cm), (big_qu, big_cm), (tri_qu, tri_cm)]
    for pair in pairs :
        cct = countCross(pair[0], pair[1])
        Features.append(cct)
        Features.append(float(cct)/len(words_question) if not cct == 0 else 0)
        Features.append(float(cct)/len(words_comment) if not cct == 0 else 0)
        dct = dottCross(pair[0], pair[1])
        d0t = dottCross(pair[0], pair[0])
        d1t = dottCross(pair[1], pair[1])
        Features.append(float(dct)/math.sqrt(float(d0t*d1t)) if not dct == 0 else 0)



    Features = [float(x) for x in Features]
    #print len(Features)
    #len(Features) = 100
    return Features

def getLabeledFile_TaskA(data, outputFile, limit=False) :
    labelList = ['Good', 'Bad', 'Potential', 'Dialogue', 'Not English', 'Other', 'direct', 'related', 'irrelevant']
    labelList_r = {label:index for index, label in enumerate(labelList)}
    convert = {
        'Good':'Good',
        'Bad':'Bad', 
        'Potential':'Potential', 
        'Dialogue':'Bad', 
        'Not English':'Bad', 
        'Other':'Bad', 
        'direct':'Good', 
        'related':'Potential', 
        'irrelevant':'Bad'
    }
    getLabel = (lambda x : labelList_r[x]) if not limit else (lambda x : labelList_r[convert[x]])

    output = codecs.open(outputFile, "w", "utf-8")
    for question in data :
        for i, comment in enumerate(question['comments']) :
            feature_t = getFeatures(question, comment, i)
            output.write('%d'%(getLabel(comment['CGOLD'])))
            for j, fea in enumerate(feature_t) :
                if fea == 0 :
                    continue
                output.write(' %d:%.4f'%(j+1, fea))
            output.write('\n')
    output.flush()
    output.close()

def getLabeledFile_TaskB(data, outputFile) :
    labelList = ['Yes', 'No', 'Unsure']
    labelList_r = {label:index for index, label in enumerate(labelList)}

    output = codecs.open(outputFile, "w", "utf-8")
    for question in data :
        if not question['QTYPE'] == 'YES_NO' :
            continue
        feature_t_list = []
        for i, comment in enumerate(question['comments']) :
            if not comment['CGOLD'] == 'Good' :
                continue
            feature_t_list.append(getFeatures(question, comment, i))
        feature_t = [0.]*100
        for fea in feature_t_list:
            for i in range(len(feature_t)) :
                feature_t[i] += fea[i] / len(feature_t_list)
        output.write('%d'%(labelList_r[question['QGOLD_YN']]))
        for j, fea in enumerate(feature_t) :
            if fea == 0 :
                continue
            output.write(' %d:%.4f'%(j+1, fea))
        output.write('\n')
    output.flush()
    output.close()

        

if __name__ == '__main__':
    trn_data = loadListofDict('../data/train.json', output_type='list')
    dev_data = loadListofDict('../data/dev.json', output_type='list')
    tst_data = loadListofDict('../data/test.json', output_type='list')

    unigram = {}
    bigram  = {}
    trigram = {}
    for data in [trn_data, dev_data, tst_data] :
        for question in data :
            #words_question = nltk.word_tokenize(question['QBody'].lower())
            #combineNGrams(words_question, unigram, bigram, trigram)
            if not question['QCATEGORY'] in QCATEGORY :
                QCATEGORY[question['QCATEGORY']] = len(QCATEGORY)
            #for comment in question['comments'] :
                #words_comment  = nltk.word_tokenize(comment['CBody'].lower())
                #combineNGrams(words_comment, unigram, bigram, trigram)
    """
    print len(unigram)
    print len(bigram)
    print len(trigram)
    leastFrequency = 1
    unigram = countDcit2list(unigram, leastFrequency)
    bigram = countDcit2list(bigram, leastFrequency)
    trigram = countDcit2list(trigram, leastFrequency)
    print len(unigram)
    print len(bigram)
    print len(trigram)
    
    unigram = sorted(unigram, reverse=True)
    bigram  = sorted(bigram,  reverse=True)
    trigram = sorted(trigram, reverse=True)
    print trigram[0]
    #"""

    #getLabeledFile_TaskA(trn_data, '../data/train_taskA.data')
    #getLabeledFile_TaskA(dev_data, '../data/dev_taskA.data')
    #getLabeledFile_TaskA(tst_data, '../data/test_taskA.data')

    #getLabeledFile_TaskA(trn_data, '../data/train_taskA2.data', limit=True)
    #getLabeledFile_TaskA(dev_data, '../data/dev_taskA2.data'  , limit=True)
    #getLabeledFile_TaskA(tst_data, '../data/test_taskA2.data' , limit=True)
    #"""
    svm_result_trn_C = loadSVMResult_A('../data/train.json', '../libsvm-master/predict.train2')
    svm_result_dev_C = loadSVMResult_A('../data/dev.json'  , '../libsvm-master/predict.dev2'  )
    svm_result_tst_C = loadSVMResult_A('../data/test.json' , '../libsvm-master/predict.test2' )
    trn_data = labelAllGood(trn_data, QGOLD_YN=None, CGOLD=svm_result_trn_C)
    dev_data = labelAllGood(dev_data, QGOLD_YN=None, CGOLD=svm_result_dev_C)
    tst_data = labelAllGood(tst_data, QGOLD_YN=None, CGOLD=svm_result_tst_C)

    getLabeledFile_TaskB(trn_data, '../data/train_taskB.data')
    getLabeledFile_TaskB(dev_data, '../data/dev_taskB.data')
    getLabeledFile_TaskB(tst_data, '../data/test_taskB.data')
    #"""

            
