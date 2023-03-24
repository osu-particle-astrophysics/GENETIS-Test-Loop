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
population=${1}
Generations=${2}
Roul_Cross=${3}
Roul_Mut=${4}
Tour_Cross=${5}
Tour_Mut=${6}
Run_Number=${7}
echo ${Run_Number}

# Move things to TMPDIR
cp GA/a.out $TMPDIR
cp test_fitness_chi.py $TMPDIR
cp AREA_plotter.py $TMPDIR
cp makeResultsCSV_singleGenSummary.py $TMPDIR
cp getFS_testLoop.py $TMPDIR
cd $TMPDIR
mkdir txts

#loop over generations
for g in `seq 0 ${Generations}`
do
    if [ $g -eq 0 ]
    then
	
	echo ${Roul_Cross}'_'${Roul_Mut}'_'${Tour_Cross}'_'${Tour_Mut} 'Generation 0'
	./a.out -gp $Roul_Cross $Roul_Mut $Tour_Cross $Tour_Mut -p 0
	echo 'GA ran for gen 0'

    fi

    # Run GA for non-zero generations
    if [ $g -ne 0 ]
    then
	echo ${Roul_Cross}'_'${Roul_Mut}'_'${Tour_Cross}'_'${Tour_Mut} 'Generation' ${g}
	
	#Call GA
	./a.out -gp $Roul_Cross $Roul_Mut $Tour_Cross $Tour_Mut -p $population txts/child*
	echo 'GA ran for gen' ${g}

    fi

    # Call script to get results from AREA GA output
    python makeResultsCSV_singleGenSummary.py -i $g $population txts

    # Call script to calculate test loop fitness
    python test_fitness_chi.py $g $population txts
    
    # Call script to write test loop fitness scores to individual's .txts
    python getFS_testLoop.py -i $g $population 1 txts

    #save copies of files created into storage directory (change based on user)
    cp txts/gen${g}_Scores.csv /users/PAS1960/breynolds/work/GENETIS-Test-Loop/AREA/Results/${Roul_Cross}'_'${Roul_Mut}'_'${Tour_Cross}'_'${Tour_Mut}'_'${Run_Number}_Scores.csv
    
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

