# 12/18/2020
# by: Ryan T Debolt
"""Go through each file, gather and plot/save important information."""
import csv
import statistics as stat
from statistics import mean
import numpy as np

design = "ARA"
population = 100
generations = 50
error = "0.0"

count = 0
run_min_metric = []
earliest_gen = []
average_gen = []
sigma_average_gen = []
runtype = []
benchmark = 0.1


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
                    submetric.append(float(row[2]))
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
for rank in range(0, 101, 10):
    for roulette in range(0, 101, 10):
        for tournament in range(10, 101, 10):
            selections = rank + roulette + tournament
            if selections == population:
                for reproduction in range(4, 17, 4):
                    for crossover in range(72, 101, 4):
                        for mutation in range(8, 21, 4):
                            operators = crossover + reproduction + mutation
                            if operators <= population:
                                for sigma in range(10, 11, 1):
                                    runtype.append(f"{rank}_{roulette}_{tournament}_{reproduction}_{crossover}_{mutation}_{sigma}")

# For each runtype, test gather information
for run in range(len(runtype)):
    print(f"Analyzing: {runtype[run]}")
    min_metric = 1.0
    earliest = []
    for test in range(1, 11):
        runname = f"{runtype[run]}_{test}"
        min_gen = 50
        gen, metric = read_data(runname)
        for g in range(0, generations+1):
            if (min(metric[g]) < min_metric):
                min_metric = min(metric[g])
            if (min(metric[g]) <= benchmark and g <= min_gen):
                earliest.append(g)
    earliest_gen.append(min(earliest.copy()))
    average_gen.append(mean(earliest.copy()))
    sigma_average_gen.append(stat.pstdev(earliest.copy()))
    earliest.clear()

print("Creating Master File")
# Print data into master file
with open("Master_gen.csv", 'w') as f:
    f.write("Run Name, Earliest Generation, Average Generations, Standard Deviation , Minimum Metric \n")
    for x in range(0, len(runname)):
        f.write(f"{runtype[x]}, {earliest_gen[x]}, {average_gen[x]}, {sigma_average_gen[x]}, {min_metric[x]} \n")

f.close()
print("Master_gen.csv written")
