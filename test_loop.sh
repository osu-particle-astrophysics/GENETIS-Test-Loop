#!/bin/bash

## Created by Ryan T Debolt
## created on 10/23/2020
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
population=50

# Initialize job submission variables
count=0
start=0

# Loop over variables: define them in their ranges in their loops
for rank in {30..30..2} 
do
    for roulette in {10..10..2} 
    do
        for tournament in {10..10..2} 
        do
            selection=$(( $rank + $roulette + $tournament ))
            if [ $selection -eq $population ]
            then  
                for reproduction in {2..2..2} 
                do
                    for crossover in {46..46..4} 
                    do
                        for mutation_rate in {25..25..5}
                        do
                            for sigma in {7..7..1} 
                            do
                                for test in {1..10..1}
                                do
                                    # Submit run
                                    sbatch test_run.sh ${design} ${generations} ${population} ${rank} ${roulette} ${tournament} ${reproduction} ${crossover} ${mutation_rate} ${sigma} ${test}
                                    count=$((count+1))
                                    if [ $count -ge 250 ]
                                    then
                                        echo batch submitted
                                        nfiles=$(ls $PlotsPath/ | wc -l)
                                        while [[ $(((nfiles)%500)) -ne 0 || $nfiles -eq $start ]] 
                                        do
                                            nfiles=$(ls $PlotsPath/ | wc -l)
                                            echo $nfiles
                                            sleep 10
                                        done
                                        start=$nfiles
                                        count=0
                                    fi
                                done
                            done
                        done
                    done
                done
            fi
        done
    done
done

