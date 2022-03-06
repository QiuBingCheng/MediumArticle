# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 22:14:45 2022

@author: Jerry
"""
from csv import reader
import math

# read csv
data_path = "data/play.csv"
df = pd.read_csv(data_path)
df.head()

# preprocessing
m = {"Play":True,"Don't Play":False}
df["play"] = df["play"].map(m)

X = df[["outlook","temperature","humidity","windy"]]
y = df["play"]

data_type = ["str","integer","integer","str"]


(y[[0,1]] == False).sum()

math.log(0/4, 2)

def entropy_fun(c,n):
    if c == 0 :
        return 0
    return -(c/n)*math.log(c/n, 2)
    
def total_entropy(groups,y):
    # calculate entropy for each group
    entropy_list = []
    count_list = []
    for group in groups:
        total = len(y[group])
        p_count = (y[group]==True).sum()
        n_count = total-p_count
        entropy = entropy_fun(p_count,total) + entropy_fun(n_count,total)
         
        # for total calculation
        entropy_list.append(entropy)
        count_list.append(total)
        
    # get total entroy 
    total_entroy = 0
    for count, entropy in zip(count_list, entropy_list):
        sample_ratio = count/sum(count_list)
        total_entroy += entropy*sample_ratio
    
    return total_entroy
        
# Split a dataset based on an attribute and an attribute value
def test_str_split(indexs, attr, X):
    unique_val = X.loc[indexs][attr].unique().tolist()
    groups = [[] for _ in range(len(unique_val))]
    for index in indexs:
        th = unique_val.index(X.loc[index][attr])
        groups[th].append(index)
    return groups

def test_integer_split(indexs, attr, val, X):
    groups = [[],[]]
    for index in indexs:
        if(X.loc[index][attr]<=val):
            groups[0].append(index)
        else:
            groups[1].append(index)
    return groups

def valid_groups(groups):
    l = 0
    for group in groups:
        if(len(group)>0):
            l += 1
    return True if l>1 else False

#[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], []]
    
b_group = None
b_entropy = 999
b_condition = None
indexs = X.index.tolist()

for i, attr in enumerate(X.columns):
     
    if(data_type[i] == "str"):
        groups = test_str_split(indexs, attr, X)
        if not valid_groups(groups):
            continue
        entropy = total_entropy(groups,y)
        
        if(entropy<b_entropy):
            b_group = groups
            b_entropy = entropy
        
    elif (data_type[i] == "integer"):
        unique_val =  X.loc[indexs][attr].unique().tolist()
        for val in unique_val:
            groups = test_integer_split(indexs, attr, val, X)
            
            if not valid_groups(groups):
                continue
            
            entropy = total_entropy(groups,y)
            if(entropy<b_entropy):
                b_condiction = val
                b_group = groups
                b_entropy = entropy

  


