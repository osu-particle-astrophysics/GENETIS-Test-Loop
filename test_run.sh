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

# Input arguments for this script are:
Design=${1}
Generations=${2}
Population=${3}
Rank=${4}
Roulette=${5}
Tournament=${6}
Reproduction=${7}
Crossover=${8}
MutationRate=${9}
Sigma=${10}
Test=${11}

# Move things to TMPDIR
cp GA/SourceFiles/GA.exe $TMPDIR
cp data_write.py $TMPDIR
cp test_fitness.py $TMPDIR
cp test_plotter.py $TMPDIR
cp fitness_check.py $TMPDIR
cd $TMPDIR

#loop over generations
for g in `seq 0 ${Generations}`
do
    if [ $g -eq 0 ]
    then
	
	echo ${Rank}'_'${Roulette}'_'${Tournament}'_'${Reproduction}'_'${Crossover}'_'${MutationRate}'_'${Sigma} 'Generation 0'
	
	#Call GA
	./GA.exe ${Design} ${g} ${Population} ${Rank} ${Roulette} ${Tournament} ${Reproduction} ${Crossover} ${MutationRate} ${Sigma}
	echo 'GA ran for gen 0'

    fi

    #Run GA for non-zero generations
    if [ $g -ne 0 ]
    then
	echo ${Rank}'_'${Roulette}'_'${Tournament}'_'${Reproduction}'_'${Crossover}'_'${MutationRate}'_'${Sigma} 'Generation' ${g}
	
	#Call GA
	./GA.exe ${Design} ${g} ${Population} ${Rank} ${Roulette} ${Tournament} ${Reproduction} ${Crossover} ${MutationRate} ${Sigma}
	echo 'GA ran for gen' ${g}

    fi

    #Call script to calculate test loop fitness
    python test_fitness.py $Design $g $Population 
    
    #Check to see if there are duplicate antennas
    python fitness_check.py $Design $g $Population
    
    #Combine all datafiles into one file
    python data_write.py $Design $g $Population
    
    # Copy Combined file to permanent directory
    cp generationData.csv /users/PAS0654/ryantdebolt/test_loop_build_directory/Run/${Rank}'_'${Roulette}'_'${Tournament}'_'${Reproduction}'_'${Crossover}'_'${MutationRate}'_'${Sigma}'_'${Test}'_'${g}_generationData.csv
    
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
python test_plotter.py $Design $Generations $Population 

#move plot to the permanent directory
mv fitness.png /users/PAS0654/ryantdebolt/test_loop_build_directory/Plots/${Rank}'_'${Roulette}'_'${Tournament}'_'${Reproduction}'_'${Crossover}'_'${MutationRate}'_'${Sigma}'_'${Test}_fitness.png
mv chisquared.png /users/PAS0654/ryantdebolt/test_loop_build_directory/Plots/${Rank}'_'${Roulette}'_'${Tournament}'_'${Reproduction}'_'${Crossover}'_'${MutationRate}'_'${Sigma}'_'${Test}_chisquared.png

