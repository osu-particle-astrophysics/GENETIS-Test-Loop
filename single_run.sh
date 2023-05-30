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
design="PUEO"
generations=50
population=1000
rank=600
roulette=200
tournament=200
reproduction=0
crossover=960
mutation_rate=25
sigma=6
test=3

# establish run name
runname=${rank}'_'${roulette}'_'${tournament}'_'${reproduction}'_'${crossover}'_'${mutation_rate}'_'${sigma}'_'${test}

# loop over generations
for g in `seq 0 ${generations}`
do
    if [ $g -eq 0 ]
    then
        echo ${runname} 'Generation 0'
        
	# Call GA
        ./GA.exe ${design} ${g} ${population} ${rank} ${roulette} ${tournament} ${reproduction} ${crossover} ${mutation_rate} ${sigma}
        echo 'GA ran for gen 0'
    fi
    
    # Run GA for non-zero generations
    if [ $g -ne 0 ]
    then
        echo ${runname} 'Generation' ${g}
	#Call GA
        ./GA.exe ${design} ${g} ${population} ${rank} ${roulette} ${tournament} ${reproduction} ${crossover} ${mutation_rate} ${sigma}
        echo 'GA ran for gen' ${g}
    fi
    
    # Call script to calculate test loop fitness
    python test_fitness.py $design $g $population 
    
    # Check to see if there are duplicate antennas
    if [ $g -ne 0 ]
    then
        python fitness_check.py $design $g $population
    fi

    # Combine all datafiles into one file
    python data_write.py $design $g $population
    
    # Copy Combined file to permanent directory
    cp generationData.csv $RunPath/${runname}'_'${g}_generationData.csv
    
    # Make copies of fitnessScores, generationDNA, and generationData to be used later
    cp generationData.csv ${g}_generationData.csv
    cp fitnessScores.csv ${g}_fitnessScores.csv
    cp generationDNA.csv ${g}_generationDNA.csv
    
    # Show Status
    echo waiting...
    echo waiting...
    echo waiting...
    echo waiting...
done

# Call plotting scripts
#Save plots in plot directory with unique names
python test_plotter.py $design $generations $population

# move plot to the permanent directory
mv fitness.png $PlotsPath/${runname}_fitness.png
mv chisquared.png $PlotsPath/${runname}_chisquared.png
