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

# Define target gain pattern based on design
if (g.Design == "ARA"):
  target = [[0.968807,14.1263,-0.053024,0.8256] , [4.83102,10.4062,0.027465,-0.396757]]
  sections = 2
  genes = 4
  
else if (g.Design == "AREA"):
  target = [[3.54491,-0.0317852,-0.00413922,-0.0166417,-0.0334298,0.0129763,-0.0294556,0.00505468,-0.0356591,-0.0360021,0.026303,0.032135,-0.00430533,-2.28384], [-4.31513,1.52493,2.47681,-4.8304,3.92823,-4.21634,2.46806,0.274596,3.44827,-4.5354,-3.64286,2.02234,0.930429,-4.57881]]
  sections = 2
  genes = 14

else if (g.Design == "PUEO"):
  target = [[33.2056,38.6897,23.6239,14.6074,30.1627,32.4097,1.70987]]
  sections = 1
  genes = 7
  
# Define list to hold each antennas observed gain pattern
observed = [[[0]*genes for i in range(sections)] for j in range(g.NPop+1)]

# Populate the observed list from csv
ReadData(genes, observed)

# Define lists to store scores
fitness = []
error = []
chi2 = []

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


# Functions

def ReadData(genes, observed):
  # Read in data from generationDNA.csv and put it into the observed list
  with open('generationDNA.csv') as dna:
    csv_read = csv.reader(dna, delimiter = ',')
    for i, row in enumerate(csv_read):
      if( i > 8):
        
          
def ChiSquared(target, observed, sections, genes):
  # Solve for Chi-squared scores
  for i in range(0, g.NPop):
    tempChi2 = 0
    for j in range(sections):
       for k in range(genes):
        tempChi2 = tempChi2 + abs(((observed[i][j]-target[j])**2)/target[j])
    chi2.append(tempChi2)
  
