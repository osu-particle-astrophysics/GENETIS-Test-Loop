########################################################################
#Reads fitness scores and genetic information for each individual from txt files
#and writes it to CSV files (one in each gen's directory)
#Intended to be called in job submission bash script

#Usage:
#python makeResultsCSV_singleGenSummary.py -i <generation number> <number of individuals> <path to run's directory>

#Author: Bryan Reynolds (reynolds.886@osu.edu)
#Last Modified: January 30, 2023
########################################################################

import os
import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='Input values', nargs='+', required=True)

args = parser.parse_args()

#bash input for gen count
gen=args.input[0]

#bash input for number of individuals
individuals=int(args.input[1])

# bash input for directory for run 
source=args.input[2]

#dataframes to hold results summaries
results_gen = pd.DataFrame(columns=['gen', 'indiv', 'fitness', 'c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11', 'c12', 'c13'])

#loop over each generation
#for gen in range(int(gens)):
print("Reading results from Gen " + str(gen) + " and compiling summary CSV...")
#loop over each individual
for indiv in range(individuals):
    f_indiv_in = open(source + "/gen_{}".format(str(gen)) + "/child_{}.txt".format(str(indiv)), 'rt')
    indiv_data = f_indiv_in.readlines()
    for i,line in enumerate(indiv_data):
        if "test Veff :" in line:
            fit = float(indiv_data[i].split()[3])
            #print(fit)
        if "Gain Coefficients" in line:
            coeffs = indiv_data[i+2].split(",")
            #print(coeffs)
        
    #write individual info to new line in dataframe
    indiv_info = [gen, indiv, fit, coeffs[0], coeffs[1], coeffs[2], coeffs[3], coeffs[4], coeffs[5], coeffs[6], coeffs[7], coeffs[8], coeffs[9], coeffs[10], coeffs[11], coeffs[12], coeffs[13].strip()]
    results_gen.loc[len(results_gen)] = indiv_info
    #results_overall.loc[len(results_overall)] = indiv_info

    f_indiv_in.close()

results_gen.to_csv(source + "/results_gen{}.csv".format(str(gen)), index=False)

#results_overall.to_csv(source + "/results_fullRun.csv", index=False)

print("Done! Results written to CSV")
