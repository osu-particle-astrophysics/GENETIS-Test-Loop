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


for a in {2..2..2} # Roulette
do
    for b in {2..2..2} # Tournament
    do
	for c in {6..6..2} # Rank
	do
	    r=$(( $a + $b + $c ))
	    if [ $r -eq 10 ]
	    then  
		for d in {0..0..6} # Reproduction
		do
		    for e in {100..100..6} # Crossover Make sure Reprodcution + Crossover < pop
		    do
			de=$(( $d +$e ))
			if [ $de -le $pop ]
			then
			    for f in {15..15..5} # M_rate
			    do
				if [ $f -ne 0 ]
				then
				    sigma=5
				fi
				if [ $f -eq 0 ] 
				then
				    sigma=1
				fi
				for (( g=5; g <= $sigma; g++ )) # sigma
				do
				    for h in {1..1..1} # test count
				    do
					./test_run.sh ${pop} ${generations} ${d} ${e} ${f} ${g} ${a} ${b} ${c} ${elite} ${h}
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

