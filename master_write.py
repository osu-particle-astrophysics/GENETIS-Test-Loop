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

design = "PUEO"
population = 50
error = "0.5"

count = 0
earliest_gen = []
average_gen = []
average_gen2 = []
sigma_average_gen = []
sigma_average_gen2 = []
run_name = []
bench_mark = 0.5
bench_mark2 = 0.25

for rank in range(30, 31, 1):
    for roulette in range(10, 11, 1):
        for tournament in range(10, 11, 1):
            if rank + roulette + tournament == population:
                for reproduction in range(2, 3, 1):
                    for crossover in range(46, 47, 2):
                        for mutation_rate in range(25, 26, 1):
                            for sigma in range(7, 8, 1):
                                count = count+1
                                color = iter(cm.rainbow(np.linspace(0, 1, 11)))
                                temp_benchmark_gen = []
                                temp_benchmark_gen2 = []
                                run_name.append(f"{rank}_{roulette}_{tournament}_{reproduction}_{crossover}_{mutation_rate}_{sigma}")
                                for test in range(1, 11):
                                    temp_earliest = 50
                                    temp_earliest2 = 50
                                    c = next(color)
                                    ave_fitness = []
                                    max_fitness = []
                                    ave_chi = []
                                    min_chi = []
                                    gen_num = []
                                    for generation in range(0, 51, 1):
                                        gen_num.append(generation)
                                    for gens in range(0, 51):
                                        runname=f"{rank}_{roulette}_{tournament}_{reproduction}_{crossover}_{mutation_rate}_{sigma}_{test}_{gens}"
                                        fit = []
                                        chi = []
                                        with open(f"{runname}_generationData.csv") as F1:
                                            txt_read = csv.reader(F1, delimiter=",")
                                            for i, row in enumerate(txt_read):
                                                if i > 3:
                                                    fit.append(float(row[2]))
                                                    chi.append(float(row[1]))
                                        ave_fitness.append(mean(fit))
                                        max_fitness.append(max(fit))
                                        ave_chi.append(mean(chi))
                                        min_chi.append(min(chi))

                                        # Now update temp_earliest
                                        if min(chi) <= bench_mark and gens < temp_earliest:
                                            temp_earliest = gens
                                        if min(chi) <= bench_mark2 and gens < temp_earliest2:
                                            temp_earliest2 = gens
                                    temp_benchmark_gen.append(temp_earliest)
                                    temp_benchmark_gen2.append(temp_earliest2)

                                    # Begin Plotting
                                    plt.figure(count, figsize=(16,9))
                                    plt.plot(gen_num, ave_chi, c=c, linestyle='dotted', label=(f"Run {test} average"))
                                    plt.plot(gen_num, min_chi, c=c, linestyle='solid', label=(f"Run {test} High"))
                                    # plt.axis([0,50, 0.00, 1.5])
                                    plt.grid(visible=True, which='major', color='#666666', linestyle='-', linewidth=0.5)
                                    plt.minorticks_on()
                                    plt.grid(visible=True, which='minor', color='#999999', linestyle='-', linewidth=0.2, alpha=0.5)
                                    plt.ylabel('Fitness Score')
                                    plt.xlabel('Generations')
                                    plt.suptitle(f"{design} Population: {population} Error: {error}")
                                    plt.savefig(f"plot_{design}_{error}_{rank}_{roulette}_{tournament}_{reproduction}_{crossover}_{mutation_rate}_{sigma}.png")
                                plt.close()
                                print(f"plot_{design}_{error}_{rank}_{roulette}_{tournament}_{reproduction}_{crossover}_{mutation_rate}_{sigma}.png written")
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
