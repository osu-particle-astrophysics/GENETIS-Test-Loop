import csv
import numpy as np
import argparse
import random
import math


#parse arguments
parser = argparse.ArgumentParser();
parser.add_argument("Gen", type=int)
parser.add_argument("NPop", type=int)
g=parser.parse_args()

#Gain Pattern 1 (gen0, child0)
#3.54491,0.297905,-0.535914,0.614219,0.179899,0.361058,-0.035016,-0.0683897,-0.280901,-0.516088,0.0234517,0.484627,0.453672

#define target gain pattern
target = [3.54491,0.297905,-0.535914,0.614219,0.179899,0.361058,-0.035016,-0.0683897,-0.280901,-0.516088,0.0234517,0.484627,0.453672]

"""
c0_target = param_list[0]
c1_target = param_list[1]
c2_target = param_list[2]
c3_target = param_list[3]
c4_target = param_list[4]
c5_target = param_list[5]
c6_target = param_list[6]
c7_target = param_list[7]
c8_target = param_list[8]
c9_target = param_list[9]
c10_target = param_list[10]
c11_target = param_list[11]
c12_target = param_list[12]
#c13_target = param_list[13] #For when freq dependence is included
"""

observed = [[0]*len(target) for i in range(g.NPop+1)]

"""
c0_obs = []
c1_obs = []
c2_obs = []
c3_obs = []
c4_obs = []
c5_obs = []
c6_obs = []
c7_obs = []
c8_obs = []
c9_obs = []
c10_obs = []
c11_obs = []
c12_obs = []
#c13_obs = [] #For when freq dependence is included
"""

# read in values to the arrays
# BRYAN: coe back and fix filename once arguments are added
with open("results_gen" + str(g.Gen) + ".csv") as f:
    csv_read = csv.reader(f, delimiter = ',')
    for i, row in enumerate(csv_read):
        if i > 0:
            #sanity check row:
            print(row[2])
            for j in range(len(target)):
                observed[i][j] = float(row[j+2])
            """
            c0_obs.append(float(row[2]))
            c1_obs.append(float(row[3]))
            c2_obs.append(float(row[4]))
            c3_obs.append(float(row[5]))
            c4_obs.append(float(row[6]))
            c5_obs.append(float(row[7]))
            c6_obs.append(float(row[8]))
            c7_obs.append(float(row[9]))
            c8_obs.append(float(row[10]))
            c9_obs.append(float(row[11]))
            c10_obs.append(float(row[12]))
            c11_obs.append(float(row[13]))
            c12_obs.append(float(row[14]))
            #c13_obs.append(float(row[15])) #for when freq dependence is used
            """
f.close()

fitness = []
error = []
chi2 = []

for i in range(0, g.NPop):
    tempChi2 = 0
    for j in range(len(target)):
        tempChi2 = tempChi2 + abs(((observed[i][j]-target[j])**2)/target[j])
    chi2.append(tempChi2)
    """
    c0_fit = abs(((c0_obs[i]-c0_target)**2)/c0_target)
    c1_fit = abs(((c1_obs[i]-c1_target)**2)/c1_target)
    c2_fit = abs(((c2_obs[i]-c2_target)**2)/c2_target)
    c3_fit = abs(((c3_obs[i]-c3_target)**2)/c3_target)
    c4_fit = abs(((c4_obs[i]-c4_target)**2)/c4_target)
    c5_fit = abs(((c5_obs[i]-c5_target)**2)/c5_target)
    c6_fit = abs(((c6_obs[i]-c6_target)**2)/c6_target)
    c7_fit = abs(((c7_obs[i]-c7_target)**2)/c7_target)
    c8_fit = abs(((c8_obs[i]-c8_target)**2)/c8_target)
    c9_fit = abs(((c9_obs[i]-c9_target)**2)/c9_target)
    c10_fit = abs(((c10_obs[i]-c10_target)**2)/c10_target)
    c11_fit = abs(((c11_obs[i]-c11_target)**2)/c11_target)
    c12_fit = abs(((c12_obs[i]-c12_target)**2)/c12_target)
    #c13_fit = abs(((c13_obs[i]-c13_target)**2)/c13_target) #For when freq depen

    chi2.append(c0_fit+c1_fit+c2_fit+c3_fit+c4_fit+c5_fit+c6_fit+c7_fit+c8_fit+c9_fit+c10_fit+c11_fit+c12_fit) #remember to add c13 when freq dependence
    """

#fitness.append(1/(chi2[i]+1))
fitness = [(1/(x+1)) for x in chi2]

#introduce error
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

#write csv with data for the generation
with open('gen' + str(g.Gen) + '_testLoopData.csv', "w") as f2:
    for x in range(0, len(fitness)+1):
        if x < 1:
            f2.write("chi2, fitness, error\n")
        elif x>=1:
            f2.write(str(chi2[x-1]) + ", " + str(fitness[x-1]) + ", " + str(error[x-1]) + "\n")
f2.close

print("Max fitness: " + str(max(fitness)))
