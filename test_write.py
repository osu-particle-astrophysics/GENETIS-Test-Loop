"""Merge generationData.csv files into single file."""

# Imports
import csv
import argparse


# Functions
def read_data(generation, runname):
    """Read and return data from file."""
    data = []
    with open(f'{runname}_{generation}_generationData.csv', 'r') as file:
        file_lines = file.readlines()[4:]
        csv_read = csv.reader(file, delimiter=':')
        for i, row in enumerate(csv_read):
            print(i)
            if i == 1:
                seed = str(row[1])
                print("look here!")

    for line in file_lines:
        data.append(line)
    return data, seed


# Main
print("Writting testData")
# Read in arguments
parser = argparse.ArgumentParser()
parser.add_argument("design", type=str)
parser.add_argument("generations", type=int)
parser.add_argument("population", type=int)
parser.add_argument("runname", type=str)
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
seeds = []
for gen in range(0, arg.generations+1):
    data, seed = read_data(gen, arg.runname)
    lines.append(data.copy)
    seeds.append(seed)
    data.clear()


# Print data to file
with open(f'{arg.runname}_testData.csv', "w") as file:
    # Write out the header
    file.write("Test Data for \n")
    file.write("Generation, Seed, Individual, Metric, Fitness, Error, Parent 1,")
    file.write(" Parent 2, Opperator")
    for x in range(sections*genes):
        file.write(f", Gene {x+1}")
    file.write('\n')
    for gen in range(0, arg.generations+1):
        for pop in range(0, arg.population):
            file.write(f'{gen}, {seeds[gen]}, {lines[gen][pop]}')

print("testData Written")
