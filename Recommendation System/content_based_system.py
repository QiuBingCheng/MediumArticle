# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 10:22:43 2020

@author: Jerry
"""
#%%
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
#%%
#function
def get_the_most_similar_movies(user_id, user_movie_matrix,num):
    """Find the top-n movies most similar to the user"""
    user_vec = user_movie_matrix.loc[user_id].values 
    sorted_index = np.argsort(user_vec)[::-1][:num]
    return list(user_movie_matrix.columns[sorted_index])
 
def get_the_most_similar_users(movie_id, user_movie_matrix,num):
    """Find the top-n users most similar to the movie"""
    movie_vec = user_movie_matrix.loc[:,movie_id].values 
    sorted_index = np.argsort(movie_vec)[::-1][:num]
    return list(user_movie_matrix.index[sorted_index])    

#%%
#read movie data
movies = pd.read_csv(r"dataset\MovieLens\movies.csv")
movies.columns
movies.drop('title',axis=1,inplace=True)
df = pd.read_csv(r"dataset\MovieLens\ratings.csv")

df.drop(['rating', 'timestamp'],axis=1,inplace=True)
df = pd.merge(df, movies, on='movieId')
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

# user_movie_similarity_matrix[i,j] 
# similarity between useri and moviej
user_movie_similarity_matrix = cosine_similarity(user_vec.values,movie_vec.values)
user_movie_similarity_matrix = pd.DataFrame(user_movie_similarity_matrix, index=user_vec.index,columns=movie_vec.index)

#Find the top-10 movies most similar to the user1
get_the_most_similar_movies(1, user_movie_similarity_matrix,10)

#Find the top-10 users most similar to the movie1
get_the_most_similar_users(1, user_movie_similarity_matrix,10)

