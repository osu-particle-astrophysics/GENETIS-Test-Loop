#pragma once


// User Functions
#include "ConstraintARA.h"
#include "ConstraintPUEO.h"
#include "ConstraintAREA.h"

// Global Variables
extern int seed;
extern std::default_random_engine generator;
extern string design;

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

void Mutation(vector<vector<vector<float> > > & varOutput)
{
	// Start Flag
	cout << "Mutation Started" << endl;
	
	// Set random number generator
	uniform_real_distribution<float> select(0.0, 1.0);

	// itterate over individuals and genes to determine for mutations
	for(int i=reproduction_no; i<crossover_no+reproduction_no; i++)
	{
		for(int j=0; j<sections; j++)
		{	
			for(int k=0; k<genes; k++)
			{
				// Initialize vector to store temporary values as to not lose data
				vector<float> temp;
				
				// Save input genes into temp vector
				for(int x=0; x<genes; x++)
				{
					temp.push_back(varOutput[i][j][x]);
				}
					
				// generate random value for mutation
				float s = select(generator);
				
				// See if this gene will be mutated
				if(s < mutation_rate/100.0)
				{
					// Set the intersect condition
					bool intersect = true;
			
					// Attempt mutations and check if viable
					while (intersect == true)
					{
						// Set distribution based on current gene
						normal_distribution<float> mutate(varOutput[i][j][k], sigma/100.0*varOutput[i][j][k]);
					
						// Save the mutated value into temp[k]
						temp[k] = (mutate(generator));	
				
						// Check to see if the antenna is viable
						if (design == "ARA")
						{
							intersect = ConstraintARA(temp[0], temp[1], temp[2], temp[3]);
						}
						else if (design == "PUEO")
						{
							intersect = ConstraintPUEO(temp[0], temp[1], temp[2], temp[3], temp[4], temp[5], temp[6]);
						}
						else if (design == "AREA")
						{	
							// create 2D antenna
							std::vector<std::vector<float> > antenna (sections,std::vector <float>(genes, 0.0f));
							
							// populate the antenna
							for(int a=0; a<sections; a++)
							{	
								for(int b=0; b<genes; b++)
								{
									// if the section matches the outer loop, fill with temp values
									if (a==j)
									{
										antenna[a][b] = temp[b];
									}
									// if the section does not match the outer loop, will with permanent values
									else
									{
										antenna[a][b] = varOutput[i][a][b];
									}
								}
							}
							// rescale and replace antenna with gain corrected version
							intersect = ConstraintAREA(antenna);
							
							// replace temp values with the newly scaled ones
							for(int a=0; a<genes; a++)
							{	
								temp[a] = antenna[j][a];
							}
						}
					}
				}
				// Save temp values back to the output vector
				for (int y=0; y<genes; y++)
				{
					varOutput[i][j][y] = temp[y];
				}
				// Make sure temp is cleared between loops
				temp.clear();
			}
		}
	}
	// End Flag
	cout << "Mutation Complete" << endl;
}
