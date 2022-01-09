# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 23:22:17 2020

@author: Jerry
"""
import re
import jieba
#%%    
class WordSegment:
    def __init__(self,texts,stop_words_path,dicts_path=""):
        self.jieba = jieba
        self.texts = texts
        self.dicts_path = dicts_path
        self.stop_words_path = stop_words_path
        
    def read_dictionary(self): 
        #讀取類別
        print("read_dictionary is called")
        if self.dicts_path:
            for dic in self.dicts_path:
                self.jieba.load_userdict(dic)

    def read_stop_words(self):
        #讀取stopword
        self.stop_words = set()
        for stop_words_file in self.stop_words_path:
            with open(stop_words_file,encoding = 'UTF-8') as file:
                self.stop_words = self.stop_words | set(map(str.strip,file.readlines()))
        
    def remove_stop_words(self):
        # 去除繁體中文以外的英文、數字、符號
        rule = re.compile(r"[^\u4e00-\u9fa5]")
        self.texts = [list(self.jieba.cut(rule.sub('', text))) for text in self.texts]
        for idx, speech in enumerate(self.texts):
            self.texts[idx] = ' '.join([word for word in speech if word.strip() not in self.stop_words])
    
