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

pop=100
arguement=1
generations=100
repro=3
cross=36
roul_no=2
tour_no=2
rank_no=6
zero=0
elite=0
M_rate=5
sigma=1


for a in {0..0..1} # Roulette
do
    for b in {1..1..1} # Tournament
    do
	for c in {9..9..1} # Rank
	do
	    r=$(( $a + $b + $c ))
	    if [ $r -eq 10 ]
	    then  
		for d in {0..0..1} # Reproduction
		do
		    for e in {36..36..2} # Crossover Make sure Reprodcution + Crossover < pop
		    do
			for f in {5..5..1} # M_rate
			do
			    for g in {1..1..1} # sigma
			    do
				for h in {0..0..1} # test count
				do
				    for i in `seq 0 ${generations}` #generation
				    do
					if [ $i -eq $zero ] 
					then
					    echo ${f}'_'${g}'_'${h} 'Generation 0'
					    ./a.out start $pop $repro $cross $f $g $roul_no $tour_no $rank_no $elite 
					    python3 test_fitness_inv.py $i
					    python3 test_chi.py $i
					    cp ${i}_fitnessScores.csv fitnessScores.csv
					    cp ${i}_ChiScores.csv ChiScores.csv
					    cp generationDNA.csv ${i}_generationDNA.csv
					    cp Parents.csv ${i}_Parents.csv
					    cp ${i}_fitnessScores.csv ${e}_${f}_${g}_${h}_${i}_fitnessScores.csv
					    cp ${i}_ChiScores.csv ${e}_${f}_${g}_${h}_${i}_ChiScores.csv
					    cp ${i}_generationDNA.csv ${e}_${f}_${g}_${h}_${i}_generationDNA.csv
					    cp ${i}_Parents.csv ${e}_${f}_${g}_${h}_${i}_Parents.csv
					    mv ${e}_${f}_${g}_${h}_${i}_generationDNA.csv Inverse
					    mv ${e}_${f}_${g}_${h}_${i}_Parents.csv Inverse
					    mv ${e}_${f}_${g}_${h}_${i}_fitnessScores.csv Inverse
					    mv ${e}_${f}_${g}_${h}_${i}_ChiScores.csv Inverse
					fi

					if [ $i -ne $zero ]
					then
					    echo ${f}'_'${g}'_'${h} 'Generation' $i
					    ./a.out cont $pop $repro $cross $f $g $roul_no $tour_no $rank_no $elite
					    python3 test_fitness_inv.py $i
					    python3 test_chi.py $i
					    cp ${i}_fitnessScores.csv fitnessScores.csv
					    cp ${i}_ChiScores.csv ChiScores.csv
					    cp generationDNA.csv ${i}_generationDNA.csv
					    cp Parents.csv ${i}_Parents.csv
					    #python3 fitness_check.py ${i}
					    cp ${i}_fitnessScores.csv ${e}_${f}_${g}_${h}_${i}_fitnessScores.csv
					    cp ${i}_ChiScores.csv ${e}_${f}_${g}_${h}_${i}_ChiScores.csv
					    cp ${i}_generationDNA.csv ${e}_${f}_${g}_${h}_${i}_generationDNA.csv
					    cp ${i}_Parents.csv ${e}_${f}_${g}_${h}_${i}_Parents.csv
					    mv ${e}_${f}_${g}_${h}_${i}_generationDNA.csv Inverse
					    mv ${e}_${f}_${g}_${h}_${i}_Parents.csv Inverse
					    mv ${e}_${f}_${g}_${h}_${i}_fitnessScores.csv Inverse
					    mv ${e}_${f}_${g}_${h}_${i}_ChiScores.csv Inverse
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
				    python3 test_plotter.py $pop $generations $repro $cross
				    python3 Chi_plotter.py $pop $generations $repro $cross
				    cp fitness.png ${e}_${f}_${g}_${h}_fitness.png
				    cp Chi.png ${e}_${f}_${g}_${h}_Chi.png
				    mv ${e}_${f}_${g}_${h}_fitness.png Inverse
				    mv ${e}_${f}_${g}_${h}_Chi.png Inverse
				    for i in `seq 0 $generations`
				    do
					rm ${i}_fitnessScores.csv
					rm ${i}_ChiScores.csv
					rm ${i}_Parents.csv
					rm ${i}_generationDNA.csv
				    done
				 done
			     done
			done
		   done
	      done
	   fi
	done
    done
done

