#!/bin/bash

## Created by Bryan Reynolds
## January 2023

#Add arguments

#compile AREA GA
g++ -std=c++11 ara_GA.cpp #BRYAN: check name

#loop over generations
for g in `seq 0 ${Generations}`
do
    #if initial generation, create and test initial population
    if [ $g -eq 0 ]
    then
	echo 'Generation 0- will add argument info later'
	#call GA for gen 0
	./a.out -gp $A $B $C $D -p 0
	
    fi

    if [ $g -ne 0 ]
    then
	echo 'Generation G- will add argument info later'
	#call GA for generation G
	#FIX NAMEING- CHILD_NO == NPOP
	./a.out -gp $A $B $C $D -p $CHILD_NO ./$RunName/gen_$LAST_CNT/child*

    fi

    #call file to calculate fitness score (to be written)
    #save copies of files created into storage directory (possibly condense)

    #may need to add wait functions here
done

#call plotting scripts
#save plots in plot directory with unique names

for g in `seq 0 ${Generations}`
do
    #remove excess csv files
done
