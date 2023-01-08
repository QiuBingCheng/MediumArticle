# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 15:28:46 2023

@author: Jerry
"""
#%%
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from numpy import dot
from numpy.linalg import norm
#%%
#read data
movies = pd.read_csv(r"dataset\MovieLens\movies.csv")
rating = pd.read_csv(r"dataset\MovieLens\ratings.csv")

#%%
vote_count = rating.groupby("movieId").count()["userId"].rename("vote_count").reset_index()
vote_average = rating.groupby("movieId").mean()["rating"]
C = vote_average.mean()

m = vote_count["vote_count"].quantile(0.9)
q_movies = vote_count[vote_count["vote_count"]>=m].reset_index(drop=True)
q_movies["vote_average"] = vote_average[q_movies.movieId].values

def weighted_rating(x, m=m, C=C):
    v = x["vote_count"]
    R = x["vote_average"]
    # Calculation based on the IMDB formula
    return (v/(v+m) * R) + (m/(m+v) * C)

q_movies["score"] = q_movies.apply(weighted_rating,axis=1).values
#Sort movies based on score calculated above
q_movies = q_movies.sort_values('score', ascending=False)

df = pd.merge(q_movies, movies, on='movieId')
df.head()

plt.barh(df['title'].head(6),df['score'].head(6), align='center',
        color='skyblue')
plt.gca().invert_yaxis()
plt.xlabel("Scores")
plt.title("Popular Movies")

#%%
f, ax = plt.subplots(figsize=(6, 6))
sns.scatterplot(x="vote_count", y="vote_average",data=q_movies)
ax.set_ylabel("Vote average",fontsize=14)
ax.set_xlabel("Vote count",fontsize=14)
#%%
genres = df.genres.str.get_dummies(sep="|")
df = pd.merge(df,genres,left_index=True,right_index=True)
df.drop("genres",axis=1,inplace=True)
#%%
# Top Action Movies
columns = ["title","vote_count","vote_average"]
df.loc[df["Action"]==1,columns].head()
# Top Action Movies
df.loc[df["Comedy"]==1,columns].head()
#%%
#Content Based Recommender

def get_the_most_similar_movies(user_id, user_movie_matrix,num):
    """Find the top-n movies most similar to the user"""
    user_vec = user_movie_matrix.loc[user_id].values 
    sorted_index = np.argsort(user_vec)[::-1][:num]
    return list(user_movie_matrix.columns[sorted_index])
 
# movie vector
dummies = movies["genres"].str.get_dummies('|')
movie_vec = pd.concat([movies["movieId"], dummies], axis=1)
movie_vec.set_index("movieId",inplace=True)

#user vector 
movie_rating = pd.merge(rating[["userId","movieId"]], movies[["movieId","genres"]], on='movieId')
dummies = movie_rating["genres"].str.get_dummies('|')
user_vec = pd.concat([movie_rating, dummies], axis=1)
user_vec.drop(['movieId', 'genres'],axis=1,inplace=True)
user_vec = user_vec.groupby("userId").mean()

# user_movie_similarity_matrix[i,j] 
# similarity between useri and moviej
user_movie_similarity_matrix = cosine_similarity(user_vec.values,movie_vec.values)
user_movie_similarity_matrix = pd.DataFrame(user_movie_similarity_matrix, index=user_vec.index,columns=movie_vec.index)

#Find the top-10 movies most similar to the user1
movied_ids = get_the_most_similar_movies(1, user_movie_similarity_matrix,10)
print(movies[movies["movieId"].isin(movied_ids)]["title"])
#%%
#Content Based Recommender

def find_common_movies(user1,user2):
    """Find movies that both users have watched"""
    s1 = set((df.loc[df["userId"]==user1,"movieId"].values))
    s2 = set((df.loc[df["userId"]==user2,"movieId"].values))
    return s1.intersection(s2)

def cal_similarity_for_movie_ratings(user1,user2,movies_id,method="cosine"):
    """Calculate the similarity for movie ratings between user1 and user2"""
    u1 = df[df["userId"]==user1]
    u2 = df[df["userId"]==user2]
    vec1 = u1[u1.movieId.isin(movies_id)].sort_values(by="movieId")["rating"].values
    vec2 = u2[u2.movieId.isin(movies_id)].sort_values(by="movieId")["rating"].values
    if method=="cosine":        
        return dot(vec1, vec2)/(norm(vec1)*norm(vec2))
    return None

def find_the_most_similar_users(user, num=10):
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

movie_rating = pd.merge(rating[["userId","movieId","rating"]], movies[["movieId","genres"]], on='movieId')
dummies = movie_rating["genres"].str.get_dummies('|')
df = pd.concat([movie_rating, dummies], axis=1)
df.drop(['genres'],axis=1,inplace=True)

num = 15
top_n = 10
user_id = 1
similar_users = find_the_most_similar_users(user_id,num)
top_ratings = recommend(user_id,similar_users, top_n)

print(f"Top-{num} similar users: {similar_users}")
print(f"Top-{top_n} average ratings by the most simiilar users:")
print(pd.merge(top_ratings, movies, on='movieId'))

