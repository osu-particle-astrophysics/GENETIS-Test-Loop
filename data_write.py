## This program reads in information from our assorted files and writes it into a single, easy to read and store file.

## Imports
import csv
import argparse
import math
import numpy as np


## Read in arguement
parser = argparse.ArgumentParser();
parser.add_argument("Gen", type=str)
g = parser.parse_args()

## Data lists and variables
seed = ''
individual =  []
parent1 = []
parent2 = []
opperator = []
fitness = []
error = [] 
chi = []
radius = [] ## temp array
radius1 = []
radius2 = []
length = [] ## temp array
length1 = []
length2 = []
Q = []      ## temp array
Q1 = []
Q2 = []
L =  []     ## temp array
L1 = []
L2 = []

## read in parent file for seed, individuals, parents, and opperators

with open(g.Gen+"_parents.csv") as f1:
    csv_read = csv.reader(f1, delimiter = ',')
    for i, row in enumerate(csv_read):
        if i==1:
            seed = str(row[0])
        elif i> 4:
            individual.append(row[0].ljust(2, ' '))
            parent1.append(row[1].ljust(2, ' '))
            parent2.append(row[2].ljust(2, ' '))
            opperator.append(row[3].rjust(13, ' '))
f1.close()


## Read in Chi score

with open(g.Gen+'_chiScores.csv') as f2:
    csv_read = csv.reader(f2, delimiter = ',')
    for i, row in enumerate(csv_read):
        if i > 1:
            chi.append(str(round(float(row[0]), 8)).rjust(12, ' '))
f2.close()


## Read in fitness score and error

with open(g.Gen+'_fitnessScores.csv') as f3:
    csv_read = csv.reader(f3, delimiter = ',')
    for i, row in enumerate(csv_read):
        if i > 1:
            fitness.append(str(round(float(row[0]), 8)).rjust(10, ' '))
            error.append(str(round(float(row[1]), 8)).rjust(10, ' '))
f3.close()
    

## Read in DNA

with open(g.Gen+'_generationDNA.csv') as f4:
    csv_read = csv.reader(f4, delimiter = ',')
    for i, row in enumerate(csv_read):
        if i > 8:
            radius.append(str(round(float(row[0]), 8)).rjust(10, ' '))
            length.append(str(round(float(row[1]), 8)).rjust(12, ' '))
            Q.append(str(round(float(row[2]), 8)).rjust(11, ' '))
            L.append(str(round(float(row[3]), 8)).rjust(11, ' '))
f4.close()


## Re-sort DNA into sides

for i in range(0, len(radius), 2):
    radius1.append(radius[i])
    radius2.append(radius[i+1])
    length1.append(length[i])
    length2.append(length[i+1])
    Q1.append(Q[i])
    Q2.append(Q[i+1])
    L1.append(L[i])
    L2.append(L[i+1])


## Write Data into file

with open(g.Gen+'_generationData.csv', "w") as f5:
    # Write out the header
    f5.write("Generation Data for generation " +g.Gen+ '\n')
    f5.write(seed+ '\n')
    f5.write('\n')
    f5.write("Individual, Chi, Fitness, Error, Parent 1, Parent 2, Opperator, Radius 1, length 1, Quadratic 1, Linnear 1, Radius 2, Length 2, Quadratic 2, Linnear 2 \n")
    
    # Write data
    for i in range(len(individual)):
        f5.write( individual[i] +', '+ chi[i] +', '+ fitness[i] +', '+ error[i] +', '+ parent1[i] +', '+ parent2[i] +', '+ opperator[i] +', '+ \
                  radius1[i] +', '+ length1[i] +', '+ Q1[i] +', '+ L1[i] +', '+ radius2[i] +', '+ length2[i] +', '+ Q2[i] +', '+ L2[i] +'\n')

f5.close()
