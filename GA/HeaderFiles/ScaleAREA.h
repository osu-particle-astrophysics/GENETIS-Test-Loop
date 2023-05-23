#pragma once

std::vector<std::vector<float> > ScaleAREA(vector<vector<float> > & antenna, vector<vector<vector<float> > > & Gains)
{
  // Establish Gains vector length variables
  int Theta_index = 37;
  int Phi_index = 72;
  int Frequency_index = 60;
  float Min = 0.0;
  
  // Find Min Vlaue
  Min = FindMin(Gains);
  
  // Check if Min is negative
  if(Min< 0.0)
  {
    // Scale the individual to conserve energy
    // Loop over all non-constant gain coefficients
    // Currently not adjusting extrapolating coefficient
    for(int i=1; i<13; i++)
    {
      antenna[0][i] = (1.0/(1.0-Min))*antenna[0][i];
    }
  }
  
  // Return scaled individual
  return antenna;
}
