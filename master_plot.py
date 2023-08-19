"""Create a plot of runtype."""

# Imports
import csv
import argparse
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import matplotlib.colors as mcolors
from cycler import cycler
import statistics as stat
from statistics import mean
import numpy as np
import pandas as pd

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("params", type=str)
parser.add_argument("num_runs", type=int)
parser.add_argument("num_gens", type=int)
parser.add_argument("npop", type=int)
parser.add_argument("input_dir", type=str)
g = parser.parse_args()

# Define function to read in data and 
# create secondary csv with avg and min metric and fitness for each generation and run
def parse_data(param_string, num_runs, gens, npop, input_dir):
    '''Read in data from each run with given parameters 
    and create a csv with avg and min metric/fitness for each gen and run.'''

    # create data frame to hold data
    # stores run_num, gen, avg_metric, min_metric, avg_fitness, min_fitness
    df = pd.DataFrame(columns=['run_num', 'gen', 'avg_metric', 'min_metric', 'avg_fitness', 'min_fitness'])
    
    # Access data from each run
    for i_run in range(1, num_runs+1):

        # Read in data from a run
        # Skip first row because it is a text header
        df_run = pd.read_csv(f"{input_dir}/{param_string}_{i_run}_testData.csv", skiprows=1)

        #print(df_run.head())

        # Drop columns that are non-numeric (Parent 1, Parent 2, Opperator)
        df_run = df_run.drop([' Parent 1', ' Parent 2', ' Opperator'], axis=1)

        # group data by generation and calculate avg and min metric and fitness
        df_avg = df_run.groupby('Generation').mean()
        df_min = df_run.groupby('Generation').min()

        # Concat data to data frame for each generation
        for i_gen in range(0, gens+1):

            df.loc[len(df.index)] = [int(i_run), int(i_gen), df_avg[' Metric'][i_gen], df_min[' Metric'][i_gen], df_avg[' Fitness'][i_gen], df_min[' Fitness'][i_gen]]

            #df_temp = {'run_num': i_run, 
            #                'gen': i_gen, 
            #                'avg_metric': df_avg[' Metric'][i_gen], 
            #                'min_metric': df_min[' Metric'][i_gen], 
            #                'avg_fitness': df_avg[' Fitness'][i_gen], 
            #                'min_fitness': df_min[' Fitness'][i_gen]}
            #pd.concat([df, df_temp])

    # Return data frame
    return df

# Define function to populate 2-D list of avg and min metric for each run
def process_data(df_runs):
    '''Read in data frame of per generation avg, min metrics for each run.
    Returns list of lists containing avg and min scores, separated by run.'''

    # Initialize storage lists
    avg_metric = []
    min_metric = []

    # Get runs in dataset
    runs = df_runs['run_num'].unique()

    # Loop over runs
    for run in runs:
    
        # Get data for current run
        df_run = df_runs.loc[df_runs['run_num'] == run]

        # Get avg and min metric for current run as lists
        # and append to storage lists
        avg_metric.append(df_run['avg_metric'].tolist())
        min_metric.append(df_run['min_metric'].tolist())

    # Return lists
    return avg_metric, min_metric

# Define function to plot data
def plot_data(avg_metric, min_metric):
    '''Plot data from avg and min metric lists.'''

    # Define colors (need 10 for now) and line styles (solid for min, dashed for avg)
    colors = ['blue', 'red', 'green', 'orange', 'purple', 'pink', 'olive', 'cyan', 'brown', 'gray']
    line_style_min = 'solid'
    line_style_avg = 'dashed'

    # Begin plotting
    plt.figure(figsize=(16, 9))

    for i_run in range(0, len(avg_metric)):

        plt.plot(avg_metric[i_run], linestyle=line_style_avg, color=colors[i_run], alpha=0.6, label=f"Run {i_run+1}")
        plt.plot(min_metric[i_run], linestyle=line_style_min, color=colors[i_run], alpha=0.6, label=f"Run {i_run+1}")

    plt.title(g.params + ' Metric Versus Generation', fontsize=32)
    plt.ylabel('Metric', fontsize=32)
    plt.xlabel('Generation', fontsize=32)
    plt.axis([0, g.num_gens, 0, 1])
    plt.grid(visible=True, which='major', color='#666666', linestyle='-', linewidth=0.5)
    plt.minorticks_on()
    plt.tick_params(axis='both', which='major', labelsize=24)
    plt.grid(visible=True, which='minor', color='#999999', linestyle='-', linewidth=0.2, alpha=0.5)

    plt.savefig(f"{g.params}_fitness.png")

# Parse data
data = parse_data(g.params, g.num_runs, g.num_gens, g.npop, g.input_dir)

# Process data
avg_metric, min_metric = process_data(data)

# Plot data
plot_data(avg_metric, min_metric)

#print(data.head())
#print(avg_metric)
#print(len(avg_metric))

print("Plotting complete!")

# Write to csv for testing
data.to_csv('test_for_plotter.csv', index=False)