# GENETIS-Test-Loop
Repository for the GA testing loop written by Ryan Debolt 

Inside this repository exists all the files you should need to be able to run the test loop for the Genetis Project

Once pulled, to run a test loop, first look at the file test_loop.sh in a text editor. Adjust the for loops to run over the desired parameters that need to be tested and change the desired parameters being sent to the GA ( by default it is set on fixed parameters defined at the top of the code). Once you have adjusted the parameters, save and exit the file.

Now that the loop is prepped, run the loop with the command ./test_loop.sh. 

This should automatically compile the GA, run all the programs, and sort the files for you.

Have fun.
