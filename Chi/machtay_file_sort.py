# 12/18/2020
# by: Ryan T Debolt
# go through each file, gather and plot/save important information.
import csv
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import matplotlib.colors as mcolors
from cycler import cycler
import statistics as stat
from statistics import mean
import numpy as np

count = 0
earliest_gen = []
average_gen = []
sigma_average_gen = []
run_name = []
bench_mark = 0.8 ## the benchmark we are trying to cross


for d in range(0,10,3): # 2,22,2
	for e in range(32,51,1): #60,90,10
		if((e-32)%6 == 0 or (e == 36 and d == 3)):
			de = d+e
			if (de < 50):
				for f in range(0,11,5):
					if((e == 36 and d == 3 and f == 5) or (e-32)%6 == 0):
						for g in range(1,6,1):
							if((e == 36 and d == 3 and f == 5 and g == 1) or (e-32)%6 == 0):
								count = count+1
								color = iter(cm.rainbow(np.linspace(0,1,11)))
								## MACHTAY LOOK HERE
								temp_benchmark_gen = [] ## 
								run_name.append(str(d) +'_'+ str(e) +'_'+ str(f) +'_'+ str(g))
								for h in range(1,6):
									temp_earliest = 50 ## Need to find the earliest gen where BM passed for each run
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
										## Now update temp_earliest
										if(max(gen) >= bench_mark and gens < temp_earliest):
											temp_earliest = gens
									temp_benchmark_gen.append(temp_earliest) 

									#print("averages", len(averages), averages)
									#print("highs", len(highs), averages)
									# fig, ax = plt.subplots() 
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
								earliest_gen.append(min(temp_benchmark_gen))
								average_gen.append(mean(temp_benchmark_gen))
								sigma_average_gen.append(stat.pstdev(temp_benchmark_gen))





with open("Master_gen.csv", 'w') as f:
	f.write("Run Name, \t Earliest, \t Average, \t Standard Deviation\n")
	for x in range(0, len(run_name)):
		f.write(str(run_name[x]) + ", \t " + str(earliest_gen[x]) + ", \t " + str(average_gen[x]) + ", \t " + str(sigma_average_gen[x]) + "\n")

f.close()
