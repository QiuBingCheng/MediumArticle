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
def recommend(user, num=10, top_n=15):
    """Recommend n movies to the user
    
    Parameters
    ----------
    user : int
        The user id  
    num : int
        Collaborative filtering based on how many users.
    top_n : int
        The number of the movies recommended
        
    Returns
    -------
    list
        a list of integer representing the movie ids recommended
    """
   
    
    #calculate the similarity between the user and other users
    similarities = []
    user_ids = []
    for other_user in df.userId.unique():
        if other_user == user:
            continue
        print ("other user :",other_user)
        common_movies = find_common_movie(user,other_user)
        sim = cal_similarity_for_movie_ratings(user,other_user,common_movies)
        similarities.append(sim)
        user_ids.apend(other_user)
    
    #find top n similar users
    similarities = np.array(similarities)
    sorted_index = np.argsort(similarities)[::-1][:top_n]
    most_similar_users = user_ids[sorted_index] 
    
    #find the movie the user haven't seen
    #TODO: make the code elegant
    seen_movies = df.loc[df["userId"]==user,"movieId"].values
    not_seen_movies = defaultdict(list) 
    for similar_user in most_similar_users:
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
    """Find movies that both users have watched"""
    s1 = set((df.loc[df["userId"]==user1,"movieId"].values))
    s2 = set((df.loc[df["userId"]==user2,"movieId"].values))
    return s1.intersection(s2)

def cal_cosine_similarity(vec1, vec2):
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

def cal_similarity_for_movie_ratings(user1,user2,movies_id):
    """Calculate the similarity for movie ratings between user1 and user2"""
    u1 = df[df["userId"]==user1]
    u2 = df[df["userId"]==user2]
    vec1 = u1[u1.movieId.isin(movies_id)].sort_values(by="movieId")["rating"].values
    vec2 = u2[u2.movieId.isin(movies_id)].sort_values(by="movieId")["rating"].values
    return cal_cosine_similarity(vec1, vec2)

#%%
top10_movie = recommend(1,num=10)
    
    
