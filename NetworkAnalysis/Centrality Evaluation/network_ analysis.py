# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 09:18:08 2020

@author: Jerry
"""
from collections import defaultdict,deque
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import pandas as pd
#%% plot
friendships = [("郭靖","黃蓉"),("郭靖","楊康"),("郭靖","洪七公"),("郭靖","楊過"),
               ("郭靖","周伯通"),("郭靖","郭嘯天"),("郭靖","李萍"),
               ("黃蓉","黃藥師"),("楊康","楊鐵心"),("楊康","歐陽鋒"),("楊康","穆念慈"),
               ("洪七公","黃藥師"),("楊過","小龍女"),("周伯通","王重陽"),
               ("王重陽","丘處機"),("李萍","郭嘯天")]
def draw_basic_network_graph(nodes):
    G = nx.Graph()
    G.add_edges_from(friendships)
    plt.figure(figsize=(8,8)) 
    nx.draw(G, with_labels=True, node_size=3500, font_size=22, font_family='Source Han Sans TW',font_color="yellow", font_weight="bold")
    plt.show()
    
draw_basic_network_graph(friendships)
#%%
#degree centrality
#計算好友數量
def degree_centrality(friendships):
    user_friend_count = defaultdict(int)
    for friendship in friendships:
        user_id, friend_id = friendship
        user_friend_count[user_id] += 1
        user_friend_count[friend_id] += 1
    return user_friend_count

def standardize(user_friend_count):
    #標準化-除以(n-1)(n-2)
    total_count = sum(user_friend_count.values())
    return {user:count/((total_count-1)*(total_count-2)) for user,count in user_friend_count.items()}

user_friend_count = degree_centrality(friendships)
user_friend_count_after_standardization = standardize(user_friend_count)

#make it readable
df = pd.DataFrame.from_dict(user_friend_count.items())
df.insert(2,"degree centrality(std)",user_friend_count_after_standardization.values())
df.columns = ["人物","degree centrality","degree centrality(std)"]
#%%
def construct_users_friends(friendships):
    """
    Returns:
        key:userId
        value:friends list
    """
    users = defaultdict(list)
    for friendship in friendships:
        user_id, friend_id = friendship
        users[user_id].append(friend_id)
        users[friend_id].append(user_id)
    return users
        
def shortest_paths_from(from_user, users):
    shortest_paths = {}  
    visited  = deque() #(節點路徑,該節點ID)
    for friend_id in users[from_user]:
        cur_path = [from_user,friend_id]
        shortest_paths[friend_id] = [cur_path]
        print(f"找到第1次與 {friend_id} 最短路徑")
        visited.append((cur_path,friend_id))
        
    while visited:
        prev_path, friend_id = visited.popleft()
        print(f"開始拜訪 {friend_id} 的朋友")
        #拜訪該節點的朋友
        for friend_of_friend in users[friend_id]:
            #略過from_user本身
            if friend_of_friend == from_user:
                continue
            cur_path = prev_path+[friend_of_friend]
            if friend_of_friend in shortest_paths:
                if len(cur_path) == len(shortest_paths[friend_of_friend][0]):
                     shortest_paths[friend_of_friend].append(cur_path)
                     visited.append((cur_path,friend_of_friend))
                     path_count = len(shortest_paths[friend_of_friend])
                     print(f"找到第{path_count}次與 {friend_of_friend} 最短路徑")
            else:
                shortest_paths[friend_of_friend] = [cur_path]
                print(f"找到第1次與 {friend_of_friend} 最短路徑")
                visited.append((cur_path,friend_of_friend))
    return shortest_paths

def betweenness_centrality(user_shortest_paths):
    """
    Keyword arguments:
        user_shortest_paths - {from_user:{to_user:[[shortest_path],[shortest_path]]}}
    Returns:
       user_betweenness_centrality - {user_id:betweenness_centrality}
    """
    #all_short_paths
    
    frequency_of_visits = defaultdict(int)
    total_shortest_paths = 0
    for from_user in user_shortest_paths:
        for to_user in user_shortest_paths[from_user]:
            for path in user_shortest_paths[from_user][to_user]:
                if len(path) == 2:
                    continue
                for node in path[1:-1]:
                    frequency_of_visits[node] += 1
                total_shortest_paths += 1
    
    users = user_shortest_paths.keys()
    user_betweenness_centrality = {user:frequency_of_visits[user]/total_shortest_paths
                                   for user 
                                   in users}
    return user_betweenness_centrality
        
users = construct_users_friends(friendships)
#shortest_paths_from("郭靖",users)
user_shortest_paths = {}
for from_user in users:
    user_shortest_paths[from_user] = shortest_paths_from(from_user,users)

user_betweenness_centrality = betweenness_centrality(user_shortest_paths)
#%%
#closeness
def closeness_centrality(user_shortest_paths):
    user_closeness_centrality = defaultdict(lambda :[0,0])
    for user in user_shortest_paths:
        for to_user in user_shortest_paths[user]:
            user_closeness_centrality[user][0] += len(user_shortest_paths[user][to_user][0])
            user_closeness_centrality[user][1] += 1
            
    return {user:1/(count[0]/count[1]) for user,count in user_closeness_centrality.items()}

user_closeness_centrality = closeness_centrality(user_shortest_paths)
#%%package
G = nx.Graph()
G.add_edges_from(friendships)
b = nx.betweenness_centrality(G,
                              weight=None,
                              normalized=True,
                              endpoints=False)
