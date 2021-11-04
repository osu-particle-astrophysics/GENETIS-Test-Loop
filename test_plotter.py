#plot the invidviduals at each generation
import matplotlib.pyplot as plt
import csv
import argparse
import math

parser = argparse.ArgumentParser();
parser.add_argument("Npop", type=int)
parser.add_argument("Gen", type=int)
g = parser.parse_args()

generations=[]
scores=[]
max_scores = []
for z in range(0, g.Gen):
    with open(str(z)+"_fitnessScores.csv") as f:
        txt_read = csv.reader(f, delimiter = ',')
        for i, row in enumerate(txt_read):
          #  print(i)
            if i>1:
             #   print("i>1")
                scores.append(float(row[0]))
              #  print(scores)
    max_scores.append(max(scores))
    generations = [z for f in range(0, g.Npop)]
    plt.title('Non-Linear Bicone Evolution test')
    plt.plot(generations, scores, '.', color = 'indigo')
    #plt.plot(z, max(scores), 'o', color = 'b', markersize='4')
    plt.ylabel('Fitness Scores')
    plt.xlabel('Generations')
    plt.axis([0,g.Gen, 0, 150])
    plt.grid(b=True, which='major', color = '#666666', linestyle = '-', linewidth =0.5)
    plt.minorticks_on()
    plt.grid(b=True, which = 'minor', color = '#999999', linestyle = '-', linewidth=0.2, alpha = 0.5)
    generations.clear()
    scores.clear()

generations = [f for f in range(0, g.Gen)]
plt.plot(generations, max_scores, linestyle = '-', color = 'b')

plt.savefig("fitness.png")


scores2=[]
with open("fitnessScores.csv") as f2:
    txt_read = csv.reader(f2, delimiter = ',')
    for i, row in enumerate(txt_read):
        if i>1:
            scores2.append(float(row[0]))
print(max(scores2)) 
