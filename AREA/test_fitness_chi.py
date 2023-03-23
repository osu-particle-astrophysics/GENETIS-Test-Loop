# Imports
import csv
import numpy as np
import argparse
import random
import math


# Parse arguments
parser = argparse.ArgumentParser();
parser.add_argument("Gen", type=int)
parser.add_argument("NPop", type=int)
parser.add_argument("Source", type=str)
g=parser.parse_args()

# Store some target Gain Patterns
# Gain Pattern 1 (gen0, child0)
#3.54491,0.297905,-0.535914,0.614219,0.179899,0.361058,-0.035016,-0.0683897,-0.280901,-0.516088,0.0234517,0.484627,0.453672

# Define target gain pattern
target = [3.54491,0.297905,-0.535914,0.614219,0.179899,0.361058,-0.035016,-0.0683897,-0.280901,-0.516088,0.0234517,0.484627,0.453672]

# Define list to hold each antennas observed gain pattern
observed = [[0]*len(target) for i in range(g.NPop+1)]

# Read in values to the arrays
with open(str(g.Source) + "/results_gen" + str(g.Gen) + ".csv") as f:
    csv_read = csv.reader(f, delimiter = ',')
    for i, row in enumerate(csv_read):
        if i > 0:
            #sanity check row:
            #print(row[2])
            for j in range(len(target)):
                observed[i-1][j] = float(row[j+3])           
f.close()

# Define lists to store scores
fitness = []
error = []
chi2 = []

# Solve for Chi-squared scores
for i in range(0, g.NPop):
    tempChi2 = 0
    for j in range(len(target)):
        tempChi2 = tempChi2 + abs(((observed[i][j]-target[j])**2)/target[j])
    chi2.append(tempChi2)

# Translate Chi-Squared into fitness score
fitness = [(1/(x+1)) for x in chi2]

# Introduce error to fitness score
for i in range(0, len(fitness)):
    if (fitness[i] == 0):
        error.append(0.0)
    else:
        error.append(0.1)
        tempFit = fitness[i]
        tempFit = random.gauss(fitness[i], 0.1)
        while(tempFit < 0):
            tempFit = random.gauss(fitness[i], 0.1)
        fitness[i] = tempFit

# Write csv with data for the generation
with open(str(g.Source) + '/gen' + str(g.Gen) + '_Scores.csv', "w") as f2:
    for x in range(0, len(fitness)+1):
        if x < 1:
            f2.write("chi2, fitness, error\n")
        elif x>=1:
            f2.write(str(chi2[x-1]) + ", " + str(fitness[x-1]) + ", " + str(error[x-1]) + "\n")
f2.close

print("Max fitness: " + str(max(fitness)))
print("Min Chi-squared: " + str(min(chi2)))
