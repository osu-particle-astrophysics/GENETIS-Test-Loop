#pragma once

#include <vector>
#include <random>
#include "ConstraintAREA.h"
extern int genes;
extern int sections;
extern int seed;
extern std::default_random_engine generator;

std::vector<std::vector<float> > GenerateAREA()
{
  // initialize an interesect condidtion
  bool intersect = true;
  std::vector<std::vector<float> > antenna (sections,std::vector <float>(genes, 0.0f));
  
  // variables
  long double PI = 3.14159265359;
  float min_gain_coeff = -5.0;
  float max_gain_coeff = 5.0;
  float min_phase_coeff = -5.0;
  float max_phase_coeff = 5.0;
  
  // while the intersect condition is true, generate the side of an individual
  intersect = true;
  while(intersect==true)
  {
    // loop over genes (coeffs that weight the sphereical harm terms to calculate the gain/phase as a function of theta and phi)
    for(int i=0; i<genes; i++)
    {
      if(i==0){
        // first gain coeff is always 2*sqrt(PI), necessary for power conservation
        antenna[0][i] = 2*sqrt(PI);
      }
      
      else{
        // other gain coeffs are randomly generated
        std::uniform_real_distribution <float> distribution_gain_coeff(min_gain_coeff, max_gain_coeff);          // Gain Coefficients
        antenna[0][i] = distribution_gain_coeff(generator);
      }
      
      // all phase coeffs are randomly generated
      // DOUBLE CHECK THIS "FACT"!
      std::uniform_real_distribution <float> distribution_phase_coeff(min_phase_coeff, max_phase_coeff); // Phase Coefficients
      antenna[1][i] = distribution_phase_coeff(generator);
    }
    
    // Take the individual and pass it to the constraint function and update the intersect condition
    intersect = ConstraintAREA(antenna);
  }
  
  return(antenna);
}
