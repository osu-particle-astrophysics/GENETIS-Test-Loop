# 4/12/2023
# by: Ryan T Debolt, Bryan Reynolds
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
average_gen2 = []
sigma_average_gen = []
sigma_average_gen2 = []
run_name = []
bench_mark = 0.25 ## the benchmark we are trying to be bellow in chi score
bench_mark2 =0.1 

for a in range(0,101,10): 
	for b in range(0,101,10): 
		for r in range(0,101,10):
			for d in range(0,101,10):
				if (a+b+r+d == 100):
					count = count+1
					color = iter(cm.rainbow(np.linspace(0,1,11)))
					temp_benchmark_gen = [] ## 
					temp_benchmark_gen2 = []
					run_name.append(str(a) +'_'+ str(b) +'_'+ str(r) +'_'+ str(d))
					for e in range(1,11):
						temp_earliest = 50 ## Need to find the earliest gen where BM passed for each run
						temp_earliest2 = 50
						c=next(color)
						averages =[] # store average fitness score for each generation of test 
						highs = [] # store highest fitness score for each generation of test
						lows = [] # store Chi squared minimums
						gen_num = []
						for x in range(0,51,1):
							gen_num.append(x) #stores generation numbers
						for gens in range(0,51):
							runname= str(a) +'_'+ str(b) +'_'+ str(r) +'_'+ str(d) +'_'+ str(e) +'_'+ str(gens) 
							fit = [] # store all the fitness scores of a single generation
							chi = [] # store all the chi scores of a single generation
							with open(str(runname) + '_Scores.csv') as F1:
								txt_read = csv.reader(F1, delimiter = ",")
								for i, row in enumerate(txt_read):
									if i > 0:
										fit.append(float(row[1]))
										chi.append(float(row[0]))
							averages.append(mean(fit))
							highs.append(max(fit))
							lows.append(min(chi))
                    
							## Now update temp_earliest
							if(min(chi) <= bench_mark and gens < temp_earliest): # check if the min chi score is bellow threshold 
								temp_earliest = gens
							if(min(chi) <= bench_mark2 and gens < temp_earliest2):
								temp_earliest2 = gens
						temp_benchmark_gen.append(temp_earliest) 
						temp_benchmark_gen2.append(temp_earliest2)

						# fig, ax = plt.subplots() 
						plt.figure(count, figsize=(16,9))
						plt.plot(gen_num, lows, c=c, linestyle = 'dotted', label =('Run'+str(e)+'average'))
						plt.plot(gen_num, highs, c=c, linestyle = 'solid', label = ('Run'+str(e)+'High'))
						plt.axis([0,50, 0.00, 1.25])
						plt.grid(visible=True, which='major', color = '#666666', linestyle = '-', linewidth =0.5)
						plt.minorticks_on()
						plt.grid(visible=True, which = 'minor', color = '#999999', linestyle = '-', linewidth=0.2, alpha = 0.5)
						plt.ylabel('Scores')
						plt.xlabel('Generations')
						plt.suptitle('Parameter:'+str(a)+'RC' +str(b)+'RM' +str(r)+'TC' +str(d)+'TM')
						plt.savefig("plot" +  str(a) +'_' + str(b)+'_' + str(r)+'_' + str(d) +'.png')
					plt.close()
					print("plot "+ str(a) +'_'+ str(b) +'_'+ str(r) +'_'+ str(d) +" complete")
					earliest_gen.append(min(temp_benchmark_gen))
					average_gen.append(mean(temp_benchmark_gen))
					average_gen2.append(mean(temp_benchmark_gen2))
					sigma_average_gen.append(stat.pstdev(temp_benchmark_gen))
					sigma_average_gen2.append(stat.pstdev(temp_benchmark_gen))




with open("Master_gen.csv", 'w') as f:
	f.write("Run Name, \t Earliest, \t Average (.25), \t Standard Deviation (.25), \t Average (.1), \t Standard Deviation (.1) \n")
	for x in range(0, len(run_name)):
		f.write(str(run_name[x]) + ", \t " + str(earliest_gen[x]) + ", \t " + str(average_gen[x]) + ", \t " + str(sigma_average_gen[x]) +", \t" +str(average_gen2[x]) + ", \t" + str(sigma_average_gen2[x]) + "\n")

f.close()
print( "Master_gen.csv written")
