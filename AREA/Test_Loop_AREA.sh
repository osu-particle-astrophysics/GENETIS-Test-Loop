#!/bin/bash

## Created by Ryan T Debolt
## created on 10/23/2020
## Created for: GENETIS Research group at Ohio State University
## Modified for use in AREA optimization 3/23/2023


## Algorithm

# run start for bicone GA
# run fitness score function
# run plotting function?
# run cont for bicone GA
# repeat for step 2-4 until desired amount of generations is complete

#echo 1

## Compile the GA
g++ -std=c++11 GA/ara_GA_noLinearDep_speedUpGainWritingTest_15March2023.cc

#echo 2

pop=100
generations=50
Count=0
Start=0

# Loop
for a in {25..25..1} # Roulette Crossover
do
	for b in {25..25..1} # Roulette Mutation
  do
		for c in {25..25..1} # Tournament Crossover 
		do
			for d in {25..25..1} # Tournament Mutation
			do
			    let pop_check=$(( $a + $b + $c + $d ))
				if [ $pop_check -eq $pop ]
    		then
				  for t in {1..1..1} # test count
				  do
				      #echo 2.1
						sbatch test_run_AREA.sh ${pop} ${generations} ${a} ${b} ${c} ${d} ${t}
						echo job submitted
						Count=$((Count+1))
						if [ $Count -ge 250 ]
						then
					  	echo batch submitted
					    nfiles=$(ls Plots/ | wc -l)
					    while [[ $(((nfiles)%250)) -ne 0 || $nfiles -eq $start ]] 
					    do
								nfiles=$(ls Plots/ | wc -l)
								echo $nfiles
								sleep 10
					    done
					    start=$nfiles
					    Count=0
						fi
				  done
				fi
			done
		done
	done
done

#echo 3
