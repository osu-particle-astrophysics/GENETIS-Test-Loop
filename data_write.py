## This program reads in information from our assorted files and writes it into a single, easy to read and store file.

## Imports
import csv
import argparse
import math
import numpy as np


## Read in arguement
parser = argparse.ArgumentParser();
parser.add_argument("Design", type=str)
parser.add_argument("Gen", type=int)
parser.add_argument("NPop", type=int)
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

# Find DNA vector parameters based on design
if (g.Design == "ARA"):
    sections = 2
    genes = 4
  
elif (g.Design == "AREA"):
    sections = 2
    genes = 14

elif (g.Design == "PUEO"):
    sections = 1
    genes = 7
  
# Define list to hold dna
dna = [[[0]*genes for i in range(sections)] for j in range(g.NPop+1)]

## read in parent file for seed, individuals, parents, and opperators
if (g.Gen==0):
    for i in range(g.NPop):
        individual.append(i+1)
        parent1.append("NA")
        parent2.append("NA")
        opperator.append("NA")
else:
    with open("parents.csv") as f1:
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
with open('chiScores.csv') as f2:
    csv_read = csv.reader(f2, delimiter = ',')
    for i, row in enumerate(csv_read):
        if i > 1:
            chi.append(str(round(float(row[0]), 8)).rjust(12, ' '))
f2.close()

## Read in fitness score and error
with open('fitnessScores.csv') as f3:
    csv_read = csv.reader(f3, delimiter = ',')
    for i, row in enumerate(csv_read):
        if i > 1:
            fitness.append(str(round(float(row[0]), 8)).rjust(10, ' '))
            error.append(str(round(float(row[1]), 8)).rjust(10, ' '))
f3.close()

## Read in DNA
with open('generationDNA.csv') as f4:
    csv_read = csv.reader(f4, delimiter = ',')
    individual_no = 0
    for i, row in enumerate(csv_read):
        if( i > 8):
            if( (i-9)%sections == 0 ):
                j=0
            if( (i-9)%sections != 0 ):
                j=(i-9)%sections
            for k in range(genes):
                dna[individual_no][j][k] = float(row[k])
            if ( j == (i-9)%sections and (i-9)%sections != 0):
                individual_no = individual_no + 1
                
print(dna)

## Write Data into file
with open('generationData.csv', "w") as f5:
    # Write out the header
    f5.write("Generation Data for generation " +str(g.Gen)+ '\n')
    f5.write(seed+ '\n')
    f5.write('\n')
    f5.write("Individual, Chi, Fitness, Error, Parent 1, Parent 2, Opperator")
    for x in range(sections*genes):
        f5.write(", Gene " +str(x+1))
    f5.write('\n')
    
    # Write data
    for i in range(len(individual)):
        f5.write(str(individual[i]))
        f5.write(", " + str(chi[i]) )
        f5.write(", " +str(fitness[i]))
        f5.write(", " +str(error[i]))
        f5.write(", " +str(parent1[i]))
        f5.write(", " +str(parent2[i]))
        f5.write(", " +str(opperator[i]))
        for j in range(sections):
            for i in range(genes):
                f5.write(", " +str(dna[i][j][k]))
        f5.write( "\n")
f5.close()
