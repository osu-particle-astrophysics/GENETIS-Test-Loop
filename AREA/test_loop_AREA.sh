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
# $1 = roulette cross-over
# $2 = roulette mutation
# $3 = tournament cross-over
# $4 = tournament mutation
# $5 = number of generations to run
# $6 = index number of the starting generation for the run, 0 for a new run

# To submit a job:
# sbatch --export=ALL,A=10,B=10,C=10,D=10,E=5,F=0 GA_Controller_job.sh

# Permissions variable
USER=$breynolds

# Variable for run name
RunName='Runs/testSeparateGainWritingv10_21March2023'

# Path variables
GAPATH='/users/PAS1960/breynolds/work/GENETIS-Test-Loop/AREA/GA'
MAINPATH='/users/PAS1960/breynolds/work/GENETIS-Test-Loop/AREA'

A=$1
B=$2
C=$3
D=$4
E=$5
F=$6

# Read input GA parameters
let NPOP=$(($A+$B+$C+$D))
#let NPOP=$(($1+$2+$3+$4))
let TOT=$NPOP-1
GEN_CNT=$F
#GEN_CNT=$6
GEN_TOT=$E
#GEN_TOT=$5
let GEN_START=$GEN_CNT
SEEDS=1 #Number of parallel jobs, NOT CURRENTLY ENABLED

# Remove any remnants of stalled jobs (if applicable)
rm -r $GAPATH/$RunName/gen_$GEN_CNT/*
rm -r $GAPATH/$RunName/Flag_Files/*

# Compile AREA GA
cd $GAPATH
# g++ -std=c++11 ara_GA_noLinearDep_testDec2022.cc #BRYAN: check name
g++ -std=c++11 ara_GA_noLinearDep_speedUpGainWritingTest_15March2023.cc
cd $MAINPATH

# exporting this makes it a variable any bash script can see
export TOT=$TOT
export GEN_CNT=$GEN_CNT

#loop over generations
#for g in {$GEN_START..$GEN_TOT}
for g in $(seq $GEN_START $GEN_TOT)
do
    echo g is $g
    # If initial generation, create and test initial population
    if [ $g -eq 0 ]
    then
	
	echo 'Generation 0- will add argument info later'
	
	# Create file structure for GA outputs
	cd $GAPATH
	mkdir -m775 ./Runs
	mkdir -m775 ./$RunName
	cd $RunName
	# Create generation error and output files
	mkdir -m775 output
	mkdir -m775 error
	# Make new directory for gen 0
	mkdir -m775 ./gen_$g

	# Run GA for gen 0
	cd $GAPATH
	echo 'Running GA for gen 0...'
	./a.out -gp $A $B $C $D -p 0
	echo 'GA ran for gen 0'

    fi

    # Run GA for non-zero generations
    if [ $g -ne 0 ]
    then
	echo Beginning generation $g - will add argument info later
	
	# Define variable to track previous gen
	let LAST_CNT=$g-1
	
	# Make directory for new gen
	cd $GAPATH/$RunName
	mkdir -m775 ./gen_$g
	echo made directory for gen_$g
	
	# Call GA for generation G with genes from last gen as parents
	cd $GAPATH
	echo running GA for gen_$g ...
	echo inputs from previous gen are: ./$RunName/gen_$LAST_CNT/child*
	./a.out -gp $A $B $C $D -p $NPOP ./$RunName/gen_$LAST_CNT/child*
	echo ran GA for gen_$g

    fi

    # Move individuals to current gen folder
    mv child_* $GAPATH/$RunName/gen_$g
    #cd $RunName

    # Call script to get results from AREA GA output
    # Will make summary csv of each individual's genes in the generation
    # and save them to results_gen{g}.csv in the RunName directory
    cd $MAINPATH
    python makeResultsCSV_singleGenSummary.py -i $g $NPOP $GAPATH/$RunName

    # Call script to calculate test loop fitness
    # Will take in results_gen{g}.csv and calculate test loop Chi2 and fitness
    # and save them to gen{g}_testLoopData.csv
    python test_fitness_chi.py $g $NPOP $GAPATH/$RunName
    
    # Call script to write test loop fitness scores to individual's .txts
    # Reads gen{g}_testLoopData.csv and replaces Veff values in GA outputs with
    # test loop fitness scores
    python getFS_testLoop.py -i $g $NPOP $SEEDS $GAPATH/$RunName
    
    # Clean up excess files (delete individual's .txts when done)
    # remove gens from two generations prior
#    if [ $g -gt 1 ]
#    then
#	let CLEAN_GEN=$g-2
#	rm -r $GAPATH/$RunName/gen_$CLEAN_GEN/
#	echo Removed Gen_$CLEAN_GEN directory
#    fi
    
    # Update gen count variable
    let GEN_CNT=$g
    export GEN_CNT=$GEN_CNT

    #save copies of files created into storage directory (possibly condense)
    
    #may need to add wait functions here
    #sleep 10
done

# Call plotting scripts
# Save plots in plot directory with unique names
python AREA_Plotter.py $NPOP $GEN_CNT $GAPATH/$RunName

#for g in `seq 0 ${Generations}`
#do
    #remove excess files
#done
