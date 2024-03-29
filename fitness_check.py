"""Solve the weighted average of duplicated individuals."""
# Imports
import csv
import argparse


# Functions


def read_fitness(fitness, error, filename):
    """Read in fitness scores."""
    with open(filename) as f1:
        txt_read = csv.reader(f1, delimiter=',')
        for i, row in enumerate(txt_read):
            if i > 1:
                fitness.append(float(row[0]))
                error.append(float(row[1]))


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


def combine_scores(current_fitness, previous_fitness,
                   current_error, previous_error):
    """Combine scores of identical individuals in the previous generation."""
    matches = 0
    for i in range(len(current_fitness)):
        for j in range(len(previous_fitness)):
            if current_dna[i] == previous_dna[j]:
                matches = matches + 1
                current_weight = 1.0/(current_error[i]**2.0)
                previous_weight = 1.0/(previous_error[j]**2.0)
                current_fitness[i] = ((current_weight * current_fitness[i]
                                       + previous_weight * previous_fitness[j])
                                      / (current_weight + previous_weight))
                current_error[i] = (1.0 /
                                    ((current_weight + previous_weight)**(0.5))
                                    )
    print(matches, "Matches found")


def write_fitness(fitness, error):
    """Write fitnessScore.csv with data for the generation."""
    with open('fitnessScores.csv', "r") as fs:
        lines = fs.readlines()
    lines2 = []
    with open('fitnessScores.csv', "w") as f2:
        for x in range(len(fitness)+2):
            if x <= 1:
                lines2.append(lines[x])
            elif x > 1:
                lines2.append(f"{fitness[x-2]}, {error[x-2]}\n")
        f2.writelines(lines2)


# Read in arguments
parser = argparse.ArgumentParser()
parser.add_argument("design", type=str)
parser.add_argument("generation", type=int)
parser.add_argument("population", type=int)
g = parser.parse_args()

# fitness related arrays
current_fitness = []
previous_fitness = []
current_error = []
previous_error = []

# Set constants based on design
if (g.design == "ARA"):
    sections = 2
    genes = 4

elif (g.design == "AREA"):
    sections = 2
    genes = 14

elif (g.design == "PUEO"):
    sections = 1
    genes = 7

# Initialize DNA vectors
current_dna = [[[0]*genes for i in range(sections)]
               for j in range(g.population+1)]
previous_dna = [[[0]*genes for i in range(sections)]
                for j in range(g.population+1)]

# Gather fitness scores and error from current Gen
filename = "fitnessScores.csv"
read_fitness(current_fitness, current_error, filename)

# Gather fitness scores and error from previous Gen
filename = str(g.generation-1) + "_fitnessScores.csv"
read_fitness(previous_fitness, previous_error, filename)

# Read in values from current Gen DNA
filename = "generationDNA.csv"
read_dna(sections, genes, current_dna, filename)

# Read in values from previous gen DNA
filename = str(g.generation-1) + "_generationDNA.csv"
read_dna(sections, genes, previous_dna, filename)

# combine fitness scores of identical individuals in the previous generation
combine_scores(current_fitness, previous_fitness,
               current_error, previous_error)

# print updated scores into the csv
write_fitness(current_fitness, current_error)
