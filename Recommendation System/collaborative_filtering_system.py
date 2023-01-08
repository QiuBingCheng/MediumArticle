# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 11:15:05 2020

@author: Jerry
"""

#%%
#import
import numpy as np
import pandas as pd
from numpy import dot
from numpy.linalg import norm
#%%
#read data
movies = pd.read_csv(r"dataset\MovieLens\movies.csv")
movies.drop(columns="genres",inplace=True)
df = pd.read_csv(r"dataset\MovieLens\ratings.csv")
df.drop(columns="timestamp",inplace=True)
df = pd.merge(df, movies, on='movieId')
print(df.head())
#%% 
# Common function
def cal_similarity_for_movie_ratings(user1,user2,movies_id,method="cosine"):
    """Calculate the similarity for movie ratings between user1 and user2"""
    u1 = df[df["userId"]==user1]
    u2 = df[df["userId"]==user2]
    vec1 = u1[u1.movieId.isin(movies_id)].sort_values(by="movieId")["rating"].values
    vec2 = u2[u2.movieId.isin(movies_id)].sort_values(by="movieId")["rating"].values
    if method=="cosine":        
        return dot(vec1, vec2)/(norm(vec1)*norm(vec2))
    return None

def find_common_movies(user1,user2):
    """Find movies that both users have watched"""
    s1 = set((df.loc[df["userId"]==user1,"movieId"].values))
    s2 = set((df.loc[df["userId"]==user2,"movieId"].values))
    return s1.intersection(s2)

def find_the_most_similar_users(user, num=10):
    """Find the most similar users
    
    Args:
        user (int): User id
        num (int): Collaborative filtering based on how many users
  
    Returns:
        list: A list of the similar users id.
    """
    # Calculate the similarity between the user and other users
    similarities = []
    user_ids = []
    for other_user in df.userId.unique():
        if other_user == user:
            continue
        
        common_movies = find_common_movies(user,other_user)
        
        if len(common_movies)<10:
            sim = 0
        else:
            sim = cal_similarity_for_movie_ratings(user,other_user,common_movies)
        
        similarities.append(sim)
        user_ids.append(other_user)
            
    # Find top n similar users
    similarities,user_ids = np.array(similarities),np.array(user_ids)
    sorted_index = (np.argsort(similarities)[::-1][:num]).tolist()
    most_similar_users = user_ids[sorted_index] 
    return most_similar_users

def recommend(user,similar_users ,top_n=10):
    """Find the top_n movies of most high average ratings
    by the most similar users.
    
    Args:
        user (int): User id
        similar_users (list): A list of the similar users id
        
    Returns:
        top_ratings (dataframe): a dataframe includes the most recommended movies and average ratings.
    """
    
    # Find the movies the user hasn't seen and the similar users have seen.
    seen_movies = np.unique(df.loc[df["userId"]==user,"movieId"].values)
    not_seen_cond = df["movieId"].isin(seen_movies)==False
    similar_cond = df["userId"].isin(similar_users)
    not_seen_movies_ratings = df[not_seen_cond & similar_cond][["movieId","rating"]]
    
    # Find average ratings by the most similar users
    average_ratings = not_seen_movies_ratings.groupby("movieId").mean()
    average_ratings.reset_index(inplace=True)
    top_ratings = average_ratings.sort_values(by="rating",ascending=False).iloc[:top_n]
    top_ratings.reset_index(inplace=True,drop=True)
    return top_ratings

#%%

num = 15
top_n = 10
user_id = 1
similar_users = find_the_most_similar_users(user_id,num)
top_ratings = recommend(user_id,similar_users, top_n)

print(f"Top-{num} similar users: {similar_users}")
print(f"Top-{top_n} average ratings by the most simiilar users:")
print(pd.merge(top_ratings, movies, on='movieId'))
