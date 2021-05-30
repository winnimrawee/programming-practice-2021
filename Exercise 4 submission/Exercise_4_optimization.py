import numpy as np
from optimization1 import *



def exercise_4():
    #Set Parameters
    trials = 30
    F = 1.0
    number_of_variables = 2
    number_of_individuals = 100
    upper_bound = 10
    lower_bound = -5
    generations = 1000
    evaluation = salomon
    graph = False  # Task 3: Set to True to see graph
    
    de_all = []
    pso_all = []
    for c in range(trials):
        print('Trial DE:', c+1)
        de = DE(generations, number_of_variables, number_of_individuals, F, evaluation, lower_bound, upper_bound, graph)
        x = de.optimize1()
        print('Average of last generation:', x, '\n')
        de_all.append(x)
        print('Trial PSO:', c+1)
        pso = PSO(generations, number_of_individuals, number_of_variables, upper_bound, lower_bound, evaluation, graph)
        y= pso.optimize()
        pso_all.append(y)
        print('Average of last generation:', y, '\n\n\n')

    print("--------SUMMARY---------\n")
    de_all_avg = np.mean(de_all)
    pso_all_avg = np.mean(pso_all)
    print("Average of DE from", trials, 'runs is: ', de_all_avg)
    print("Average of PSO from", trials, 'runs is: :' , pso_all_avg)
    print('Method used:', de.evaluation.__name__)
    print('Sample range was from', lower_bound, 'to', upper_bound)
    print('Number of Variables: ', de.number_of_vairables)

# RUN
exercise_4()
