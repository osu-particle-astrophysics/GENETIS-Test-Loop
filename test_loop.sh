#!/bin/bash

## Created by Ryan T Debolt
## created on 10/23/2020
## Created for: GENETIS Research group at Ohio State University


## Algorithm

#run start for bicone GA
#run fitness score function
# run plotting function?
#run cont for bicone GA
#repeat for step 2-4 until desired amount of generations is complete

g++ -std=c++11 GA.cpp

pop=50
arguement=1
generations=30
repro=10
cross=36
roul_no=6
tour_no=2
rank_no=2
zero=0
elite=0

for a in {0..0..1} # Roulette
do
    for b in {0..0..1} # Tournament
    do
	for c in {0..0..1} # Rank
	do
	    r=$(( $a + $b + $c ))
	    if [ $r -eq 10 ]
	    then  
		for d in {0..0..1} # Reproduction
		do
		    for e in {0..0..1} # Crossover Make sure Reprodcution + Crossover < pop
		    do
			for f in {0..0..1} # test number
			do
			    for i in `seq 0 $generations` #generation
			    do
				if [ $i -eq $zero ] 
				then
				    echo ${f} 'Generation 0'
				    ./a.out start $pop $repro $cross $roul_no $tour_no $rank_no $elite 
				    python3 test_fitness.py $i
				    cp ${i}_fitnessScores.csv fitnessScores.csv
				    cp generationDNA.csv ${i}_generationDNA.csv
				    cp ${i}_fitnessScores.csv ${f}_${i}_fitnessScores.csv
				    cp ${i}_generationDNA.csv ${f}_${i}_generationDNA.csv
				    mv ${f}_${i}_generationDNA.csv Results
				    mv ${f}_${i}_fitnessScores.csv Results
				fi

				if [ $i -ne $zero ]
				then
				    echo ${f} 'Generation' $i
				    ./a.out cont $pop $repro $cross $roul_no $tour_no $rank_no $elite
				    python3 test_fitness.py $i
				    cp ${i}_fitnessScores.csv fitnessScores.csv
				    cp generationDNA.csv ${i}_generationDNA.csv
				    python3 fitness_check.py ${i}
				    cp ${i}_fitnessScores.csv ${f}_${i}_fitnessScores.csv
				    cp ${i}_generationDNA.csv ${f}_${i}_generationDNA.csv
				    mv ${f}_${i}_generationDNA.csv Results
				    mv ${f}_${i}_fitnessScores.csv Results
				fi
				echo waiting... 
				sleep 0.25
				echo ...
				sleep 0.25
				echo ...
				sleep 0.25
				echo ...
				sleep 0.25 #waits 1/4 seconds
			     done
			done
		   done
		   python3 test_plotter.py $pop $generations
		   cp fitness.png ${f}_fitness.png
		   mv ${f}_fitness.png Results
	      done
	   fi
	done
    done
done

