import csv
import numpy as np
import argparse
import random
import math

parser = argparse.ArgumentParser();
parser.add_argument("Gen", type=int)
g = parser.parse_args()

## define the target bicone


## Bicone 1:
#0.805509,46.834,-0.00367457,0.241596
#6.63162,38.9667,-0.00142568,0.0386078


# Bicone 2:
#6.0752,49.2369,0.00201547,-0.126026
#2.51994,39.3388,0.0033282,-0.0635223


# Bicone 3:
#6.12781,39.2655,-0.00404388,0.0344241
#5.99898,68.8562,0.00308239,-0.193231

# Bicone 4:
#0.304913,67.2326,0.0,0.0661881
#1.60948,113.61,0.0,0.507206

Bicone_List = [0.805509,46.834,-0.00367457,0.241596, 2.51994,39.3388,0.0033282,-0.0635223]


Radius1 = Bicone_List[0] #1.7
Radius2 = Bicone_List[4] #1.7
Length1 = Bicone_List[1] #121.0
Length2 = Bicone_List[5] #121.0
Theta1 = Bicone_List[2] # -.001 # this is A on the curved bicones
Theta2 = Bicone_List[6] #.034
B_coeff1 = Bicone_List[3] # .01 #curved only
B_coeff2 = Bicone_List[7] #.01 
# these are defined randomly

# define vectors for holding values
r1 = []
r2 = []
l1 = []
l2 = []
t1 = []
t2 = []
b1 = [] #curved only
b2 = []

# read in values to the arrays
with open("generationDNA.csv") as f:
    csv_read = csv.reader(f, delimiter = ',')
    for i, row in enumerate(csv_read):
        if i > 8:
            if( i%2 != 0):
                r1.append(float(row[0]))
                l1.append(float(row[1]))
                t1.append(float(row[2]))
                b1.append(float(row[3]))
            if(i%2 == 0):
                r2.append(float(row[0]))
                l2.append(float(row[1]))
                t2.append(float(row[2]))
                b2.append(float(row[3]))
f.close()
# find each individuals fitness score
fitness = []
error = []
for i in range(0, len(r1)):
    
    R1_fit = abs(((r1[i]-Radius1)**2)/Radius1)
    R2_fit = abs(((r2[i]-Radius2)**2)/Radius2)
    L1_fit = abs(((l1[i]-Length1)**2)/Length1)
    L2_fit = abs(((l2[i]-Length2)**2)/Length2)
    T1_fit = abs(((t1[i]-Theta1)**2)/Theta1)
    T2_fit = abs(((t2[i]-Theta2)**2)/Theta2)
    b1_fit = abs(((b1[i]-B_coeff1)**2)/B_coeff1)
    b2_fit = abs(((b2[i]-B_coeff2)**2)/B_coeff2) 

    Chi = R1_fit+R2_fit+L1_fit+L2_fit+T1_fit+T2_fit+b1_fit+b2_fit
    
    fitness.append(np.log10(1.0/(Chi))+1)


for i in range(0, len(fitness)): #introduce error
    if (fitness[i] == 0):
        error.append(0.0)
    else:
        error.append(0.0)
    fitness[i] = random.gauss(fitness[i], 0.0)

with open('fitnessScores.csv', "r") as f2:
    lines = f2.readlines()
    print(len(lines))
f2.close()
print(len(lines))
lines2 = []
with open(str(g.Gen)+'_fitnessScores.csv', "w") as f3:
    for x in range(0, len(fitness)+2):
        if x <= 1:
            lines2.append(str(lines[x]))
        elif x>1:
            lines2.append(str(fitness[x-2]) +"," + str(error[x-2]) + '\n')
    f3.writelines(lines2)
f3.close()

print("Max Fitness: " +str(max(fitness)))            
