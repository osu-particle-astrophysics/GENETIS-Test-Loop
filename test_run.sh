#!/bin/bash

#SBATCH -A PAS1960
#SBATCH -t 72:00:00
#SBATCH -N 1
#SBATCH -n 8
##SBATCH -o ~
##SBATCH -e ~
###PBS -o /users/PAS1960/breynolds/work/GENETIS-Test-Loop/AREA/termoutput/
###PBS -e /users/PAS1960/breynolds/work/GENETIS-Test-Loop/AREA/termoutput/

#############################
## Created by Bryan Reynolds
## Created January 2023
## Last edit: Feb 8, 2023
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
Mutation_Rate=${9}
Sigma=${10}
echo ${Run_Number}

# Move things to TMPDIR
cp GA/SourceFiles/GA.exe $TMPDIR
cp test_fitness_chi.py $TMPDIR
cp AREA_plotter.py $TMPDIR
cp makeResultsCSV_singleGenSummary.py $TMPDIR
cp getFS_testLoop.py $TMPDIR
cd $TMPDIR

#loop over generations
for g in `seq 0 ${Generations}`
do
    if [ $g -eq 0 ]
    then
	
	echo ${Rank}'_'${Roulette}'_'${Tournament}'_'${Reproduction}'_'${Crossover}'_'${Mutation_Rate}'_'${Sigma} 'Generation 0'
	
	#Call GA
	./GA.exe ${Design) ${g} ${Population} ${Rank} ${Roulette} ${Tournament} ${Reproduction} ${Crossover} ${Mutation_Rate} ${Sigma}
	echo 'GA ran for gen 0'

    fi

    # Run GA for non-zero generations
    if [ $g -ne 0 ]
    then
	echo ${Rank}'_'${Roulette}'_'${Tournament}'_'${Reproduction}'_'${Crossover}'_'${Mutation_Rate}'_'${Sigma} 'Generation' ${g}
	
	#Call GA
	./GA.exe ${Design) ${g} ${Population} ${Rank} ${Roulette} ${Tournament} ${Reproduction} ${Crossover} ${Mutation_Rate} ${Sigma}
	echo 'GA ran for gen' ${g}

    fi

    # Call script to calculate test loop fitness
    python test_fitness_chi.py $Design $g $population 
    
    # Check to see if there are duplicate antennas
    python3 fitness_check.py $g
    
    # Combine all datafiles into one file
    python data_write.py ${Design} $g
    
    # Move Combined file to permanent directory
    # need to adjust nameing convention
    mv generationData.csv /users/PAS0654/ryantdebolt/test_loop_build_directory/Run/
    
    #Show Status
    echo waiting...
    echo waiting...
    echo waiting...
    echo waiting...
done

# Call plotting scripts
# Save plots in plot directory with unique names
python AREA_Plotter.py $population $Generations txts
mv fitness.png /users/PAS1960/breynolds/work/GENETIS-Test-Loop/AREA/Plots/${Roul_Cross}'_'${Roul_Mut}'_'${Tour_Cross}'_'${Tour_Mut}'_'${Run_Number}_fitness.png

