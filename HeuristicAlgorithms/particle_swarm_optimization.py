# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 22:52:04 2021

@author: Jerry
"""
import random
import sys
#%%
class PSOSolver():
    def __init__(self,pop_size,dimension,upper_bounds,lower_bounds,compute_objective_value,
               cognition_factor=0.5,social_factor=0.5):
        
        self.pop_size = pop_size
        self.dimension = dimension
        self.upper_bounds = upper_bounds
        self.lower_bounds = lower_bounds
        
        self.solutions = [] #current solution
        self.individual_best_solution = [] #individual best solution
        self.individual_best_objective_value = [] #individual best val
        
        self.global_best_solution = [] #global best solution
        self.global_best_objective_value = sys.float_info.max;
        self.cognition_factor = cognition_factor #particle movement follows its own search experience
        self.social_factor = social_factor  #particle movement follows the swarm search experience
        self.compute_objective_value = compute_objective_value
        
    def initialize(self):
        min_index = 0
        min_val = sys.float_info.max
        
        for i in range(self.pop_size):
            solution = []
            for d in range(self.dimension):
                rand_pos = self.lower_bounds[d]+random.random()*(self.upper_bounds[d]-self.lower_bounds[d])
                solution.append(rand_pos)
            
            self.solutions.append(solution)
            
            #update invidual best solution
            self.individual_best_solution.append(solution)
            objective = self.compute_objective_value(solution)
            self.individual_best_objective_value.append(objective)
            
            #record the smallest objective val
            if(objective < min_val):
                 min_index = i
                 min_val = objective
            
        #udpate so far the best solution
        self.global_best_solution = self.solutions[min_index].copy()
        self.global_best_objective_value = min_val
        
    def move_to_new_positions(self):
        for i,solution in enumerate(self.solutions):
            alpha = self.cognition_factor*random.random()
            beta = self.social_factor*random.random()
            for d in range(self.dimension):
                v = alpha*(self.individual_best_solution[i][d]-self.solutions[i][d])+\
                    beta*(self.global_best_solution[d]-self.solutions[i][d])
                    
                self.solutions[i][d] += v
                self.solutions[i][d] = min(self.solutions[i][d],self.upper_bounds[d])
                self.solutions[i][d] = max(self.solutions[i][d],self.lower_bounds[d])
                
    
    def update_best_solution(self):
        for i,solution in enumerate(self.solutions):
            obj_val = self.compute_objective_value(solution)
            
            #udpate indivisual solution
            if(obj_val < self.individual_best_objective_value[i]):
                self.individual_best_solution[i] = solution
                self.individual_best_objective_value[i] = obj_val
                
                if(obj_val < self.global_best_objective_value):
                    self.global_best_solution = solution
                    self.global_best_objective_value = obj_val
                    
#%%
pop_size = 5
solver = PSOSolver(pop_size,2,[100,100],[-100,-100],compute_objective_value)
solver.initialize()

#target function
def compute_objective_value(array):
    val = 0
    for ele in array:
        val += ele*ele
    return val

for iteration in range(20):
    solver.move_to_new_positions()
    solver.update_best_solution()
    
    #print
    print(f"========iteration {iteration+1}========")
    for i,solution in enumerate(solver.solutions):
        print(f"solution {i+1}:")
        print(f"{solution}:{compute_objective_value(solution)}")
    print("global best solution:")
    print(f"{solver.global_best_solution}:{solver.global_best_objective_value}")
