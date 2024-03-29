"""Plot the individuals at each generation."""

# Imports
import matplotlib.pyplot as plt
import csv
import argparse
from statistics import mean

# Functions


def read_data(metric_scores, fitness_scores, filename):
    """Read in all scores for current gen."""
    with open(filename) as f:
        csv_read = csv.reader(f, delimiter=',')
        for i, row in enumerate(csv_read):
            if i > 3:
                fitness_scores.append(float(row[2]))
                metric_scores.append(float(row[1]))


# Read in arguments
parser = argparse.ArgumentParser()
parser.add_argument("design", type=str)
parser.add_argument("generation", type=int)
parser.add_argument("population", type=int)
g = parser.parse_args()

# Initialize storage vectors
generations = []
fitness_scores = []
max_fitness = []
ave_fitness = []
metric_scores = []
max_metric = []
min_metric = []
ave_metric = []


# Plot each individuals fitness for each generation
plt.figure(figsize=(16, 9))
for z in range(0, g.generation+1):

    # Read in all scores for current gen
    filename = f"{z}_generationData.csv"
    read_data(metric_scores, fitness_scores, filename)

    # Calculate maxe, and average of fitness
    max_fitness.append(max(fitness_scores))
    ave_fitness.append(mean(fitness_scores))

    # populate generation vector for plotting
    generations = [z for f in range(0, g.population)]

    # begin plotting
    plt.title(g.design + ' Fitness Evolution test')
    plt.plot(generations, fitness_scores, '.',
             color='black', markersize='3.0', alpha=.5)
    plt.ylabel('Fitness Scores')
    plt.xlabel('Generations')
    plt.axis([0, g.generation, 0, 1+.5*max(max_fitness)])
    plt.grid(visible=True, which='major',
             color='#666666', linestyle='-', linewidth=0.5)
    plt.minorticks_on()
    plt.grid(visible=True, which='minor',
             color='#999999', linestyle='-', linewidth=0.2, alpha=0.5)
    generations.clear()
    fitness_scores.clear()
    metric_scores.clear()

# plot max and Ave lines
generations = [f for f in range(0, g.generation+1)]
plt.plot(generations, max_fitness, linestyle='-', color='blue', alpha=0.5)
plt.plot(generations, ave_fitness, linestyle='--', color='red', alpha=0.5)
plt.savefig("fitness.png")


# Plot each individuals chi-squared value for each generation
plt.figure(figsize=(16, 9))
for z in range(0, g.generation+1):

    # Read in all scores for current gen
    filename = f"{z}_generationData.csv"
    read_data(metric_scores, fitness_scores, filename)

    # Calculate min and average of chi
    min_metric.append(min(metric_scores))
    ave_metric.append(mean(metric_scores))

    # populate generation vector for plotting
    generations = [z for f in range(0, g.population)]

    # begin plotting
    plt.title(g.design + ' Metric Evolution test')
    plt.plot(generations, metric_scores, '.',
             color='black', markersize='3.0', alpha=.5)
    plt.ylabel('Metric')
    plt.xlabel('Generations')
    # plt.axis([0, g.generation, 0, 1])
    plt.grid(visible=True, which='major',
             color='#666666', linestyle='-', linewidth=0.5)
    plt.minorticks_on()
    plt.grid(visible=True, which='minor',
             color='#999999', linestyle='-', linewidth=0.2, alpha=0.5)

    generations.clear()
    fitness_scores.clear()
    metric_scores.clear()

# plot min and Ave lines
generations = [f for f in range(0, g.generation+1)]
plt.plot(generations, min_metric, linestyle='-', color='blue', alpha=0.5)
plt.plot(generations, ave_metric, linestyle='--', color='red', alpha=0.5)
plt.savefig("metric.png")

# Display final generation thresholds
fitness_scores2 = []
metric_scores2 = []
with open("generationData.csv") as f2:
    txt_read = csv.reader(f2, delimiter=',')
    for i, row in enumerate(txt_read):
        if i > 3:
            metric_scores2.append(float(row[1]))
            fitness_scores2.append(float(row[2]))
print(f"Max Fitness Score: {max(fitness_scores2)}")
print(f"Min metric value: {min(metric_scores2)}")
