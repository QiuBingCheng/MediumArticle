# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 11:15:05 2020

@author: Jerry
"""

#%%
#import
import numpy as np
import pandas as pd
from collections import defaultdict
#%%
#read data
movies = pd.read_csv(r"dataset\MovieLens\movies.csv")
movies.drop(columns="genres",inplace=True)
df = pd.read_csv(r"dataset\MovieLens\ratings.csv")
df.drop(columns="timestamp",inplace=True)
df = pd.merge(df, movies, on='movieId')
#%%
#function       
def recommend(user,num=10):
    #find similarity between user and other uesr.
    user_similarity = [] 
    for other_user in df.userId.unique():
        if other_user == user:
            continue
        print ("other user :",other_user)
        common_movies = find_common_movie(user,other_user)
        sim = cal_user_similarity_with_movie_rating(user,other_user,common_movies)
        user_similarity.append([other_user,sim])
    
    #find top 10 similar user
    user_similarity = np.array(user_similarity)
    sorted_index = np.argsort(user_similarity, axis=0)[:,1][::-1][:10]
    top10_similar_user = user_similarity[:,0][sorted_index] 
    
    #find the movie the user haven't seen
    seen_movies = df.loc[df["userId"]==user,"movieId"].values
    not_seen_movies = defaultdict(list) 
    for similar_user in top10_similar_user:
        movies = df.loc[df.userId==similar_user,["movieId","rating"]].values.tolist()
        if isinstance(movies[0], list):
            for movie in movies:
                if movie[0] in seen_movies:
                    continue
                not_seen_movies[movie[0]].append(movie[1])
                
        elif movies[0] not in seen_movies:
           not_seen_movies[movies[0]].append(movies[1])
                
    #average same movie rating
    for movie in not_seen_movies:
        not_seen_movies[movie] = np.mean(not_seen_movies[movie])
    
    #get top 10 ratings by sorting it 
    top10_rating = sorted(not_seen_movies.items(), key=lambda x: x[1], reverse=True)
    return [movie for movie,rating in top10_rating][:num]


def find_common_movie(user1,user2):
    """找尋兩個uesr共同觀看過電影"""
    s1 = set((df.loc[df["userId"]==user1,"movieId"].values))
    s2 = set((df.loc[df["userId"]==user2,"movieId"].values))
    return s1.intersection(s2)

def cosine_similarity(vec1, vec2):
    """
    計算兩個向量之間的餘弦相似性
    :param vec1: 向量 a 
    :param vec2: 向量 b
    :return: sim
    """
    vec1 = np.mat(vec1)
    vec2 = np.mat(vec2)
    num = float(vec1 * vec2.T)
    denom = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    cos = num / denom
    sim = 0.5 + 0.5 * cos
    return sim

def cal_user_similarity_with_movie_rating(user1,user2,movies_id):
    """計算兩個user對於特定電影評分的相似度"""
    u1 = df[df["userId"]==user1]
    u2 = df[df["userId"]==user2]
    vec1 = u1[u1.movieId.isin(movies_id)].sort_values(by="movieId")["rating"].values
    vec2 = u2[u2.movieId.isin(movies_id)].sort_values(by="movieId")["rating"].values
    return cosine_similarity(vec1, vec2)

#%%
top10_movie = recommend(1,num=10)
    
    
