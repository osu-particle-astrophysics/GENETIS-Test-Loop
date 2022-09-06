# 8/15/2022
# by: Ryan T Debolt
# go through each file of a generation, gather and plot/save important information into a single file.
import csv
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import matplotlib.colors as mcolors
from cycler import cycler
import statistics as stat
from statistics import mean
import numpy as np

count = 0
run_name = []

for d in range(0,13,4): # 2,22,2
        for e in range(88,101,4): #60,90,10
                if((e-80)%4 == 0 or (e == 72 and d == 6)):
                        de = d+e
                        if (de <= 100):
                                for f in range(15,26,5):
                                        if((e == 72 and d == 6 and f == 5) or (e-80)%4 == 0):
                                                g_range = 6
                                                if f == 0:
                                                        g_range = 4
                                                else:
                                                        g_range = 8
                                                for g in range(3,g_range,1):
                                                        if((e == 72 and d == 6 and f == 5 and g == 1) or (e-80)%4 == 0):
                                                                count = count+1
                                                                for h in range(1,11):
                                                                        runname= (str(d) +'_'+ str(e) +'_'+ str(f) +'_'+ str(g)+'_2_2_6_' +str(h))
                                                                        with open(runname + "_fullData.csv", 'w' ) as F1:
                                                                                for gens in range(0,51):
                                                                                        runname2= str(d) +'_'+ str(e) +'_'+ str(f) +'_'+ str(g) +'_2_2_6_'+ str(h) +'_'+ str(gens) 
                                                                                        with open(str(runname2) + '_generationData.csv') as F2:
                                                                                                lines = F2.readlines()
                                                                                        F2.close()
                                                                                        F1.writelines(lines)
                                                                                        F1.write('\n')
                                                                        F1.close()
                                                                        print(str(runname)+ " Written")
                                                                                                
