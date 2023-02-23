#plot the invidviduals at each generation
import matplotlib.pyplot as plt
import csv
import argparse
import math
from statistics import mean

parser = argparse.ArgumentParser();
parser.add_argument("Npop", type=int)
parser.add_argument("Gen", type=int)
#parser.add_argument("Repro", type=int)
#parser.add_argument("Cross", type=int)
g = parser.parse_args()

generations=[]
scores=[]
chi=[]
max_scores = []
ave_scores = []
plt.figure(figsize=(16,9))
for z in range(0, g.Gen):
    with open("gen"+str(z)+"_testLoopData.csv") as f:
        txt_read = csv.reader(f, delimiter = ',')
        for i, row in enumerate(txt_read):
          #  print(i)
            if i>1:
                scores.append(float(row[1]))
                chi.append(float(row[0]))
    max_scores.append(max(scores))
    min_chi.append(min(chi))
    ave_scores.append(mean(scores))

    generations = [z for f in range(0, g.Npop)]
    #print( str(len(scores[0:g.Repro])) + "Repro") #sanity check
    plt.title('Non-Linear Bicone Evolution test')
    plt.plot(generations, scores, '.', color = 'red', markersize = '3.0', alpha=.5)
    #plt.plot(generations[g.Repro:g.Cross], scores[g.Repro:g.Cross], '.', color = 'green', markersize = '3.0', alpha=.5)
    #plt.plot(generations[0:g.Repro], scores[0:g.Repro], '*', color = 'blue', markersize ='5.0')
    plt.ylabel('Fitness Scores')
    plt.xlabel('Generations')
    #plt.axis([0,g.Gen, -0.05, 1.05])
    plt.grid(b=True, which='major', color = '#666666', linestyle = '-', linewidth =0.5)
    plt.minorticks_on()
    plt.grid(b=True, which = 'minor', color = '#999999', linestyle = '-', linewidth=0.2, alpha = 0.5)
    generations.clear()
    scores.clear()

generations = [f for f in range(0, g.Gen)]
plt.plot(generations, max_scores, linestyle = '-', color = 'black', alpha = 0.5)
plt.plot(generations, min_chi, linestyle = '-', color = 'blue', alpha = 0.5)
plt.plot(generations, ave_scores, linestyle = '--', color = 'black', alpha = 0.5)
plt.savefig("fitness.png")


scores2=[]
chi2=[]
with open("gen"+g.Gen+"_testLoopData.csv") as f2:
    txt_read = csv.reader(f2, delimiter = ',')
    for i, row in enumerate(txt_read):
        if i>1:
            scores2.append(float(row[1]))
            chi2.append(float(row[0]))
     
print("Max Fitness Score:", max(scores2)) 
print("Min Chi-Squared Value:", min(chi2))
