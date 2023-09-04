#!/bin/bash

#############################
## Created by Ryan Debolt
## Created May 2023
## This is designed to run without submitting batch jobs to test single runs
## Manualy move all files needed for this run 
#############################

# set directories/paths
PlotsPath='/users/PAS0654/ryantdebolt/test_loop_build_directory/Plots'
RunPath='/users/PAS0654/ryantdebolt/test_loop_build_directory/Run'
GAPath='/users/PAS0654/ryantdebolt/test_loop_build_directory/GA/SourceFiles'

# Input arguments for this script are:
design="ARA"
generations=50
population=100
rank=50
roulette=20
tournament=30
reproduction=4
crossover=72
mutation_no=12
sigma=10
test=3

# establish run name
runname=${rank}'_'${roulette}'_'${tournament}'_'${reproduction}'_'${crossover}'_'${mutation_no}'_'${sigma}'_'${test}

# loop over generations
for g in `seq 0 ${generations}`
do
    if [ $g -eq 0 ]
    then
        echo ${runname} 'Generation 0'
        
	# Call GA
        ./GA.exe ${design} ${g} ${population} ${rank} ${roulette} ${tournament} ${reproduction} ${crossover} ${mutation_no} ${sigma}
        echo 'GA ran for gen 0'
    fi
    
    # Run GA for non-zero generations
    if [ $g -ne 0 ]
    then
        echo ${runname} 'Generation' ${g}
	#Call GA
        ./GA.exe ${design} ${g} ${population} ${rank} ${roulette} ${tournament} ${reproduction} ${crossover} ${mutation_no} ${sigma}
        echo 'GA ran for gen' ${g}
    fi
    
    # Call script to calculate test loop fitness
    python test_fitness.py $design $g $population 
    
    # Check to see if there are duplicate antennas
    if [ $g -ne 0 ]
    then
        echo no error
        # python fitness_check.py $design $g $population
    fi

    # Combine all datafiles into one file
    python data_write.py $design $g $population
    
    # Copy Combined file to permanent directory
    cp generationData.csv ${runname}'_'${g}_generationData.csv
    
    # Make copies of fitnessScores, generationDNA, and generationData to be used later
    cp generationData.csv ${g}_generationData.csv
    cp fitnessScores.csv ${g}_fitnessScores.csv
    cp generationDNA.csv ${g}_generationDNA.csv
    
    # Show Status
    echo waiting...
    echo waiting...
    echo waiting...
    echo waiting...
    sleep 0.25
done

# Call plotting scripts
python test_plotter.py $design $generations $population

# Condense data
python test_write.py $design $generations $population ${runname}

# move plot to the permanent directory
mv fitness.png $PlotsPath/${runname}_fitness.png
mv metric.png $PlotsPath/${runname}_metric.png

