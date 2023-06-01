""""Solve for fitness scores of individuals in a generation."""
# Imports
import csv
import argparse
import random
import math

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


def solve_chi_squared(target, observed, sections, genes, chi2):
    """Solve for Chi-squared scores."""
    for i in range(0, g.population):
        tempChi2 = 0
        for j in range(sections):
            for k in range(genes):
                tempChi2 = (tempChi2
                            + abs(((observed[i][j][k] - target[j][k])**2)
                            / target[j][k]))
        chi2.append(tempChi2)


def calc_error(fitness, error):
    """Calculate simulated error for the test."""
    for i in range(0, len(fitness)):
        if fitness[i] == 0:
            error.append(0.0)
        else:
            error.append(0.25/math.sqrt(2.0))
            tempFit = fitness[i]
            tempFit = random.gauss(fitness[i], 0.25/math.sqrt(2.0))
            while tempFit < 0:
                tempFit = random.gauss(fitness[i], 0.25/math.sqrt(2.0))
            fitness[i] = tempFit


def write_fitness(fitness, error):
    """Write fintessScore csv with data for the generation."""
    with open('fitnessScores.csv', "r") as fs:
        lines = fs.readlines()
    lines2 = []
    with open('fitnessScores.csv', "w") as f2:
        for x in range(0, len(fitness)+2):
            if x <= 1:
                lines2.append(f"{lines[x]}")
            elif x > 1:
                lines2.append(f"{fitness[x-2]}, {error[x-2]}\n")
        f2.writelines(lines2)


def write_chi(chi2):
    """Write chiScore csv with data for the generation."""
    with open('chiScores.csv', "r") as fc:
        lines = fc.readlines()
    lines3 = []
    with open('chiScores.csv', "w") as f2:
        for x in range(len(fitness)+2):
            if x <= 1:
                lines3.append(lines[x])
            elif x > 1:
                lines3.append(f"{chi2[x-2]}\n")
        f2.writelines(lines3)


######################################################
# MAIN CODE

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("design", type=str)
parser.add_argument("generation", type=int)
parser.add_argument("population", type=int)
g = parser.parse_args()

# Define target gain pattern based on design
if (g.design == "ARA"):
    target = [[0.968807, 14.1263, -0.053024, 0.8256],
              [4.83102, 10.4062, 0.027465, -0.396757]]
    sections = 2
    genes = 4

elif (g.design == "AREA"):
    target = [[2.82456, -0.029512, 0.0671632, -0.0681442,
              0.144533, -0.129438, 0.00934594, -0.0111579,
              -0.143811, 0.0307403, 0.0279309, 0.0676385, 0.0305001, -2.22847],
              [-1.46998, 2.94396, 3.07804, -3.72175,
              3.40754, -0.529288, 4.0295, 1.26466,
              3.03942, -4.53036, -3.74864, -0.543697, 1.08282, -3.25018]]
    sections = 2
    genes = 14

elif (g.design == "PUEO"):
    target = [[33.2056, 38.6897, 23.6239, 14.6074,
               30.1627, 32.4097, 1.70987]]
    sections = 1
    genes = 7

# Define list to hold each antennas observed gain pattern
observed = [[[0]*genes for i in range(sections)]
            for j in range(g.population+1)]

# Populate the observed list from csv
filename = "generationDNA.csv"
read_dna(sections, genes, observed, filename)

# Define lists to store scores
fitness = []
error = []
chi2 = []

# Calculate ChiSquared Scores
solve_chi_squared(target, observed, sections, genes, chi2)

# Translate Chi-Squared into fitness score
fitness = [(1/(x+1)) for x in chi2]

# Introduce error to fitness score
calc_error(fitness, error)

# Write csv's with data for the generation
write_fitness(fitness, error)
write_chi(chi2)

print(f"Max fitness: {max(fitness)}")
print(f"Min Chi-squared: {min(chi2)}")
