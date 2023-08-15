#!/bin/bash

## Created by Ryan T Debolt
## created on 8/14/2023
## Created for: GENETIS Research group at Ohio State University

# set directories/paths
PlotsPath='Plots'
RunPath='Run'
GAPath='GA/SourceFiles'

# Compile the GA in its directory
g++ -std=c++11 $GAPath/New_GA.cpp -o $GAPath/GA.exe

# Set Constants
design="ARA"
generations=50
population=100

# Move to coprrect directory
mv $RunPath

# Loop over variables: define them in their ranges in their loops
for rank in {20..100..10} 
do
    for roulette in {0..100..10} 
    do
        for tournament in {0..100..10} 
        do
            selection=$(( $rank + $roulette + $tournament ))
            if [ $selection -eq $population ]
            then  
                for reproduction in {4..16..4} 
                do
                    for crossover in {72..100..4} 
                    do
                        for mutation in {8..20..4}
                        do
                            opperators=$(( $reproduction + $crossover + $mutation ))
                            if [ $opperators -le $population ]
                            then
                                for sigma in {10..10..5} 
                                do
                                    for test in {1..10..1}
                                    do
                                        # Condense test files
                                        runname="${rank}_${roulette}_${tournament}_${reproduction}_${crossover}_${mutation}_${sigma}_${test}"
                                        python test_write.py $design $generations $population $runname

                                        # Remove corresponding files
                                        rm ${runname}_*_generationData.csv
                                    done
                                done
                            fi
                        done
                    done
                done
            fi
        done
    done
done

