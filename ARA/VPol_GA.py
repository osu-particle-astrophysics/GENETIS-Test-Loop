# This code is modeled after the Curved_GA.cpp used to design VPol Bicone antennas
# Written By Ryan T Debolt 8/4/2022

# IMPORTS
import numpy as np
import csv
import argparse
import random
import time
seed = 1 #time.perf_counter() #can establish seed
random.seed(seed)

# FUNCTIONS

# Utilities
def DataRead(Fitness, I_Pop, Gen):
    '''Reads in data from files for the GA to use'''
    # Read in generationDNA.csv
    with open("generationDNA.csv", 'r') as f1:
        csv_read = csv.reader(f1, delimiter =",")
        j=0
        for i, row in enumerate(csv_read):
            if i>8:
                if( i%2 != 0):
                    I_Pop[j][0][0] = float(row[0])
                    I_Pop[j][0][1] = float(row[1])
                    I_Pop[j][0][2] = float(row[2])
                    I_Pop[j][0][3] = float(row[3])
                if( i%2 == 0):
                    I_Pop[j][1][0] = float(row[0])
                    I_Pop[j][1][1] = float(row[1])
                    I_Pop[j][1][2] = float(row[2])
                    I_Pop[j][1][3] = float(row[3])
                    j=j+1
    f1.close()

    # Read in fitnessScores.csv
    with open("fitnessScores.csv", 'r') as f2:
        csv_read = csv.reader(f2, delimiter = ",")
        for i, row in enumerate(csv_read):
            if (i >=2):
                Fitness.append(float(row[0]))
    f2.close()
    return

def DataWrite(NPop, F_Pop, freq_coeff, freqVector, S_no, C_no, selected, Gen, seed):
    '''Writes data out to files from the GA'''
    # Write generationDNA.csv 
    with open("generationDNA.csv", 'w') as f1:
        f1.write("Hybrid of Rank, Roulette, and Tournament \n")
        f1.write("Written by Ryan Debolt, adapted from GA written by David Liu \n")
        f1.write("Notable contributors: Julie Rolla, Hannah Hasan, and Adam Blenk \n")
        f1.write("Done at The Ohio State University \n")
        f1.write("Working on behalf of Dr. Amy Connolly \n")
        f1.write("And the ANITA project \n")
        f1.write("Revision date: 8/5/2022 \n")
        for i in range(0, freq_coeff):
            if (i==freq_coeff-1):
                f1.write(str(freqVector[i])+"\n")
            else:
                f1.write(str(freqVector[i])+",")
        f1.write("Matrices for this Generation: "+"\n")
        for i in range(0, NPop):
            for j in range(0,Sections):
                for k in range(0,Parameters):
                    if(k==(Parameters-1)):
                        f1.write(str(F_Pop[i][j][k])+"\n")
                    else:
                        f1.write(str(F_Pop[i][j][k])+",")
    f1.close()

    # Write parents.csv if not gen 0
    if (Gen != 0):
        with open("parents.csv", 'w') as f2:
            f2.write("Location of individuals used to make this generation: \n")
            f2.write("seed: " +str(seed)+ "\n")
            f2.write("\n")
            f2.write("Current Gen, Parent 1, Parent 2, Operator \n")
            j=0

            for i in range(0,NPop):
                if (i<S_no):
                    f2.write(str(i+1)+", "+ str(selected[i]+1) + ", NA, Reproduction \n" )
                elif(i>=S_no and i<C_no+S_no):
                    if(j%2 ==0 ):
                        f2.write(str(i+1)+", "+ str(selected[i]+1) + ", " + str(selected[i+1]+1) + ", Crossover \n")
                    elif(j%2 != 0 ):
                        f2.write(str(i+1)+", "+ str(selected[i-1]+1) + ", " + str(selected[i]+1) + ", Crossover \n")
                    j=j+1
                else:
                    f2.write(str(i+1)+", NA, NA, Immigration\n")
        f2.close()
                
    return

def Sort(Fitness, I_Pop, P_loc):
    '''Sorts the incoming data by fitness scores'''
    O_loc = []
    for z in range(0,len(Fitness)):
        O_loc.append(z)

    for i in range(len(Fitness)):
        temp = Fitness[i]
        T = O_loc[i]
        location = I_Pop[i]
        j = i
        while( j>0 and Fitness[j-1] < temp):
            Fitness[j] = Fitness[j-1]
            P_loc[j] = P_loc[j-1]
            I_Pop[j] = I_Pop[j-1]
            j = j-1
        Fitness[j] = temp
        P_loc[j] = T 
        I_Pop[j] = location
    return


def Generate(Sections, Parameters):
    '''Generates a random individual, used in immigration and initial population'''
    Individual= [[0]*Parameters for i in range(Sections)]
    for j in range(0,Sections):
        intersect=True
        while(intersect==True):
           Individual[j][0] = random.uniform(0.0, 7.5)     # Radius
           R = Individual[j][0]
           Individual[j][1] = random.uniform(10.0, 140.0)  # Length
           L = Individual[j][1]
           Individual[j][2] = random.uniform(-1.0, 1.0)    # A Coeff
           A = Individual[j][2]
           Individual[j][3] = random.uniform(-1.0, 1.0)    # B Coeff
           B = Individual[j][3]
           intersect = SizeCheck(R, L, A, B)
    return(Individual)

def SizeCheck(R, L, A, B):
    '''Test to make sure that the individual's radius never exceeds the bore hole size'''
    intersect = True
    max_radius = 7.5
    min_length = 10.0
    max_length = 140.0
    min_coeff = -1.0
    max_coeff = 1.0
    end_point = A*L*L + B*L + R # Final Value of function
    if A != 0.0:
        vertex = (R - (B*B)/(4*A))  # Vertex of quadratic
    else:
        vertex = end_point
    # Check if parameters are exceeded, return True if they are
    if (A==0.0 and max_radius > end_point and end_point >= 0.0):
        if(R<0.0 or L<min_length or L>max_length or A<min_coeff or A>max_coeff or B<min_coeff or B>max_coeff):
            intersect = True
        else:
            intersect = False
    elif (A!=0.0 and max_radius > end_point and end_point >= 0.0 and max_radius > vertex and vertex >= 0.0):
        if(R<0.0 or L<min_length or L>max_length or A<min_coeff or A>max_coeff or B<min_coeff or B>max_coeff):
            intersect = True
        else:
            intersect = False
    else:
        intersect = True
    return(intersect)

# Selection Methods

def Select(Opp_no, Fitness, Elite_no, Roul_no, Rank_no, Tour_no, Pool):
    '''Calls selection methods based on proportions provided'''
    # initialize array to store locations
    locations = []

    # define how many individuals will be selected through each method
    Elite_select = round(Elite_no/100*Opp_no) # may need to change for elite
    Roul_select = round(Roul_no/100*Opp_no)
    Rank_select = round(Rank_no/100*Opp_no)
    Tour_select = round(Tour_no/100*Opp_no)

    # check to make sure the correct amount of individuals are being selected
    while(Elite_select + Roul_select + Rank_select + Tour_select != Opp_no):
        if(Elite_no/100*Opp_no - Elite_select >= 0.5 ):
            Elite_select = Elite_select + 1
        elif(Roul_no/100*Opp_no - Roul_select >= 0.5):
            Roul_select = Roul_select + 1
        elif(Rank_no/100*Opp_no - Rank_no >= 0.5):
            Rank_select = Rank_select + 1
        elif(Tour_no/100*Opp_no - Tour_select >= 0.5):
            Tour_select = Tour_select + 1

    # call selection methods
    for i in range(Elite_select):
        locations.append(Elite())
    for i in range(Roul_select):
        locations.append(Roulette(Fitness))
    for i in range(Rank_select):
        locations.append(Rank(Fitness))
    for i in range(Tour_select):
        locations.append(Tournament(Pool, Fitness))

    # return the location array
    return(locations)

def Elite():
    '''Selects the best individual overall, use sparingly or not at all'''
    return(0)

def Rank(Fitness):
    '''Selects based on rank weighted poportions'''
    probabilities = []
    sum_npop = 0
    
    # Assign probabilities
    for i in range(len(Fitness)):
        sum_npop = sum_npop +i
    for j in range(len(Fitness)):
        probabilities.append((len(Fitness)-j)/(sum_npop))
        
    # Select individual
    select = random.random()
    x =0
    probability_sum = 0
    while probability_sum <= select:
        probability_sum = probability_sum + probabilities[x]
        x = x+1
    return(x)

def Roulette(Fitness):
    '''Selects based on fitness weighted proportions'''
    probabilities = []
    total_fitness = 0

    # Assign probabilities
    for i in range(len(Fitness)):
        total_fitness = total_fitness + Fitness[i]
    for j in range(len(Fitness)):
        probabilities.append(Fitness[j]/total_fitness)
    select = random.random()
    x = 0
    probability_sum = 0

    # Select individual
    while probability_sum <= select:
        probability_sum = probability_sum + probabilities[x]
        x = x+1

    return(x)

def Tournament(Pool, Fitness):
    '''Selects best individual from subset of the population'''
    contenders = []

    # Fill pool
    for i in range(Pool):
        contenders.append(random.randint(0, len(Fitness)-1))

    # Select best individual from the pool
    select = 0
    for j in range(Pool):
        if(Fitness[contenders[j]] > Fitness[contenders[select]]):
            select = j

    return(contenders[select])


# Genetic Opperators

def Initialize(F_Pop, Sections, Parameters):
    '''Generates a complete inital population of random individuals'''
    for i in range(len(F_Pop)):
        F_Pop[i] = Generate(Sections, Parameters)
    return

def Survival(S_no, I_Pop, F_Pop, Fitness, Elite_no, Roul_no, Rank_no, Tour_no, Pool, P_loc, selected, Sections, Parameters):
    '''Simulates survival of individuals into the next generation'''
    S_Select = Select(S_no, Fitness, Elite_no, Roul_no, Rank_no, Tour_no, Pool)
    for i in range(0, S_no):
        selected.append(P_loc[S_Select[i]])
        for j in range(0, Sections):
            for k in range(0, Parameters):
                F_Pop[i][j][k] = I_Pop[S_Select[i]][j][k]
    return

def Crossover(NPop, S_no, C_no, I_Pop, F_Pop, Fitness, Elite_no, Roul_no, Rank_no, Tour_no, Pool, M_rate, sigma, P_loc, selected, Sections, Parameters):
    '''Simulates sexual; reproduction of two parent individuals to create children'''
    C_Select = Select(C_no, Fitness, Elite_no, Roul_no, Rank_no, Tour_no, Pool)
    for i in range(S_no, S_no + C_no, 2):
        selected.append(P_loc[C_Select[i-S_no]])
        selected.append(P_loc[C_Select[i+1-S_no]])
        for j in range(0,Sections):
            intersect=True
            while(intersect==True):
                for k in range(0, Parameters):
                    swap = random.randint(0,1)
                    if(swap == 0):
                        F_Pop[i][j][k] = I_Pop[C_Select[i-S_no]][j][k]
                        F_Pop[i+1][j][k] = I_Pop[C_Select[i+1-S_no]][j][k]
                    else:
                        F_Pop[i][j][k] = I_Pop[C_Select[i+1-S_no]][j][k]
                        F_Pop[i+1][j][k] = I_Pop[C_Select[i-S_no]][j][k]
                intersect_1 = SizeCheck(F_Pop[i][j][0], F_Pop[i][j][1], F_Pop[i][j][2], F_Pop[i][j][3])
                intersect_2 = SizeCheck(F_Pop[i+1][j][0], F_Pop[i+1][j][1], F_Pop[i+1][j][2], F_Pop[i+1][j][3])
                if (intersect_1==False and intersect_2==False):
                    intersect=False
                else:
                    intersect=True
    print("Starting mutation\n")
    Mutation(NPop, F_Pop, S_no, S_no + C_no, M_rate, sigma, Sections, Parameters)
    return

def Mutation(NPop, F_Pop, start, stop, M_rate, sigma, Sections, Parameters):
    '''Mutates the genes of crossover produced children about a gaussean'''
                    
    for i in range(start, stop):
        for j in range(0, Sections):
            for k in range(0, Parameters):
                g = [ [ [0]*Parameters for v in range(Sections) ] for w in range(NPop) ]
                for b in range(0, Parameters):
                    g[i][j][b] = F_Pop[i][j][b]
                if M_rate >= random.uniform(0.0, 1.0):
                    intersect = True
                    while(intersect==True):
                        g[i][j][k] = random.gauss(F_Pop[i][j][k], sigma*F_Pop[i][j][k])
                        intersect = SizeCheck(g[i][j][0], g[i][j][1], g[i][j][2], g[i][j][3])
                    F_Pop[i][j][k] = g[i][j][k]
    return

def Immigration(S_no, C_no, I_no, F_Pop, Sections, Parameters):
    '''Simulates individuals from outside populations joining the population'''
    for i in range(S_no+C_no, S_no+C_no+I_no):
        F_Pop[i] = Generate(Sections, Parameters)
        
    return
    

####################################################################################################################



# MAIN CODE BLOCK

# Read in Arguements
parser = argparse.ArgumentParser();
parser.add_argument("NPop", type=int)     # Number of individuals in an entire population
parser.add_argument("Gen", type=int)      # Current Generation
parser.add_argument("S_no", type=int)     # Number of individuals that survive to the next generation
parser.add_argument("C_no", type=int)     # Number of individuals created sexualy
parser.add_argument("I_no", type=int)     # Number of individuals generated by Immigration
parser.add_argument("M_rate", type=int)   # Ratio/100 of mutation chance occuring
parser.add_argument("Sigma", type=int)    # Ratio/100 of gaussean width controller
parser.add_argument("Elite_no", type=int) # Ratio/100 of individuals selected by Elite
parser.add_argument("Roul_no", type=int)  # Ratio/100 of individuals selected by Roulette
parser.add_argument("Rank_no", type=int)  # Ratio/100 of individuals selected by Rank
parser.add_argument("Tour_no", type=int)  # Ratio/100 of individuals selected by Tournament
x = parser.parse_args()

# Initialize contestants and arrays
Pool = int(0.07*x.NPop)                                                         # Pool size that will be used in tournaments
Fitness = []                                                                    # Initalize array of fitness scores for each individual
Sections = 2                                                                    # How many sections Will there be in this design
Parameters = 4                                                                  # How many parameters will there be for each section
I_Pop = [ [ [0]*Parameters for i in range(Sections) ] for j in range(x.NPop) ]  # Initialize array for initial population
F_Pop = [ [ [0]*Parameters for i in range(Sections) ] for j in range(x.NPop) ]  # Initialize array for final population
M_rate = x.M_rate/100.0                                                         # Set mutation rate to a floating point number
Sigma = x.Sigma/100.0                                                           # Set gausean width to a folating point number
P_loc = [0]*x.NPop                                                              # Initialize array that stores location of parents pre-sorting
freq_coeff = round(( 1.0667 - 0.08333)/ 0.01667 +1)                             # need this for generationDNA not used otherwise
freqVector = [0.0]*freq_coeff                                                   # need this for generationDNA not used otherwise
selected = []                                                                   # Saves the location of parents from P_loc that were used in selection

# Check passed in arguments
if(x.S_no+x.C_no+x.I_no != x.NPop):
    print("ERROR: Opperation numbers do not add to NPOP")
    quit()

if(x.Elite_no+x.Roul_no+x.Rank_no+x.Tour_no != 100):
    print("ERROR: Selection ratios do not add to 100")
    quit()

print(" ")
print("Starting Genetic Algorithm")
print("Seed: "+str(seed))
print(" ")

# If the Gen is 0, then call initialize, and write to csv.
if( x.Gen == 0):
    print("Initializing Gen 0")
    Initialize(F_Pop, Sections, Parameters)
    print("Initialization Complete")
    DataWrite(x.NPop, F_Pop, freq_coeff, freqVector, x.S_no, x.C_no, selected, x.Gen, seed)
    print("Data files written")

# If not, read in the data csv, sort the arrays, call the opperators, and write to csv.
else:
    print("Reading in Data")
    DataRead(Fitness, I_Pop, x.Gen)
    print("Sorting Data")
    Sort(Fitness, I_Pop, P_loc)
    print("Begining Evolution")
    Survival(x.S_no, I_Pop, F_Pop, Fitness, x.Elite_no, x.Roul_no, x.Rank_no, x.Tour_no, Pool, P_loc, selected, Sections, Parameters)
    print("Reproduction Complete")
    Crossover(x.NPop, x.S_no, x.C_no, I_Pop, F_Pop, Fitness, x.Elite_no, x.Roul_no, x.Rank_no, x.Tour_no, Pool, M_rate, Sigma, P_loc, selected, Sections, Parameters)
    print("Crossover and Mutation Complete")
    Immigration(x.S_no, x.C_no, x.I_no, F_Pop, Sections, Parameters)
    print("Immigration Complete")
    print("Evolution Complete")
    #print(selected)
    DataWrite(x.NPop, F_Pop, freq_coeff, freqVector, x.S_no, x.C_no, selected, x.Gen, seed)
    print("Data files writen")

# Print confirmation message
print(" ")
print("Genetic Algorithm ran successfully!")
print(" ")

##
##
## End of code
