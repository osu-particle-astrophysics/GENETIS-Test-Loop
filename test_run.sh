#!/bin/bash
# Previously part of test_loop.sh 
# Transplanted here to run batch jobs in parallel
# Need to pass in arguements
# 
# This code takes in a run code and runs all the generations of a test run
# This includes the GA, fitness functions, plot making, and file management


# Variables (pass these in)
Population=${1}
Generations=${2}
Reproduction=${3}
Crossover=${4}
Mutation_Rate=${5}
Sigma=${6}
Roulette=${7}
Tournament=${8}
Rank=${9}
Elite=${10}
Run_Number=${11}

echo ${Run_Number}

# Start run
for g in `seq 0 ${Generations}` 
do
    if [ $g -eq 0 ]
    then
	echo ${Reproduction}'_'${Crossover}'_'${Mutation_Rate}'_'${Sigma}'_'${Roulette}'_'${Tournament}'_'${Rank}'_'${Run_Number} 'Generation 0'
	./a.out start $Population $Reproduction $Crossover $Mutation_Rate $Sigma $Roulette $Tournament $Rank $Elite
	python3 test_fitness_chi.py $g
	python3 test_chi.py $g
	cp ${g}_fitnessScores.csv fitnessScores.csv
	cp ${g}_chiScores.csv chiScores.csv
	cp generationDNA.csv ${g}_generationDNA.csv
	cp parents.csv ${g}_parents.csv
	python3 data_write.py ${g}
	mv ${g}_generationData.csv Run/${Reproduction}_${Crossover}_${Mutation_Rate}_${Sigma}_${Roulette}_${Tournament}_${Rank}_${Run_Number}_${g}_generationData.csv
    fi

    if [ $g -ne 0 ]
    then
        echo ${Reproduction}'_'${Crossover}'_'${Mutation_Rate}'_'${Sigma}'_'${Roulette}'_'${Tournament}'_'${Rank}'_'${Run_Number} 'Generation' ${g}
        ./a.out cont $Population $Reproduction $Crossover $Mutation_Rate $Sigma $Roulette $Tournament $Rank $Elite
        python3 test_fitness_chi.py $g
        python3 test_chi.py $g
        cp ${g}_fitnessScores.csv fitnessScores.csv
        cp ${g}_chiScores.csv chiScores.csv
        cp generationDNA.csv ${g}_generationDNA.csv
        cp parents.csv ${g}_parents.csv
        python3 data_write.py ${g}
        mv ${g}_generationData.csv Run/${Reproduction}_${Crossover}_${Mutation_Rate}_${Sigma}_${Roulette}_${Tournament}_${Rank}_${Run_Number}_${g}_generationData.csv
    fi

    echo waiting...
    echo waiting...
    echo waiting...
    echo waiting...
done

python3 test_plotter.py $Population $Generations $Reproduction $Crossover
python3 chi_plotter.py $Population $Generations $Reproduction $Crossover
mv fitness.png Run/${Reproduction}_${Crossover}_${Mutation_Rate}_${Sigma}_${Roulette}_${Tournament}_${Rank}_${Run_Number}_fitness.png
mv chi.png Run/${Reproduction}_${Crossover}_${Mutation_Rate}_${Sigma}_${Roulette}_${Tournament}_${Rank}_${Run_Number}_chi.png

for g in `seq 0 ${Generations}`
do 
    rm ${g}_fitnessScores.csv
    rm ${g}_chiScores.csv
    rm ${g}_generationDNA.csv
    rm ${g}_parents.csv
done
