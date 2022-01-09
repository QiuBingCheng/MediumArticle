# -*- coding: utf-8 -*-
"""
Created on Sat Jul 24 15:56:22 2021

@author: Jerry
"""
import numpy as np
import pandas as pd
from itertools import combinations
from collections import namedtuple
import matplotlib.pyplot as plt
import sys
#%%
class TSPProblem:
    def __init__(self,coordinate,cities_name):
        self.coordinate = coordinate
        self.cities_name = cities_name
        self.city_count = len(self.cities_name)
        
    def get_distance(self,arr1,arr2):
        #Euclidean distance
        return np.sqrt(np.power(arr1-arr2,2).sum())
    
    def compute_objective_value(self,cities_id):
        total_distance = 0
        for i in range(len(cities_id)):
            city1 = cities_id[i]
            city2 = cities_id[i+1] if i<len(cities_id)-1 else cities_id[0]
            total_distance += self.get_distance(self.coordinate[city1],self.coordinate[city2])
        return total_distance
    
    def to_cities_name(self,cities_id):
        return [self.cities_name[i] for i in cities_id]
 #%%
Move = namedtuple('Tabu', ['i1', 'v1','i2','v2'])

class TabuSearch:
    def  __init__(self,
                  var_num,
                  target_fun,
                  tabu_size,
                  iteration_num = 50,
                  after_iteration = None
                  ):
        
        self.var_num = var_num
        self.iteration_num = iteration_num
        self.tabu_size = tabu_size
        self.target_fun = target_fun
        self.after_iteration = after_iteration
            
        self.reset()
          
    def reset(self):
        self.iteration = 0
        self.tabu_list = [] 
         
        #all combination of swapped index
        self.candidate_swapped_index = list(combinations(list(range(self.var_num)), 2))
        self.candiate_count = len(self.candidate_swapped_index)
        
        #initialize solution 
        self.current_sol = [i for i in range(self.var_num)]
        self.the_best_sol = self.current_sol[:]
        self.the_best_val = self.target_fun(self.current_sol)
        
        #record best value for plot
        self.best_value_in_iteration = [] 
        self.best_value_in_history = [] 
    
    def swap_move(self,sol,move):
        #swap index
        sol[move.i1],sol[move.i2] = sol[move.i2],sol[move.i1]
        return
    
    def run(self):
        for iteration in range(self.iteration_num):
            self.run_one_iteration()

    def run_one_iteration(self):
        neighbor_best_val = sys.maxsize
        neighbor_best_sol = None
        neighbor_best_move = None
        
        non_tabu_neighbor_best_val = sys.maxsize
        non_tabu_neighbor_best_move = None
        
        for swapped_index in self.candidate_swapped_index:
            i1,i2 = swapped_index
            move = Move(i1,self.current_sol[i1],i2,self.current_sol[i2])
            
            neighbor_sol =  self.current_sol[:]
            self.swap_move(neighbor_sol, move)
            neighbor_value = self.target_fun(neighbor_sol)
            
            #check if it is in tabu
            violated = False
            for tabu_move in self.tabu_list:
                if (tabu_move.i1 == i1 and tabu_move.v1 == neighbor_sol[i1] and \
                    tabu_move.i2 == i2 and tabu_move.v2 == neighbor_sol[i2]):
                    violated = True
                    break   
            
            if neighbor_value<neighbor_best_val:
                neighbor_best_val = neighbor_value
                neighbor_best_sol = neighbor_sol[:]
                neighbor_best_move = move
                
            if not violated and neighbor_value<non_tabu_neighbor_best_val:
                non_tabu_neighbor_best_val = neighbor_value
                non_tabu_neighbor_best_move = move
        
        #udpate
        #better than aspiration level
        if(neighbor_best_val<self.the_best_val):
            self.the_best_val = neighbor_best_val
            self.the_best_sol = neighbor_best_sol
            
            #udpate move
            self.swap_move(self.current_sol, neighbor_best_move)
            
            #remove if it is in tabu list
            if move in self.tabu_list:
                self.tabu_list.remove(move)
            #insert to head    
            self.tabu_list.insert(0,neighbor_best_move)
            
                
        else :
             #udpate move
             self.swap_move(self.current_sol, non_tabu_neighbor_best_move)
             self.tabu_list.append(non_tabu_neighbor_best_move)
        
        # save best value
        self.best_value_in_iteration.append(neighbor_best_val)
        self.best_value_in_history.append(self.the_best_val)
        
        if len(self.tabu_list) > self.tabu_size:
            self.tabu_list.pop()
        
        if self.after_iteration:
            self.after_iteration(self)
        
        self.iteration += 1
#%%
data = pd.read_csv("data/Latitude and Longitude of Taiwan County.csv")
coordinate = data.iloc[:,1:].values   
problem = TSPProblem(coordinate,data["縣市"].values)  

def output_message(tabu_search):
    print(f"=====Itieration {tabu_search.iteration}=====")
    print(f"Best Solution = {tabu_search.the_best_sol}")
    print(f"Best Value    = {tabu_search.the_best_val}")

tabu = TabuSearch(var_num=problem.city_count,
                  target_fun=problem.compute_objective_value,
                  tabu_size=5,
                  iteration_num = 20,
                  after_iteration=output_message)

tabu.run()

#%% plot
plt.figure(figsize=(8,6))     
plt.plot(tabu.best_value_in_iteration,marker="o",color = "y")
plt.plot(tabu.best_value_in_history,marker="o",color = "r")
plt.legend(["Best In Iteration","Best In History"],loc="upper right")
plt.xlabel("Iteration",fontsize=16)
plt.ylabel("Value",fontsize=16)
plt.title("Iteration vs Objective Value")
plt.show()