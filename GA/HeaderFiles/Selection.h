#pragma once


// User Functions
#include "Rank.h"
#include "Roulette.h"
#include "Tournament.h"

// Gloabal Variables
extern int seed;
extern int generation;
extern int population;
extern int sections;
extern int genes;
extern int reproduction_no;
extern int crossover_no;
extern int mutation_rate;
extern int sigma; 
extern int rank_no; 
extern int roulette_no;
extern int tournament_no;

void Selection(int Opp_no, vector<float> Fitness, vector<int> & locations)
{
 // Start Flag
 cout << "Begining Selection" << endl;
 
 // initialize Values
 int Roul_Select = (double)roulette_no/population * 1.0*Opp_no;
 int Rank_Select = (double)rank_no/population * 1.0*Opp_no;
 int Tour_Select = (double)tournament_no/population * 1.0*Opp_no;
 
 // Check to make sure values sum to correct value
 while(Roul_Select + Rank_Select + Tour_Select < Opp_no)
 {
  
  float roul_cut = roulette_no/population * 1.0*Opp_no - 1.0*Roul_Select;
  float rank_cut = rank_no/population * 1.0*Opp_no - 1.0*Rank_Select;
  float tour_cut = tournament_no/population * 1.0*Opp_no - 1.0*Tour_Select;

  if (roul_cut > rank_cut && roul_cut > tour_cut)
  {
   Roul_Select = Roul_Select+1;
  }
  
  else if (rank_cut > roul_cut && rank_cut > tour_cut)
  {
   Rank_Select = Rank_Select+1;
  }
  
  else if (tour_cut > roul_cut && tour_cut > rank_cut)
  {
   Tour_Select = Tour_Select+1;
  }
  
  else
  {
    if (Rank_Select > Roul_Select && Rank_Select > Tour_Select)
    {
      Rank_Select = Rank_Select + 1;
    }
    
    else if (Roul_Select > Rank_Select && Roul_Select > Tour_Select)
    {
      Roul_Select = Roul_Select + 1;
    }
    
    else if (Tour_Select > Roul_Select && Tour_Select > Rank_Select)
    {
      Tour_Select = Tour_Select + 1;
    }
    
    else
    {
      Rank_Select = Rank_Select+1;
    }
  }          
 }
 
 // Call each selection method
 for(int i=0; i<Roul_Select; i++)
 {
  locations.push_back(Roulette(Fitness));
 }
 for(int i=0; i<Rank_Select; i++)
 {
  locations.push_back(Rank(Fitness));
 }
 for(int i=0; i<Tour_Select; i++)
 {
  locations.push_back(Tournament(Fitness));
 }
 
 // End Flag
 cout << "Selection Finished" << endl;
}
