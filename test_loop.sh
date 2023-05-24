#!/bin/bash

## Created by Ryan T Debolt
## created on 10/23/2020
## Created for: GENETIS Research group at Ohio State University

# Compile the GA in its directory
g++ -std=c++11 GA/SourceFiles/GA.cpp GA/SourceFiles/GA.exe

# Set Constants
Population=100
Generations=50
Design="ARA"

# Initialize job submission variables
Count=0
start=0

# Loop over variables: define them in their ranges in their loops
for Rank in {2..2..2} 
do
    for Roulette in {2..2..2} 
    do
		for Tournament in {6..6..2} 
		do
	    	Selection=$(( $Rank + $Roulette + $Tournament ))
	    	if [ $Selection -eq $Population ]
	    	then  
				for Reproduction in {0..12..4} 
				do
		    		for Crossover in {88..100..4} 
		    		do
						for MutationRate in {15..25..5}
						do
							for Sigma in {1..1..1} 
							do
				    			for Test in {1..10..1} 
				   				do
									# Submit run
									sbatch test_run.sh ${Design} ${Generations} ${Population} ${Rank} ${Roulette} ${Tournament} ${Reproduction} ${Crossover} ${MutationRate} ${Sigma} ${Test}
									Count=$((Count+1))
									if [ $Count -ge 250 ]
									then
					    				echo batch submitted
					    				nfiles=$(ls Plots/ | wc -l)
					    				while [[ $(((nfiles)%500)) -ne 0 || $nfiles -eq $start ]] 
					   					do
										nfiles=$(ls Plots/ | wc -l)
										echo $nfiles
										sleep 10
					    				done
					    				start=$nfiles
					    				Count=0
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

