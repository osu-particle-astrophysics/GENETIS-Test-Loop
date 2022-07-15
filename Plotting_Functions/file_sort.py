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
average_gen2 = []
sigma_average_gen = []
sigma_average_gen2 = []
run_name = []
bench_mark = 0.5 ## the benchmark we are trying to be bellow in chi score
bench_mark2 =0.25 

for d in range(6,19,6): # 2,22,2
	for e in range(64,101,2): #60,90,10
		if((e-64)%12 == 0 or (e == 72 and d == 6)):
			de = d+e
			if (de <= 100):
				for f in range(0,11,5):
					if((e == 72 and d == 6 and f == 5) or (e-64)%12 == 0):
						g_range = 6
						if f == 0:
							g_range = 2
						else:
							g_range = 6
						for g in range(1,g_range,1):
							if((e == 72 and d == 6 and f == 5 and g == 1) or (e-64)%12 == 0):
								count = count+1
								color = iter(cm.rainbow(np.linspace(0,1,11)))
								## MACHTAY LOOK HERE
								temp_benchmark_gen = [] ## 
								temp_benchmark_gen2 = []
								run_name.append(str(d) +'_'+ str(e) +'_'+ str(f) +'_'+ str(g))
								for h in range(5,11):
									temp_earliest = 50 ## Need to find the earliest gen where BM passed for each run
									temp_earliest2 = 50
									c=next(color)
									averages =[] # store average fitness score for each generation of test 
									highs = [] # store highest fitness score for each generation of test
									lows = [] # store Chi squared minimums
									gen_num = []
									for x in range(0,51,1):
										gen_num.append(x) #stores generation numbers
									#print(gen_num)
									for gens in range(0,51):
										#print(r, c, t, g)
										runname= str(d) +'_'+ str(e) +'_'+ str(f) +'_'+ str(g) +'_'+ str(h) +'_'+ str(gens) 
										fit = [] # store all the fitness scores of a single generation
										chi = [] # store all the chi scores of a single generation
										with open(str(runname) + '_generationData.csv') as F1:
											txt_read = csv.reader(F1, delimiter = ",")
											for i, row in enumerate(txt_read):
												if i > 3:
													fit.append(float(row[2]))
													chi.append(float(row[1]))
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

									#print("averages", len(averages), averages)
									#print("highs", len(highs), averages)
									# fig, ax = plt.subplots() 
									plt.figure(count, figsize=(16,9))
									plt.plot(gen_num, lows, c=c, linestyle = 'dotted', label =('Run'+str(h)+'average'))
									plt.plot(gen_num, highs, c=c, linestyle = 'solid', label = ('Run'+str(h)+'High'))
									plt.axis([0,50, 0.00, 1.25])
									plt.grid(b=True, which='major', color = '#666666', linestyle = '-', linewidth =0.5)
									plt.minorticks_on()
									plt.grid(b=True, which = 'minor', color = '#999999', linestyle = '-', linewidth=0.2, alpha = 0.5)
									plt.ylabel('Fitness Score')
									plt.xlabel('Generations')
									plt.suptitle('Parameter:'+str(d)+'Repro' +str(e)+'cross' +str(f)+'M_Rate' +str(g)+'sigma')
									plt.savefig("plot" +  str(d) +'_' + str(e)+'_' + str(f)+'_' + str(g) +'.png')
								plt.close()
								print("plot "+ str(d) +'_'+ str(e) +'_'+ str(f) +'_'+ str(g) +" complete")
								earliest_gen.append(min(temp_benchmark_gen))
								average_gen.append(mean(temp_benchmark_gen))
								average_gen2.append(mean(temp_benchmark_gen2))
								sigma_average_gen.append(stat.pstdev(temp_benchmark_gen))
								sigma_average_gen2.append(stat.pstdev(temp_benchmark_gen))




with open("Master_gen.csv", 'w') as f:
	f.write("Run Name, \t Earliest, \t Average (.5), \t Standard Deviation (.5), \t Average (.25), \t Standard Deviation (.25) \n")
	for x in range(0, len(run_name)):
		f.write(str(run_name[x]) + ", \t " + str(earliest_gen[x]) + ", \t " + str(average_gen[x]) + ", \t " + str(sigma_average_gen[x]) +", \t" +str(average_gen2[x]) + ", \t" + str(sigma_average_gen2[x]) + "\n")

f.close()
print( "Master_gen.csv written")
