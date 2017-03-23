#coding=utf-8
#-*- coding: UTF-8 -*- 
import sys
import math
import numpy as np
import tensorflow as tf
from keras.layers import Embedding, Input, Dense, Flatten, Dropout, Activation, Lambda, Reshape
from keras.layers.pooling import MaxPooling1D
from keras.layers.merge import concatenate

# little tools
def getIndex_i(input, index) :
    return Lambda(lambda x: tf.expand_dims(x[:, index], 1))(input)
def getSigmoid(r, minus=0) :
    # ret = sigmoid(r*(x - minus))
    sigmoid = lambda x : 1 / (1 + tf.exp(-x))
    return Lambda(lambda x: sigmoid(r * (x - minus)))

# Inputs Group
def getInputGroup(shape, dtype, nameHead, Num, convert=str) :
    ret_Inputs = []
    for i in range(Num) :
        ret_Inputs.append(Input(shape=shape, dtype=dtype, name=(nameHead+'_'+convert(i))))
    return ret_Inputs

# multi-perspective CNN Embedding
def CNNSentenceEmbd(input_sequences, wordVector, cnnlayers, drop_rate=0) :
    assert type(cnnlayers) is list
    inputLength = int(input_sequences._shape[1])
    w2vSize = np.shape(wordVector)[0]
    w2vLength = np.shape(wordVector)[1]

    x = Embedding(output_dim=w2vLength, input_dim=w2vSize, input_length=inputLength, weights=[wordVector])(input_sequences)
    xall = []
    for cnnlayer in cnnlayers :
        xt = cnnlayer(x)
        lxt = inputLength - cnnlayer.kernel_size[0] + 1
        xt = MaxPooling1D(strides=None, padding='valid', pool_size=lxt)(xt)
        xt = Flatten()(xt)
        xt = Reshape([cnnlayer.filters])(xt)
        xall.append(xt)
    xout = concatenate(xall)
    if not drop_rate == 0 :
        xout = Dropout(drop_rate)(xout)
    return xout

# smarter Dense Layer
def getDense(inputs, outputLength = None, denseLayer = None, DropoutRate=0) :
    assert type(inputs) is list
    assert not(outputLength is None and denseLayer is None)
    if denseLayer is None :
        denseLayer = Dense(outputLength, activation='relu', kernel_initializer='uniform')

    xout = inputs[0] if len(inputs) == 1 else concatenate(inputs)
    xout = denseLayer(xout)
    if not DropoutRate == 0 :
        xout = Dropout(DropoutRate)(xout)
    return xout

# batch_dot and batch_cosine, because something went wrong in keras
def my_batch_dot(input1, input2) :
    """
    input  : (?, n), (?, n)
    output : (?, 1)
    """
    return Lambda(lambda x: tf.expand_dims(tf.diag_part(tf.matmul(x[0], tf.transpose(x[1]))), 1))([input1, input2])
def cosine(input1, input2) :
    return Lambda(lambda x: my_batch_dot(x[0], x[1]) / tf.sqrt(my_batch_dot(x[0], x[0]) * my_batch_dot(x[1], x[1])))([input1, input2])

def getAttention(input, attentionList, Index) :
    att = Lambda(lambda x: tf.expand_dims(x[:, Index], 1))(attentionList)
    artt = Lambda(lambda x: x[0] * x[1])([att, input])
    return artt
