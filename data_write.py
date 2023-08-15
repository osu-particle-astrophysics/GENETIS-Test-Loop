"""Collect and write all data into a single file."""
# Imports
import csv
import argparse

# Functions


def read_dna(sections, genes, dna, filename):
    """Read in antenna dna."""
    with open(filename) as data:
        csv_read = csv.reader(data, delimiter=',')
        individual = 0
        for i, row in enumerate(csv_read):
            if i > 8:
                if (i-9) % sections == 0:
                    j = 0
                elif (i-9) % sections != 0:
                    j = (i-9) % sections
                for k in range(genes):
                    dna[individual][j][k] = float(row[k])
                if j == (i-9) % sections and (i-9) % sections != 0:
                    individual = individual + 1
                if sections == 1:
                    individual = individual + 1


def read_fitness(fitness, error, filename):
    """Read in fitness scores."""
    with open(filename) as f1:
        csv_read = csv.reader(f1, delimiter=',')
        for i, row in enumerate(csv_read):
            if i > 1:
                fitness.append(float(row[0]))
                error.append(float(row[1]))


def read_metric(metric, filename):
    """Read in metric scores."""
    with open(filename) as f1:
        csv_read = csv.reader(f1, delimiter=',')
        for i, row in enumerate(csv_read):
            if i > 1:
                metric.append(float(row[0]))


def read_parents(gen, pop, individual, parent1, parent2, opperator, seed):
    """Read in parents, seed, and opperators."""
    if gen == 0:
        for i in range(pop):
            individual.append(i+1)
            parent1.append("NA")
            parent2.append("NA")
            opperator.append("NA")
    else:
        with open("parents.csv") as f1:
            csv_read = csv.reader(f1, delimiter=',')
            for i, row in enumerate(csv_read):
                if i == 1:
                    seed = str(row[0])
                elif i > 4:
                    individual.append(row[0])
                    parent1.append(row[1])
                    parent2.append(row[2])
                    opperator.append(row[3])


# Read in arguement
parser = argparse.ArgumentParser()
parser.add_argument("design", type=str)
parser.add_argument("generation", type=int)
parser.add_argument("population", type=int)
g = parser.parse_args()

# Data lists and variables
seed = ''
individual = []
parent1 = []
parent2 = []
opperator = []
fitness = []
error = []
metric = []

# Find DNA vector parameters based on design
if g.design == "ARA":
    sections = 2
    genes = 4

elif g.design == "AREA":
    sections = 2
    genes = 14

elif g.design == "PUEO":
    sections = 1
    genes = 7

# Define list to hold dna
dna = [[[0]*genes for i in range(sections)] for j in range(g.population+1)]

# read in parents
read_parents(g.generation, g.population, individual,
             parent1, parent2, opperator, seed)

# Read in Chi score
filename = "metric.csv"
read_metric(metric, filename)

# Read in fitness score and error
filename = "fitnessScores.csv"
read_fitness(fitness, error, filename)

# Read in DNA
filename = "generationDNA.csv"
read_dna(sections, genes, dna, filename)

# Write Data into file
with open('generationData.csv', "w") as f5:
    # Write out the header
    f5.write(f"Generation Data for generation {g.generation}\n")
    f5.write(f"{seed}\n")
    f5.write('\n')
    f5.write("Individual, Metric, Fitness, Error, Parent 1, Parent 2,")
    f5.write(" Opperator")
    for x in range(sections*genes):
        f5.write(f", Gene {x+1}")
    f5.write('\n')

    # Write data
    for i in range(len(individual)):
        f5.write(f"{individual[i]}, {metric[i]}, {fitness[i]}, {error[i]}, "
                 f"{parent1[i]}, {parent2[i]}, {opperator[i]}, ")
        dnas = (dna[i][j][k] for j in range(sections) for k in range(genes))
        f5.write(', '.join(map(str, dnas)))
        f5.write("\n")
