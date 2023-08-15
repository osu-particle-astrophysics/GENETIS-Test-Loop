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
FlagPath='/users/PAS0654/ryantdebolt/test_loop_build_directory/Flags'
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
mutation_no=${9}
sigma=${10}
test=${11}

# Establish run name
runname=${rank}'_'${roulette}'_'${tournament}'_'${reproduction}'_'${crossover}'_'${mutation_no}'_'${sigma}'_'${test}
echo $runname

# Move files to correct directory
cp test_write.py $TMPDIR
mv ${RunPath}/${runname}_*_generationData.csv $TMPDIR
cd $TMPDIR

# Condense test files
python test_write.py $design $generations $population $runname

# Remove corresponding files
rm ${runname}_*_generationData.csv

# Move file to permanent directory
mv ${runname}_testData.csv ${RunPath}

# Make Flag
cp test_write.py ${FlagPath}/${runname}_test_write.py
