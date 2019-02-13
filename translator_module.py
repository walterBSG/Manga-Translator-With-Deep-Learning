#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 16:34:24 2019

@author: walter
"""

import os
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
import re

def load_data(path):
    path = os.path.join(path)
    with open(path, mode='rt', encoding='utf-8') as f:
        data = f.read()

    return data.strip().split('\n')

def threshold(pt_sentences,en_sentences, length = 140):
    pt = []
    en = []
    for p, e in zip(pt_sentences, en_sentences):
        if len(e) < length:
            pt.append(p)
            en.append(e)
    return pt, en

def tokenize(x):
    x_tk = Tokenizer()
    x_tk.fit_on_texts(x)
    return x_tk.texts_to_sequences(x), x_tk

def pad(x, length=36):
    if length is None:
        length = len(max(x, key=len))

    return pad_sequences(x, maxlen=length, padding='post')

def preprocess(x, y):
    preprocess_x, en_tokenizer = tokenize(x)
    preprocess_y, pt_tokenizer = tokenize(y)

    preprocess_x = pad(preprocess_x)
    preprocess_y = pad(preprocess_y)

    preprocess_y = preprocess_y.reshape(*preprocess_y.shape, 1)

    return preprocess_x, preprocess_y, en_tokenizer, pt_tokenizer

def load_sentences(path = 'translator'):
	
	dataset = load_data(os.path.join(path,'por.txt'))
	en_sentences = []
	pt_sentences = []
	
	for d in dataset:
	    row = d.split('\t')
	    en_sentences.append(row[0])
	    pt_sentences.append(row[1])
    
	pt_sentences, en_sentences = threshold(pt_sentences,en_sentences)
	
	return en_sentences, pt_sentences
    
def load_all():
	
	en_sentences, pt_sentences = load_sentences()
	
	preproc_en_sentences, preproc_pt_sentences, en_tokenizer, pt_tokenizer = preprocess(en_sentences, pt_sentences)
    
	max_pt_sequence_length = preproc_pt_sentences.shape[1]
	
	x = pad(preproc_en_sentences, max_pt_sequence_length)

	y_id_to_word = {value: key for key, value in pt_tokenizer.word_index.items()}
	y_id_to_word[0] = '<PAD>'
	
	model = load_model('translator/translator.h5')
	
	return  model, en_tokenizer, x, y_id_to_word

def prepare(sentence):
	sentence = re.sub(r'[^\w\s]','',sentence)
	sentence = sentence.lower()
	return sentence.replace('\n',' ')

def translate(model, sentence, en_tokenizer, x, y_id_to_word):
	s = sentence
	try:
		sentence = prepare(sentence)
		print(sentence)
		sentence = [en_tokenizer.word_index[word] for word in sentence.split()]
		sentence = pad_sequences([sentence], maxlen=x.shape[-1], padding='post')
		prediction = model.predict(sentence)
		answer = ' '.join([y_id_to_word[np.argmax(x)] for x in prediction[0]])
		answer = answer.replace('<PAD>','')
		print(answer)
		return str(answer)
	except:
		return s

def test(sentense):
	model, tokenizer, x, y = load_all()
	sentense = prepare(sentense)
	translate(model, sentense, tokenizer, x, y)