# 12/18/2020
# by: Ryan T Debolt
# go through each file, gather and plot/save important information. Designed to be used in the directory holding results of a run.
import csv
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import matplotlib.colors as mcolors
from cycler import cycler
from statistics import mean
import numpy as np

count = 0
for d in range(0,10,3): # 2,22,2
    for e in range(32,51,6): #60,90,10
        de = d+e
        if (de < 50):
            for f in range(0,11,5):
                for g in range(1,6,1):
                    count = count+1
                    color = iter(cm.rainbow(np.linspace(0,1,11)))
                    for h in range(1,6):
                        c=next(color)
                        averages =[] # store average fitness score for each generation of test 
                        highs = [] # store highest fitness score for each generation of test
                        gen_num = []
                        for x in range(0,51,1):
                            gen_num.append(x) #stores generation numbers
                        #print(gen_num)
                        for gens in range(0,51):
                            #print(r, c, t, g)
                            runname= str(d) +'_'+ str(e) +'_'+ str(f) +'_'+ str(g) +'_'+ str(h) +'_'+ str(gens) 
                            gen = [] # store all the fitness scores of a single generation
                            with open(str(runname) + '_fitnessScores.csv') as F1:
                                txt_read = csv.reader(F1, delimiter = ",")
                                for i, row in enumerate(txt_read):
                                    if i > 1:
                                        gen.append(float(row[0]))
                            averages.append(mean(gen))
                            highs.append(max(gen))
                        plt.figure(count, figsize=(16,9))
                        plt.plot(gen_num, averages, c=c, linestyle = 'dotted', label =('Run'+str(h)+'average'))
                        plt.plot(gen_num, highs, c=c, linestyle = 'solid', label = ('Run'+str(h)+'High'))
                        plt.axis([0,50, 0.00, 1.05])
                        plt.grid(b=True, which='major', color = '#666666', linestyle = '-', linewidth =0.5)
                        plt.minorticks_on()
                        plt.grid(b=True, which = 'minor', color = '#999999', linestyle = '-', linewidth=0.2, alpha = 0.5)
                        plt.ylabel('Fitness Score')
                        plt.xlabel('Generations')
                        plt.suptitle('Parameter:'+str(d)+'Repro' +str(e)+'cross' +str(f)+'M_Rate' +str(g)+'sigma')
                        plt.savefig("plot" +  str(d) +'_' + str(e)+'_' + str(f)+'_' + str(g) +'.png')
                    plt.close()
