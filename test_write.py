"""Merge generationData.csv files into single file."""

# Imports
import csv
import argparse


# Functions
def read_data(generation):
    """Read and return data from file."""
    data = []
    with open(f'{generation}_generationData.csv', 'r') as file:
        file_lines = file.readlines()

    for line in file_lines:
        if lines > 2:
            data.append(line)
    return data


# Main
# Read in arguments
parser = argparse.ArgumentParser()
parser.add_argument("design", type=str)
parser.add_argument("generations", type=int)
parser.add_argument("population", type=int)
arg = parser.parse_args()

# Find DNA vector parameters based on design
if arg.design == "ARA":
    sections = 2
    genes = 4

elif arg.design == "AREA":
    sections = 2
    genes = 14

elif arg.design == "PUEO":
    sections = 1
    genes = 7

# Read data from generationData.csv into lines array
lines = []
for gen in range(0, arg.generations+1):
    lines.append(read_data(gen))

print(len(lines))
print(len(lines[0]))

# Print data to file
with open('testData.csv', "w") as file:
    # Write out the header
    file.write("Test Data for \n")
    file.write("Individual, Metric, Fitness, Error, Parent 1, Parent 2,")
    file.write(" Opperator")
    for x in range(sections*genes):
        file.write(f", Gene {x+1}")
        file.write('\n')
    for gen in range(0, arg.generations+1):
        for pop in range(0, arg.population):
            file.write(f'{lines[gen][pop]}')
