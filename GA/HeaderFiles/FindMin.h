#pragma once

float FindMin(vector<vector<vector<float> > > & Gains)
{
  // Establish Gains vector length variables
  int Theta_index = 37;
  int Phi_index = 72;
  int Frequency_index = 60;
  float Min= Gains[0][0][0];

  // Find the minimum value of the Gains vector
  for (int i=0; i<Theta_index; i++)
  {
   for (int j=0; j<Phi_index; j++)
   {
    for (int k=0; k<Frequency_index; k++)
    {
      if(Gains[i][j][k] < Min)
      {
        Min = Gains[i][j][k];
      }
    }
   }
  }
  return(Min);
}
