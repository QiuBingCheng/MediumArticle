# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 18:45:13 2020

@author: Jerry
"""
import math
import os
from wordcloud import WordCloud
from WordSegment import WordSegment
#%%
storage_folder = "clean data"
filenames = os.listdir(storage_folder)
singers = {}
for filename in filenames:
    path = f"{storage_folder}/{filename}"
    with open(path,encoding="utf-8") as file:
        #每位歌手的歌詞以字串形式連接
        lyric = ""
        for i,line in enumerate(file.readlines()):
            if i==0:continue
            title, content = line.split(",",1)
            lyric += content
        singer = filename.split(".")[0]
        singers[singer] = lyric

stop_words_path = "stop_words"
stop_words_path = [f"{stop_words_path}/{path}" for path in os.listdir(stop_words_path)]
ws = WordSegment(singers.values(),stop_words_path=stop_words_path)
ws.read_dictionary()
ws.read_stop_words()
ws.remove_stop_words()
text_files = [text.split(" ") for text in ws.texts]
#%% 
#計算tf-idf

#統計每個語詞的次數
words_count = []
for file in text_files:
    count = {}
    for word in file:
        if word in count:
            count[word] += 1
        else:
            count[word] = 1
    words_count.append(count)

# 統計每個語詞的頻率(次數/全部單語詞次數)
words_frequency = []
for word_count in words_count:
    all_count = sum(word_count.values()) #單篇歌詞的所有單詞數量
    fre = {}
    for word,count in word_count.items():
        fre[word] = round(count/all_count,4)
    words_frequency.append(fre)

#idf
#先取得每個語詞在歌手歌詞中"出現過"的次數
all_words = []
for word in words_count:
    all_words.extend(list(word.keys()))
    
occurrences_of_word = {}
for word in all_words:
    if word in occurrences_of_word:
        occurrences_of_word[word] += 1
    else:
        occurrences_of_word[word] = 1
        
inverse_document_frequency = []     
for word_count in words_count:
    #出現過的次數
    invFre = {} 
    for word in word_count.keys():
        occurrences = occurrences_of_word[word]
        invFre[word] = math.log(round((len(words_count)/occurrences),4))
    inverse_document_frequency.append(invFre)
    
##tf*idf
all_tf_idf = []
for i,words in enumerate(words_frequency):
    tf_idf = {}
    for word,freq in words.items():
        tf_idf[word] = freq*inverse_document_frequency[i][word]
    all_tf_idf.append(tf_idf)

#%%視覺化
path = ["images/JayChou.png","images/JayJay.png","images/Mayday.png"]
for i,tf_idf in enumerate(all_tf_idf):
    WordCloud(collocations=False, 
                font_path="C:\Windows\Fonts\msjhbd.ttc", # 字體設定(是中文一定要設定，否則會是亂碼)
                #font_path='NotoSansCJKjp-Black.otf',  字體設定(是中文一定要設定，否則會是亂碼)
                width=600, # 圖片寬度
                height=600,  # 圖片高度
                background_color = "white" , #圖片底色
                margin=2 # 文字之間的間距
                ).generate_from_frequencies(tf_idf).to_image().save(path[i])
