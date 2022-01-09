# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 10:22:43 2020

@author: Jerry
"""
#%%
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import paired_distances,cosine_similarity
#%%
#function
def get_the_most_similar_movies(user_id, user_movie_matrix,num):
    """找尋與特定user距離最近/最相似的前幾部movie"""
    user_vec = user_movie_matrix.loc[user_id].values 
    sorted_index = np.argsort(user_vec)[:num]
    return list(user_movie_matrix.columns[sorted_index])
 
def get_the_most_similar_users(movie_id, user_movie_matrix,num):
    """找尋與特定movie距離最近/最相似的前幾部movie"""
    movie_vec = user_movie_matrix[movie_id].values 
    sorted_index = np.argsort(movie_vec)[:num]
    return list(user_movie_matrix.index[sorted_index])    

def edu_dis(arr1,arr2):
    dis = np.zeros((arr1.shape[0],arr2.shape[0]))
    length = len(arr2)
    for i in range(length):
        fun = lambda x:get_euclidean(x, arr2[i])
        dis[:,i] = np.apply_along_axis(fun,1,arr1)
    return dis

def get_euclidean(arr1, arr2):
    #point array type
    return np.sqrt(sum(pow(arr1 - arr2, 2)))
#%%
#read movie data
movies = pd.read_csv(r"dataset\MovieLens\movies.csv")
movies.columns
movies.drop('title',axis=1,inplace=True)
df = pd.read_csv(r"dataset\MovieLens\ratings.csv")

df.drop(['rating', 'timestamp'],axis=1,inplace=True)
df = pd.merge(df, movies, on='movieId')
df.columns
df
#%%
#movie vector
dummies = movies["genres"].str.get_dummies('|')
movie_vec = pd.concat([movies, dummies], axis=1)
movie_vec.columns
movie_vec.drop('genres',axis=1,inplace=True)
movie_vec.set_index("movieId",inplace=True)

#user vector 
dummies = df["genres"].str.get_dummies('|')
user_vec = pd.concat([df, dummies], axis=1)
user_vec.drop(['movieId', 'genres'],axis=1,inplace=True)
user_vec = user_vec.groupby("userId").mean()

#距離度量 #index=user_vec columns = movie_vec.index
#user_movie_matrix = edu_dis(user_vec.values,movie_vec.values)
user_movie_matrix = cosine_similarity(user_vec.values,movie_vec.values)
user_movie_matrix = 1- user_movie_matrix  
user_movie_matrix = pd.DataFrame(user_movie_matrix, index=user_vec.index,columns=movie_vec.index)

#為user1找出最相似的10部影片
get_the_most_similar_movies(1, user_movie_matrix,10)

#為movie1找出最相似的10個用戶
get_the_most_similar_users(1, user_movie_matrix,10)

