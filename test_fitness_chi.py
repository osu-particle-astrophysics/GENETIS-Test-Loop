# Imports
import csv
import numpy as np
import argparse
import random
import math


# Parse arguments
parser = argparse.ArgumentParser();
parser.add_argument("Design", type=str)
parser.add_argument("Gen", type=int)
parser.add_argument("NPop", type=int)
g=parser.parse_args()

# Store some target Gain Patterns
# Gain Pattern 1 (gen0, child0)
#3.54491,0.297905,-0.535914,0.614219,0.179899,0.361058,-0.035016,-0.0683897,-0.280901,-0.516088,0.0234517,0.484627,0.453672

# Define target gain pattern based on design
if (g.Design == "ARA"):
  target = [0.968807,14.1263,-0.053024,0.8256,4.83102,10.4062,0.027465,-0.396757]
  
else if (g.Design == "AREA"):
  target = [3.54491,0.297905,-0.535914,0.614219,0.179899,0.361058,-0.035016,-0.0683897,-0.280901,-0.516088,0.0234517,0.484627,0.453672}

else if (g.Design == "PUEO"):
  target = [33.2056,38.6897,23.6239,14.6074,30.1627,32.4097,1.70987]
  
# Define list to hold each antennas observed gain pattern
observed = [[0]*len(target) for i in range(g.NPop+1)]

# Read in values to the arrays
with open("genrationDNA.csv") as f:
    csv_read = csv.reader(f, delimiter = ',')
    for i, row in enumerate(csv_read):
        if i > 8:
            if(design == "ARA"):
              if( i%2 != 0):
                for j in range(len(target/2)):
                  observed[i-8][j] = float(row[j])
              if(i%2 == 0):
                for j in range(len(target/2), len(target)):
                  observed[i-8][j] = float(row[j])
            else:
              for j in range(len(target)):
                observed[i-8][j] = float(row[j])           
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

# Write csv's with data for the generation
with open('fitnessScores.csv', "r") as fs:
    lines = fs.readlines()
fs.close()
            
lines2=[]            
with open('fitnessScores.csv', "w") as f2:
    for x in range(0, len(fitness)+2):
        if x <= 1:
            lines2.append(str(lines[x]))
        elif x>1:
            lines2.append(str(fitness[x-2]) +"," + str(error[x-2]) + '\n')
    f2.writelines(lines2)
f2.close
            
with open('chiScores.csv', "r") as fc:
    lines = fc.readlines()
fs.close()
            
lines3=[]            
with open('chiScores.csv', "w") as f2:
    for x in range(0, len(fitness)+2):
        if x <= 1:
            lines3.append(str(lines[x]))
        elif x>1:
            lines3.append(str(chi2[x-2]) + '\n')
    f2.writelines(lines3)
f3.close

print("Max fitness: " + str(max(fitness)))
print("Min Chi-squared: " + str(min(chi2)))
