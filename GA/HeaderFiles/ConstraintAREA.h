#pragma once

// Includes
#include "SolveGains.h"
#include "FindMin.h"
#include "ScaleAREA.h"

bool ConstraintAREA(vector<vector<float> > & antenna)
{
  bool intersect = true;
  
  // Fetch Gains of this antenna design
  vector<vector<vector<float>>> Gains = SolveGains(antenna);
    
  // Use gains to check energy conservation
  // Check if min gain value is negative, if it is, rescale gain coefficents 
  float Min = FindMin(Gains);
  while (intersect == true)
  {
    if (Min >= 0.0)
    {
      intersect = false;
    }
    else
    {
      // Scale the antenna's coefficients
      antenna = ScaleAREA(antenna, Gains);
    
      // Re-solve Gains and Min
      vector<vector<vector<float>>> Gains = SolveGains(antenna); 
      Min = FindMin(Gains);
    }
  }
  
  // Return the interesect constraint
  return intersect;
}
