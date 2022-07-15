 # GENETIS-Test-Loop
Repository for the GA testing loop written by Ryan Debolt 

Inside this repository exists all the files you should need to be able to run the test loop for the Genetis Project

Once pulled, to run a test loop, first look at the file test_loop.sh in a text editor. Adjust the for loops to run over the desired parameters, use the correct programs that need to be tested and change the desired parameters being sent to the GA ( by default it is set on fixed parameters defined at the top of the code). Once you have adjusted the parameters, save and exit the file.

Now that the loop is prepped, run the loop with the command ./test_loop.sh. 

This should automatically compile the GA, run all the programs, and sort the files for you.

List of files:

     fitnessScores.csv: Saves fitness scores of each antenna
     
     chiScores.csv: Saves chi squared values
     
     generationDNA.csv: Saves antenna DNA
     
     parents.csv: Saves parental information and seeds

     generationData.csv: Saves all above information in one file

     master_gens.csv: Tracks information about how early it took a run to reach a benchmark 


Here is a list of the functions and what they do:

     test_loop.sh: Runs the test loop and outputs to the Run Directory, you should move files from these directories into a specialty name directory in the results folder

     GA.cpp: Code for the GA run in the test. Reads in fitnessScores.csv and generationData.csv
     
     test_fitnes_*.py: These codes will asign a fitness score to the antennas created by the GA, information output to fitnessScores.csv

     test_chi.py: This code solves for the chi squared value of each antenna, use to guage performance apart from fitness

     data_write.py: This code takes the outputs of our working files (generationDNA.csv, Parents.csv, fitnessScores.csv, chiScores.csv) and saves them into generationData.csv   

     test_plotter.py: This code plots out the fitness scores

     chi_plotter.py: This code plots out the chi squared values

     master_write.py: writes data to a master file that traks the maximum fitness scores of the final generation, needs to be run in a results directory

     file_sort.py: plots and writes data into master_gens.csv

Have fun.
