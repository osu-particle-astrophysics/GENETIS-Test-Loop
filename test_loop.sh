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
generations=10
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
		for d in {6..6..6} # Reproduction
		do
		    for e in {64..64..12} # Crossover Make sure Reprodcution + Crossover < pop
		    do
			de=$(( $d +$e ))
			if [ $de -le $pop ]
			then
			    for f in {10..10..5} # M_rate
			    do
				if [ $f -ne 0 ]
				then
				    sigma=1
				fi
				if [ $f -eq 0 ] 
				then
				    sigma=1
				fi
				for (( g=1; g <= $sigma; g++ )) # sigma
				do
				    for h in {1..1..1} # test count
				    do
					for i in `seq 0 ${generations}` #generation
					do
					    if [ $i -eq $zero ] 
					    then
						echo ${d}'_'${e}'_'${f}'_'${g}'_'${h} 'Generation 0'
						./a.out start $pop $d $e $f $g $roul_no $tour_no $rank_no $elite 
						python3 test_fitness_chi.py $i # Call the fitness function desired (see Fitness Function Directory for alternate options) 
						python3 test_chi.py $i
						cp ${i}_fitnessScores.csv fitnessScores.csv
						cp ${i}_chiScores.csv chiScores.csv
						cp generationDNA.csv ${i}_generationDNA.csv
						cp parents.csv ${i}_parents.csv
						python data_write.py ${i}
						mv ${i}_generationData.csv Run/${d}_${e}_${f}_${g}_${h}_${i}_generationData.csv
					    fi

					    if [ $i -ne $zero ]
					    then
						echo ${d}'_'${e}'_'${f}'_'${g}'_'${h} 'Generation' ${i}
						./a.out cont $pop $d $e $f $g $roul_no $tour_no $rank_no $elite
						python3 test_fitness_chi.py $i # call fitness function
						python3 test_chi.py $i
						cp ${i}_fitnessScores.csv fitnessScores.csv
						cp ${i}_chiScores.csv chiScores.csv
						cp generationDNA.csv ${i}_generationDNA.csv
						cp parents.csv ${i}_parents.csv
						python3 fitness_check.py ${i}
						python data_write.py ${i}
						mv ${i}_generationData.csv Run/${d}_${e}_${f}_${g}_${h}_${i}_generationData.csv
					    fi
					    echo waiting... 
					    echo ...
					    echo ...
					    echo ...
					done
					python3 test_plotter.py $pop $generations $repro $cross  # Call desired Plotter (see Plotting functions for alternatives)
					python3 chi_plotter.py $pop $generations $repro $cross
					cp fitness.png ${d}_${e}_${f}_${g}_${h}_fitness.png
					cp chi.png ${d}_${e}_${f}_${g}_${h}_chi.png
					mv ${d}_${e}_${f}_${g}_${h}_fitness.png Run
					mv ${d}_${e}_${f}_${g}_${h}_chi.png Run
					for i in `seq 0 $generations`
					do
					    rm ${i}_fitnessScores.csv
					    rm ${i}_chiScores.csv
					    rm ${i}_parents.csv
					    rm ${i}_generationDNA.csv
					done
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

