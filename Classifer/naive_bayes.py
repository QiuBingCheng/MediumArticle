# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 08:31:01 2020

@author: Jerry
"""
import re
import random
from math import log,exp
from collections import defaultdict
import numpy as np

def read_file(filepath):
    print(f"read {filepath}...")
    """
    :return mails: 訊息列表
    """
    mails = []
    with open(filepath,encoding="utf-8") as file:
        for line in file.readlines():
            is_spam,message = line.split("\t")
            is_spam = 1 if is_spam=="spam" else 0
            message = message.strip()
            mails.append((message,is_spam))
    return mails


class NaiveBayesClassifier():
    def __init__(self, k = 1):
        self.k = k  # smoothing factor
        self.total_count_ = [0,0] # total word count in class
        self.word_count_ = defaultdict(lambda :[0,0]) 
        self.word_prob_ = defaultdict(lambda :[0,0])
        
    def tokenize(self,message):
        message = message.lower()                      
        all_words = re.findall("[a-z']+", message) 
        return set(all_words)
            
    def train(self,messages,spam_or_not):
        print("training data..")
        """
        messages:訊息文本
        spam_or_not:是否為垃圾訊息
        """
        #1-計算各類別次數、單詞在各類別的次數
        for message,is_spam in zip(messages,spam_or_not):
            for word in self.tokenize(message):
                self.word_count_[word][is_spam] += 1
                self.total_count_[is_spam] += 1 
            
        #2-計算單詞在各類別條件下的條件機率 (單詞出現數量/類別單詞總數量)
        for word,count in self.word_count_.items():
            word_prob_if_spam = (self.k+count[1])/(2*self.k+self.total_count_[1])
            word_prob_if_non_spam = (self.k+count[0])/(2*self.k+self.total_count_[0])
            
            self.word_prob_[word][1] = word_prob_if_spam
            self.word_prob_[word][0] = word_prob_if_non_spam

    def predict_proba(self,message):
        log_prob_if_spam = 0
        log_prob_if_non_spam = 0
        
        all_words = self.tokenize(message)
        for word,word_prob in self.word_prob_.items():
            if word in all_words:
                log_prob_if_spam += log(word_prob[1])
                log_prob_if_non_spam += log(word_prob[0])
                
            else:
                log_prob_if_spam += log(1-word_prob[1])
                log_prob_if_non_spam += log(1-word_prob[0])
        
        prob_if_spam = exp(log_prob_if_spam)
        prob_if_non_spam = exp(log_prob_if_non_spam )
        return prob_if_spam/(prob_if_spam+prob_if_non_spam)
    
    def predict(self,message):
        return 1 if self.predict_proba(message)>0.5 else 0

def confusion_matrix(y_true,y_pred):
    print ("generating confusion matrix")
    tn, fp, fn, tp = 0,0,0,0
    for actual,prediction in zip(y_true,y_pred):
        if (actual==0 and prediction==0):
           tn +=1
        elif(actual==0 and prediction==1):
            fp += 1
        elif(actual==1 and prediction==0):
            fn += 1
        else:
            tp += 1
    return  tn, fp, fn, tp

def split_data(mails,ratio=0.8):
    print("split data..")
    random.seed(2)
    random.shuffle(mails)
    train_num  = round(0.8*len(mails))
    train_X = [ mail[0] for mail in mails[:train_num]]
    train_y = [ mail[1] for mail in mails[:train_num]]

    test_X = [ mail[0] for mail in mails[train_num:]]
    test_y = [ mail[1] for mail in mails[train_num:]]
    return (train_X,train_y,test_X,test_y)

def get_top_proba_of_spam(proba,messages,num=5):
    def tokenize(messages):
        words = []
        for message in messages:
            message = message.lower()                      
            all_words = re.findall("[a-z]+", message) 
            words.append(set(all_words))
        return words
    
    sort_index = np.argsort(proba)[::-1][:5]
    sorted_proba = [proba[i] for i in sort_index]
    sorted_message = [messages[i] for i in sort_index]
    return (sorted_proba,sorted_message,tokenize(sorted_message))

def main():
    mails = read_file("data/SMSSpamCollection.txt")
    train_X,train_y, test_X,test_y = split_data(mails)
    nb = NaiveBayesClassifier()
    nb.train(train_X,train_y)
    
    #get proba
    y_proba = []
    y_pred = []
    for x in test_X:
        proba = nb.predict_proba(x)
        y_proba.append(proba)
        y_pred.append(1 if proba>0.5 else 0)
    
    tn, fp, fn, tp = confusion_matrix(test_y,y_pred)
    precision = tp/(tp+fp)
    recall = tp/(tp+fn)
    print(f"(tn, fp, fn, tp)=>{(tn, fp, fn, tp)}")
    print(f"precision : {precision}")
    print(f"recall : {recall}")
    
    #spammiest_message
    proba,message,tokens = get_top_proba_of_spam(y_proba,test_X)
    word_probs = []
    for token in tokens:
        probs = []
        for word in token:
            if word in nb.word_prob_:
                probs.append(nb.word_prob_[word][0])
        word_probs.append(probs)
        
if __name__ == "__main__":
    main()
            

