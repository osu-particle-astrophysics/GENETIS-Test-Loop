# Code to draw the family tree of a chosen individual in a generation

# IMPORTS
import numpy as np
import csv
import matplotlib.pyplot as plt
import argparse
import math


# Read in evolution data arguments
parser = argparse.ArgumentParser();
parser.add_argument("Pop", type=int)
parser.add_argument("Gens", type=int)
g = parser.parse_args()

# input the individual and generation that you want to trace

individual = int(input("Enter the individual number: "))
while (individual > g.Pop):
    individual = int(input("Please enter valid individual: "))

generation = int(input("Enter the generation number: "))
while (generation > g.Gens):
    generation = int(input("Please enter valid generation: "))

runtype = str(input("Enter the run type code for the parent files: "))

# Find the predessesors of the individual

# initialize array of locations
data = [[[0 for c in range(2)] for b in range(g.Pop+1)] for a in range(g.Gens+1)] # [generation] [individual] [parents]
# print(data)
                
gen = generation
ind = [] # array to store individuals  
ind.append(individual)


while (gen >= 0): # loop until all generations prior to the chosen one
    print("Generation: " +str(gen))
    temp_ind =[]
    print(len(ind))
    for x in range(len(ind)): # loop over all older relatives of the chosen individual
        #print("individual: " +str(ind[x]))
        with open(runtype + '_' + str(gen) + '_Parents.csv') as f1: # read in parent file of the generation
            csv_read = csv.reader(f1, delimiter = ',')
            for i, row in enumerate(csv_read):
                if (i==3+ind[x]):
                    # store the parent data for this generation
                    if (str(row[1]) != ' NA' and str(row[2]) != ' NA'):
                        data[gen][ind[x]-1][0] = int(row[1])
                        data[gen][ind[x]-1][1] = int(row[2])
                        temp_ind.append(int(row[1]))
                        temp_ind.append(int(row[2]))
                    elif (str(row[1]) != ' NA' and str(row[2]) == ' NA'):
                        data[gen][ind[x]-1][0] = int(row[1])
                        data[gen][ind[x]-1][1] = int(row[1])
                        temp_ind.append(int(row[1]))
        
        f1.close()
    ind.clear()
    ind = list(set(temp_ind))
    temp_ind.clear()
    gen = gen-1

print(data)
