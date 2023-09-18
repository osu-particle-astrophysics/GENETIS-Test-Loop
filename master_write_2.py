# 12/18/2020
# by: Ryan T Debolt
"""Go through each file, gather and plot/save important information."""
import csv
import statistics as stat
from statistics import mean
import numpy as np

design = "ARA"
population = 50
generations = 100
error = "0.0"

count = 0
run_min_metric = []
earliest_gen = []
average_gen = []
sigma_average_gen = []
runtype = []
runtype_name = []
runtype_list = []
benchmark = 0.05


def read_data(runname):
    """Read in data from csv."""
    # Set arrays
    gen = []
    metric = []
    subgen = []
    submetric = []

    # Open files
    with open(f"{runname}_testData.csv") as file:
        csv_read = csv.reader(file, delimiter=',')
        for i, row in enumerate(csv_read):
            if i > 1:
                if (len(subgen) < population):
                    subgen.append(float(row[0]))
                    submetric.append(float(row[3]))
                if (len(subgen) == population):
                    gen.append(subgen.copy())
                    subgen.clear()
                    metric.append(submetric.copy())
                    submetric.clear()
    return gen, metric


# MAIN

print("Starting")

print("Gathering Run Names")
# Make list of runnames
for rank in range(0, 51, 5):
    for roulette in range(0, 51, 5):
        for tournament in range(0, 51, 5):
            selections = rank + roulette + tournament
            if selections == population:
                for reproduction in range(2, 9, 2):
                    for crossover in range(36, 45, 4):
                        for mutation in range(4, 11, 2):
                            operators = crossover + reproduction + mutation
                            if operators <= population:
                                injection = population - operators
                                for sigma in range(10, 11, 1):
                                    for test in range(1, 11):
                                        runtype.append(f"{rank}_{roulette}_{tournament}_{reproduction}_{crossover}_{mutation}_{sigma}_{test}")
                                        runtype_name.append(f"{rank}_{roulette}_{tournament}_{reproduction}_{crossover}_{mutation}_{injection}_{test}")
                                        runtype_list.append(f"{rank}, {roulette}, {tournament}, {reproduction}, {crossover}, {mutation}, {injection}, {test}")

# For each runtype, test gather information
for run in range(len(runtype)):
    print(f"Analyzing: {runtype[run]}")
    min_metric = 1.0
    earliest = 100
    runname = f"{runtype[run]}"
    min_gen = 100
    gen, metric = read_data(runname)
    for g in range(0, generations+1):
        if (min(metric[g]) < min_metric):
            min_metric = min(metric[g])
        if (min(metric[g]) <= benchmark and g <= min_gen):
            earliest = g
            min_gen = g
    run_min_metric.append(min_metric)
    earliest_gen.append(earliest)

print("Creating Master Files")
# Print data into master file
with open("Master_full.csv", 'w') as f:
    f.write("Run Type, Rank, Roulette, Tournament, Reproduction, Crossover, Mutation, Injection, Earliest Generation, Average Generations, Standard Deviation , Minimum Metric \n")
    for x in range(0, len(runtype)):
        f.write(f"{runtype_name[x]}, {runtype_list[x]}, {earliest_gen[x]}, {run_min_metric[x]} \n")

f.close()
print("Master_gen.csv written")