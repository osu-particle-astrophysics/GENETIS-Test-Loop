# Purpose: This script writes the fitness score for the test loop optimization in place of the Veff value in the child_{}.txt files for the individuals in an AREA generation

# Author: Bryan Reynolds (reynolds.886@osu.edu)

# Created: February 2023
# Last Edit: March 1, 2023

# Usage:
# python getFS_testLoop.py -i $gen $NPop $NSeeds $source_dir

import os
import argparse
import csv
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='Input values', nargs='+', required=True)

args = parser.parse_args()

#bash input for gen number
gen=args.input[0]

#bash input for number of individuals
individuals=int(args.input[1])

# bash input for number of jobs per individual (seeds)
# DO WE NEED THIS FOR TEST LOOP?
jobs=int(args.input[2])

# bash input for directory for the run
source=args.input[3]

#get list of test loop fitness scores for each individual from csv
#BRYAN NOTE: might need to change this filepath depending on where the csv is
fs_list = []
#with open(str(source) + "/gen" + str(gen) + "_testLoopData.csv") as f:
with open(str(source) + "/gen" + str(gen) + "_Scores.csv") as f:
        csv_read = csv.reader(f, delimiter = ',')
        for i,row in enumerate(csv_read):
                if i > 0:
                        fs_list.append(float(row[1]))
        f.close()

#sanity check:
#print(fs_list)

#Check that a fitness score has been read for each individual:
if len(fs_list) != int(individuals):
        print("ERROR: number of rows in test loop fitness score does not equal the stated number of individuals in the run!")

#Create new text with test loop fitness scores for each child_*.txt files
for ind in range(0, individuals):
        #f_childIn = open(source + "/" + "gen_{}".format(gen) + "/child_{}.txt".format(ind), 'rt')
        f_childIn = open(source + "/child_{}.txt".format(ind), 'rt')
        childData = f_childIn.readlines()
        for i,line in enumerate(childData):
                if "test Veff :" in line:
                        childData[i] = "test Veff : " + str(fs_list[ind]) + "\n"
                        print("writing this to child_" + str(ind) + ": " + str(childData[i]))
        f_childIn.close()
        
        #write new child file with test loop fitness score inserted
        #f_childOut = open(source + "/" + "gen_{}".format(gen) + "/child_{}.txt".format(ind), 'wt')
        f_childOut = open(source + "/child_{}.txt".format(ind), 'wt')
        for line in childData:
                if line.strip("\n") != " MHz":
                        f_childOut.write(line)
        #f_childOut.writelines(childData)
        f_childOut.close()

print("getFS_testLoop.py complete: wrote test loop fitness scores in place of Veff") 
