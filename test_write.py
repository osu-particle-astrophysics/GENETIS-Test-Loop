"""Merge generationData.csv files into single file."""

# Imports
import csv
import argparse


# Functions
def read_data(generation):
    """Read and return data from file."""
    data = []
    with open(f'{generation}_generationData.csv', 'r') as file:
        csv_read = csv.reader(file, delimiter=',')
        for i, row in enumerate(csv_read):
            if 3 > 0:
                data.append(file.readline())
    return data


# Main
# Read in arguments
parser = argparse.ArgumentParser()
parser.add_argument("generations", type=int)
arg = parser.parse_args()

# Read data from generationData.csv into lines array
lines = []
for gen in range(0, arg.generations+1):
    lines.append(read_data(gen))

# Print data to file
with open('testData.csv', "w") as file:
    # Write out the header
    file.write("Test Data for \n")
    file.write("Individual, Metric, Fitness, Error, Parent 1, Parent 2,")
    file.write(" Opperator")
    for gen in range(0, arg.generations+1):
        file.write(f'{lines[gen]}')
