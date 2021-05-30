from tkinter import BooleanVar
import numpy as np
import matplotlib.pyplot as plt
import random
from mpl_toolkits.mplot3d import Axes3D


def mutation(pop, number_of_individuals, F):
    index1 = np.random.randint(number_of_individuals)
    index2 = np.random.randint(number_of_individuals)
    index3 = np.random.randint(number_of_individuals)
    mut_vector = (pop[index1] - pop[index2])*float(F) + pop[index3]
    return mut_vector

def crossover(father, mut_vector, number_of_variables):
    child = [father[i] if np.random.rand() < 0.8 else mut_vector[i] for i in range(number_of_variables)]
    return child





### OBJECTIVE FUNCTIONS ###
def rosenbrock(var):
    tmp = 0
    for i in range(len(var)-1):
        tmp += 100*np.power(var[i+1]-np.power(var[i],2),2)+np.power(var[i]-1,2)
    return tmp

def salomon(variables):
    var = np.array(variables)
    return 1.0 - np.cos(2.0*np.pi*np.sqrt(sum(var**2.0))) + 0.1*np.sqrt(sum(var**2.0))

def sphere(variables):
    #Sphere
    return np.sum(np.square(variables))





# For Graphing
fig = plt.figure(figsize=(8, 8))



######### Task 1  (Modified DE) ##########
# I modified DE so that it evaluation and some other 
class DE:

    def __init__(self, generation, number_of_variables, number_of_individuals, F, evaluation, lower_bound, upper_bound, graph = BooleanVar):
        self.number_of_vairables = number_of_variables
        self.number_of_individuals = number_of_individuals
        self.pop = np.random.uniform(low=lower_bound, high=upper_bound, size=(number_of_individuals, number_of_variables))
        self.F = F
        self.evaluation = evaluation
        self.generations = generation
        self.graph = graph

    def optimize1(self):

        if self.graph == True:
            if self.number_of_vairables == 2:
                ax = fig.add_subplot(111)
                plt.xlim(-10, 10)
                plt.ylim(-10, 10)

            if self.number_of_vairables == 3:
                ax = fig.add_subplot(111, projection = '3d')
                ax.set_zlim(0,30)
                plt.xlim(-10, 10)
                plt.ylim(-10, 10)

        for gen in range(self.generations):
            lowest = float("inf")
            position = None
            pop_eval = []
            x= []
            y= []
            z= []
            for index, individual in enumerate(self.pop):

                mut_vector = mutation(self.pop, self.number_of_individuals, self.F)
                child = crossover(individual, mut_vector, self.number_of_vairables)

                if self.evaluation(child) < self.evaluation(individual):
                    self.pop[index] = child
                

                # GRAPHING
                if self.graph == True:
                    if self.number_of_vairables == 2:
                        x.append(self.pop[index][0])
                        y.append(self.pop[index][1])
                    if self.number_of_vairables == 3:
                        x.append(self.pop[index][0])
                        y.append(self.pop[index][1])
                        z.append(self.pop[index][2])
    

                if gen == self.generations - 1:
                    pop_eval.append(self.evaluation(self.pop[index]))
                    if self.evaluation(self.pop[index]) < lowest:
                        lowest = self.evaluation(self.pop[index])
                        position = self.pop[index]

            # GRAPHING
            if self.graph == True:
                if self.number_of_vairables == 2:
                    c = ax.scatter(x,y)
                    plt.draw()
                    plt.pause(0.000001)
                    c.remove()
                if self.number_of_vairables == 3:
                    c = ax.scatter(x,y,z)
                    plt.draw()
                    plt.pause(0.000001)
                    c.remove()
    

            # Displaying Final REsult
            if gen == self.generations - 1:            
                avg_evaluation= np.mean(pop_eval)
                print("Best Individual:", position)
                print('Best Solution:', lowest)
                return avg_evaluation


######### Task 2: Method chosen = Particle Swarm Optimization  #############

class Particle:
    def __init__(self, number_of_variables, position):
        self.particle_position=position                     # particle position
        self.particle_velocity=self.velocity = np.random.uniform(low=-1, high=1, size=number_of_variables)                     # particle velocity
        self.local_best_particle_position=[]          # best position of the particle
        self.fitness_local_best_particle_position = initial_fitness # start from infinity (lower is better)
        self.number_of_variables = number_of_variables
    
           
    def evaluate(self,evaluation):
        self.fitness_particle_position = evaluation(self.particle_position)
        if self.fitness_particle_position < self.fitness_local_best_particle_position:
            self.local_best_particle_position=self.particle_position                  # update the local best
            self.fitness_local_best_particle_position=self.fitness_particle_position  # update the fitness of the local best
        


    def update_velocity(self,global_best_particle_position):
        # Constants for PSO
        weight=0.75                 
        cognative=1                    
        social=2                     

        for i in range(self.number_of_variables):
            r1=random.random()
            r2=random.random()
            # Formula for PSO
            cognitive_velocity = cognative * r1 * (self.local_best_particle_position[i] - self.particle_position[i])
            social_velocity = social * r2 * (global_best_particle_position[i] - self.particle_position[i])
            self.particle_velocity[i] = weight * self.particle_velocity[i]+ cognitive_velocity + social_velocity
  
    def update_position(self,upper_bound, lower_bound):
        for i in range(self.number_of_variables):
            self.particle_position[i]=self.particle_position[i]+self.particle_velocity[i]
  
            # Make sure to not go out of bound
            if self.particle_position[i] > upper_bound:
                self.particle_position[i] = upper_bound
            if self.particle_position[i] < lower_bound:
                self.particle_position[i] = lower_bound
                

initial_fitness = float("inf")  # Infinity

class PSO:
    def __init__(self, generation, number_of_individuals, number_of_variables, upper_bound, lower_bound, evaluation, graph = BooleanVar):
        self.fitness_global_best_particle_position = initial_fitness
        self.global_best_particle_position=[]
        self.swarm_particle = []
        self.generation = generation
        self.number_of_individuals = number_of_individuals
        self.number_of_variables = number_of_variables
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound
        self.graph = graph
        self.population = np.random.uniform(low=lower_bound, high=upper_bound, size=(number_of_individuals, number_of_variables))
        self.evaluation = evaluation
        for i in range(number_of_individuals):
            self.swarm_particle.append(Particle(number_of_variables, self.population[i]))
    
    def optimize(self):

        # For Graphing
        if self.graph == True:
            if self.number_of_variables == 2:
                ax = fig.add_subplot(111)
                plt.xlim(-10, 10)
                plt.ylim(-10, 10)

            if self.number_of_variables == 3:
                ax = fig.add_subplot(111, projection = '3d')
                ax.set_zlim(0,30)
                plt.xlim(-10, 10)
                plt.ylim(-10, 10)

        for gen in range(self.generation):
            pop_eval = []
            x= []
            y= []
            z= []
            for j in range(self.number_of_individuals):
                self.swarm_particle[j].evaluate(self.evaluation) 
                pop_eval.append(self.swarm_particle[j].fitness_particle_position)
                if self.swarm_particle[j].fitness_particle_position < self.fitness_global_best_particle_position:
                    self.global_best_particle_position = self.swarm_particle[j].particle_position.copy()
                    self.fitness_global_best_particle_position = self.swarm_particle[j].fitness_particle_position.copy()
                
            for j in range(self.number_of_individuals):
                self.swarm_particle[j].update_velocity(self.global_best_particle_position)
                self.swarm_particle[j].update_position(self.upper_bound, self.lower_bound)
                if self.graph == True:
                    if self.number_of_variables == 2:
                        x.append(self.swarm_particle[j].particle_position[0])
                        y.append(self.swarm_particle[j].particle_position[1])
                    if self.number_of_variables == 3:
                        x.append(self.swarm_particle[j].particle_position[0])
                        y.append(self.swarm_particle[j].particle_position[1])
                        z.append(self.swarm_particle[j].particle_position[2])
            if gen == self.generation-1:
                self.gen_avg = np.mean(pop_eval)
    
            if self.graph == True:
                if self.number_of_variables == 2:
                    v = ax.scatter(x,y)
                    plt.draw()
                    plt.pause(0.000001)
                    v.remove()
                if self.number_of_variables == 3:
                    v = ax.scatter(x,y,z)
                    plt.draw()
                    plt.pause(0.000001)
                    v.remove()
            
        # Display the best individual in the last generation 
        print("Best Individual:", self.global_best_particle_position)
        print('Best solution:', self.fitness_global_best_particle_position)
        return self.gen_avg

    