#!/bin/bash

## Created by Ryan T Debolt
## created on 10/23/2020
## Created for: GENETIS Research group at Ohio State University


## Algorithm

# run start for bicone GA
# run fitness score function
# run plotting function?
# run cont for bicone GA
# repeat for step 2-4 until desired amount of generations is complete

g++ -std=c++11 GA.cpp

pop=100
arguement=1
generations=50
repro=3
cross=36
roul_no=2
tour_no=2
rank_no=6
zero=0
elite=0
M_rate=5
sigma=1

Count=0
start=0

for a in {2..2..2} # Roulette
do
    for b in {2..2..2} # Tournament
    do
	for c in {6..6..2} # Rank
	do
	    r=$(( $a + $b + $c ))
	    if [ $r -eq 10 ]
	    then  
		for d in {0..12..4} # Reproduction
		do
		    for e in {88..100..4} # Crossover Make sure Reprodcution + Crossover < pop
		    do
			de=$(( $d +$e ))
			if [ $de -le $pop ]
			then
			    for f in {15..25..5} # M_rate
			    do
				if [ $f -ne 0 ]
				then
				    sigma=7
				fi
				if [ $f -eq 0 ] 
				then
				    sigma=3
				fi
				for (( g=3; g <= $sigma; g++ )) # sigma
				do
				    for h in {1..10..1} # test count
				    do
					sbatch test_run.sh ${pop} ${generations} ${d} ${e} ${f} ${g} ${a} ${b} ${c} ${elite} ${h}
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
			fi
		   done
	      done
	   fi
	done
    done
done

