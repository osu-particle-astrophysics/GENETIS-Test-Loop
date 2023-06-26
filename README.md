 # GENETIS-Test-Loop
Repository for the GA testing loop written by Ryan Debolt 

Inside this repository is the framework needed to run the GENETIS test loop. 

Once pulled, one should then collect the version of the genetic algorithm that they are testing from the Shared-Code repository. To run a test loop, the user must first set the paths for all inputs and outputs the loop will use. You must set these paths in the following pieces of code: test_loop.sh, test_run.sh, single_run.sh. Onece paths have been set, the user must adjust the desired parameters. To do this, simply edit the range and step sizes within the named for loops and variables of each of the previously mentioned scipts as well as master_write.py. Once you have adjusted the parameters, the code should be ready and you can save and exit the file.

Now that the loop is prepped, you can run the loop in two ways:

     1. Terminal mode: This is run using ./single_run.sh and as the name implies is designed for single run use only. This function serves as a good place to debug the program as all outputs from each code bloack will be visible in the terminal. It is not suggested to do comprehensive tests using this mode.
     
     2. Parallel mode: This is run using ./test_loop.sh. This mode is designed to work in OSC's batch job system where it will call a new job for each test and set of parameters. This is excellent when performing searches for the best parameters or running tests that require averages. Though it is to be noted that the loop will not print run outputs in the terminal. With this in mind, one should not use this mode to conduct bug tests as they will likely go unoticed.  

These modes should automatically compile the GA, run all the programs, and sort the following files for you.

List of files:

     fitnessScores.csv: Saves fitness scores of each antenna
     
     metric.csv: Saves values from the metric used to generate fitness scores
     
     generationDNA.csv: Saves antenna DNA
     
     parents.csv: Saves parental information and seeds

     generationData.csv: Saves all above information in one file, good for saving storage space

     Master_gens.csv: Tracks information about how early it took a run to reach a benchmark metric value, good for checking performance of a test.


Here is a list of the functions and what they do:

     test_loop.sh: Submits batch jobs of tests in parrallel while adjusting run parameters.
     
     test_run.sh: Called by test_loop.sh, this code runs a single set of test parameters in parallel to other called tests and saves outputs to permanent directories. 
     
     single_run.sh: Effectively a test run that is run in the user's terminal. Good for debugging.
   
     test_fitness.py: This code will asign a metric value and fitness score to the antennas created by the GA, information output to fitnessScores.csv and metric.csv.
     
     fitness_check.py: averages fittness scores and propagates error for repeated individuals from the previous generation. 

     data_write.py: This code takes the outputs of our working files (generationDNA.csv, Parents.csv, fitnessScores.csv, metric.csv) and saves them into generationData.csv.  

     test_plotter.py: This code plots out the fitness scores and metric values of each individual in a generation.

     master_write.py: Writes data to a master file that tracks how many generations it took to reach the threshold metric value as well as makes plots of the min metric value at each generatation for all tests using the same parameters.


Have fun.
