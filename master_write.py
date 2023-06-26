# 12/18/2020
# by: Ryan T Debolt
"""Go through each file, gather and plot/save important information."""
import csv
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import matplotlib.colors as mcolors
from cycler import cycler
import statistics as stat
from statistics import mean
import numpy as np

design = "ARA"
population = 100
error = "0.25"

count = 0
earliest_gen = []
average_gen = []
average_gen2 = []
sigma_average_gen = []
sigma_average_gen2 = []
run_name = []
bench_mark = 0.1
bench_mark2 = 0.05

for rank in range(60, 61, 1):
    for roulette in range(20, 21, 1):
        for tournament in range(20, 21, 1):
            selections = rank + roulette + tournament
            if selections == population:
                for reproduction in range(12, 13, 4):
                    for crossover in range(72, 73, 4):
                        for mutation in range(4, 5, 4):
                            operators = crossover + reproduction + mutation
                            if operators <= population:
                                for sigma in range(5, 6, 5):
                                    count = count+1
                                    color = iter(cm.rainbow(np.linspace(0, 1, 11)))
                                    temp_benchmark_gen = []
                                    temp_benchmark_gen2 = []
                                    run_name.append(f"{rank}_{roulette}_{tournament}_{reproduction}_{crossover}_{mutation}_{sigma}")
                                    for test in range(1, 101):
                                        temp_earliest = 50
                                        temp_earliest2 = 50
                                        c = 'blue' #next(color)
                                        ave_fitness = []
                                        max_fitness = []
                                        ave_metric = []
                                        min_metric = []
                                        gen_num = []
                                        for generation in range(0, 51, 1):
                                            gen_num.append(generation)
                                        for gens in range(0, 51):
                                            runname = f"{rank}_{roulette}_{tournament}_{reproduction}_{crossover}_{mutation}_{sigma}_{test}_{gens}"
                                            fit = []
                                            metric = []
                                            with open(f"{runname}_generationData.csv") as F1:
                                                txt_read = csv.reader(F1, delimiter=",")
                                                for i, row in enumerate(txt_read):
                                                    if i > 3:
                                                        fit.append(float(row[2]))
                                                        metric.append(float(row[1]))
                                            ave_fitness.append(mean(fit))
                                            max_fitness.append(max(fit))
                                            ave_metric.append(mean(metric))
                                            min_metric.append(min(metric))

                                            # Now update temp_earliest
                                            if min(metric) <= bench_mark and gens < temp_earliest:
                                                temp_earliest = gens
                                            if min(metric) <= bench_mark2 and gens < temp_earliest2:
                                                temp_earliest2 = gens
                                        temp_benchmark_gen.append(temp_earliest)
                                        temp_benchmark_gen2.append(temp_earliest2)

                                        # Begin Plotting
                                        plt.figure(count, figsize=(16,9))
                                        plt.plot(gen_num, ave_metric, c=c, linestyle='dotted', label=(f"Run {test} average"), alpha=0.1)
                                        plt.plot(gen_num, min_metric, c=c, linestyle='solid', label=(f"Run {test} High"), alpha=0.1)
                                        # plt.axis([0,50, 0.00, 1.5])
                                        plt.grid(visible=True, which='major', color='#666666', linestyle='-', linewidth=0.5)
                                        plt.minorticks_on()
                                        plt.grid(visible=True, which='minor', color='#999999', linestyle='-', linewidth=0.2, alpha=0.5)
                                        plt.ylabel('Fitness Score')
                                        plt.xlabel('Generations')
                                        plt.suptitle(f"{design} Population: {population} Error: {error}")
                                        plt.savefig(f"plot_{design}_{error}_{rank}_{roulette}_{tournament}_{reproduction}_{crossover}_{mutation}_{sigma}.png")
                                    plt.close()
                                    print(f"plot_{design}_{error}_{rank}_{roulette}_{tournament}_{reproduction}_{crossover}_{mutation}_{sigma}.png written")
                                    earliest_gen.append(min(temp_benchmark_gen))
                                    average_gen.append(mean(temp_benchmark_gen))
                                    average_gen2.append(mean(temp_benchmark_gen2))
                                    sigma_average_gen.append(stat.pstdev(temp_benchmark_gen))
                                    sigma_average_gen2.append(stat.pstdev(temp_benchmark_gen2))


with open("Master_gen.csv", 'w') as f:
    f.write("Run Name, \t Earliest, \t Average (.5), \t Standard Deviation (.5), \t Average (.25), \t Standard Deviation (.25) \n")
    for x in range(0, len(run_name)):
        f.write(f"{run_name[x]}, {earliest_gen[x]}, {average_gen[x]}, {sigma_average_gen[x]}, {average_gen2[x]}, {sigma_average_gen2[x]}\n")

f.close()
print("Master_gen.csv written")
