#!/bin/bash

## Created by Ryan T Debolt
## created on 8/14/2023
## Created for: GENETIS Research group at Ohio State University

# set directories/paths
mkdir Flags
FlagsPath='Flags'
RunPath='Run'
GAPath='GA/SourceFiles'

# Compile the GA in its directory
g++ -std=c++11 $GAPath/New_GA.cpp -o $GAPath/GA.exe

# Set Constants
design="ARA"
generations=50
population=100

# Loop over variables: define them in their ranges in their loops
for rank in {10..100..10} 
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
                                        # Submit run
                                        sbatch file_cleanup.sh ${design} ${generations} ${population} ${rank} ${roulette} ${tournament} ${reproduction} ${crossover} ${mutation} ${sigma} ${test}
                                        count=$((count+1))
                                        if [ $count -ge 250 ]
                                        then
                                            echo batch submitted
                                            nfiles=$(ls $FlagsPath/ | wc -l)
                                            while [[ $(((nfiles)%250)) -ne 0 || $nfiles -eq $start ]] 
                                            do
                                                nfiles=$(ls $FlagsPath/ | wc -l)
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

