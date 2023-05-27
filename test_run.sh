#!/bin/bash

#SBATCH -A PAS1960
#SBATCH -t 00:20:00
#SBATCH -N 1
#SBATCH -n 8
##SBATCH -o ~
##SBATCH -e ~
###PBS -o /users/PAS1960/breynolds/work/GENETIS-Test-Loop/AREA/termoutput/
###PBS -e /users/PAS1960/breynolds/work/GENETIS-Test-Loop/AREA/termoutput/

#############################
## Created by Ryan Debolt and Bryan Reynolds
## Created May 2023
#############################

# set directories/paths
PlotsPath='/users/PAS0654/ryantdebolt/test_loop_build_directory/Plots'
RunPath='/users/PAS0654/ryantdebolt/test_loop_build_directory/Run'
GAPath='/users/PAS0654/ryantdebolt/test_loop_build_directory/GA/SourceFiles'

# Input arguments for this script are:
design=${1}
generations=${2}
population=${3}
rank=${4}
roulette=${5}
tournament=${6}
reproduction=${7}
crossover=${8}
mutation_rate=${9}
sigma=${10}
test=${11}

# establish run name
runname=${rank}'_'${roulette}'_'${tournament}'_'${reproduction}'_'${crossover}'_'${mutation_rate}'_'${sigma}'_'${test}

# Move things to TMPDIR
cp $GAPath/GA.exe $TMPDIR
cp fitnessScores.csv $TMPDIR
cp chiScores.csv $TMPDIR
cp data_write.py $TMPDIR
cp test_fitness.py $TMPDIR
cp test_plotter.py $TMPDIR
cp fitness_check.py $TMPDIR
cd $TMPDIR

#loop over generations
for g in `seq 0 ${generations}`
do
    if [ $g -eq 0 ]
    then
	
	echo ${runname} 'Generation 0'
	
	#Call GA
	./GA.exe ${design} ${g} ${population} ${rank} ${roulette} ${tournament} ${reproduction} ${crossover} ${mutation_rate} ${sigma}
	echo 'GA ran for gen 0'

    fi

    #Run GA for non-zero generations
    if [ $g -ne 0 ]
    then
	echo ${runname} 'Generation' ${g}
	
	#Call GA
	./GA.exe ${design} ${g} ${population} ${rank} ${roulette} ${tournament} ${reproduction} ${crossover} ${mutation_rate} ${sigma}
	echo 'GA ran for gen' ${g}

    fi

    #Call script to calculate test loop fitness
    python test_fitness.py $design $g $population 
    if [ $g -ne 0 ]
    then
	#Check to see if there are duplicate antennas
	python fitness_check.py $design $g $population
    fi

    #Combine all datafiles into one file
    python data_write.py $design $g $population
    
    # Copy Combined file to permanent directory
    cp generationData.csv $RunPath/${runname}'_'${g}_generationData.csv
    
    # Make copies of fitnessScores, generationDNA, and generationData to be used later
    cp generationData.csv ${g}_generationData.csv
    cp fitnessScores.csv ${g}_fitnessScores.csv
    cp generationDNA.csv ${g}_generationDNA.csv
    
    
    #Show Status
    echo waiting...
    echo waiting...
    echo waiting...
    echo waiting...
done

#Call plotting scripts
#Save plots in plot directory with unique names
python test_plotter.py $design $generations $population 

#move plot to the permanent directory
mv fitness.png $PlotsPath/${runname}_fitness.png
mv chisquared.png $PlotsPath/${runname}_chisquared.png

