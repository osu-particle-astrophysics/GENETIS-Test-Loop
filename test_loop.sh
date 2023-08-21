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
population=200

# Initialize job submission variables
count=0
start=0

# Loop over variables: define them in their ranges in their loops
for rank in {40..40..10} 
do
    for roulette in {30..30..10} 
    do
        for tournament in {30..30..10} 
        do
            selection=$(( $rank + $roulette + $tournament ))
            if [ $selection -eq $population ]
            then  
                for reproduction in {4..4..4} 
                do
                    for crossover in {76..76..4} 
                    do
                        for mutation in {16..16..4}
                        do
                            opperators=$(( $reproduction + $crossover + $mutation ))
                            if [ $opperators -le $population ]
                            then
                                for sigma in {10..10..5} 
                                do
                                    for test in {1..100..1}
                                    do
                                        # Submit run
                                        sbatch test_run.sh ${design} ${generations} ${population} ${rank} ${roulette} ${tournament} ${reproduction} ${crossover} ${mutation} ${sigma} ${test}
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
                            fi
                        done
                    done
                done
            fi
        done
    done
done

