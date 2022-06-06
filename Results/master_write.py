# read in fitness score data and save to file

import csv
import numpy as np

with open('Master_file.txt', "w") as F1:
    F1.write("Master Files \n")
    F1.write("\n")
    Maxes = []
    runnames = []
    for a in range(36,42,2):
        for b in range(5,11,1):
            for c in range(1,6,1):
                highs = []
                averages = []
                run_name = str(a) + '_' + str(b) + '_' + str(c)
                F1.write(run_name + '\n')
                for d in range(1,11,1):
                    scores=[]
                    with open(run_name + '_' + str(d) + '_30_fitnessScores.csv') as F2:
                        txt_read = csv.reader(F2, delimiter =",")
                        for i, row in enumerate(txt_read):
                            if i>2:
                                scores.append(float(row[0]))
                        highs.append(max(scores))
                        averages.append(sum(scores)/len(scores))
                    F2.close()
                    F1.write("      Run:"+str(d)+"      High Score:"+str(max(scores))+"      Average Score:"+str(sum(scores)/len(scores))+"\n")
                Maxes.append(sum(highs)/len(highs))
                runnames.append(run_name)
                F1.write("   Overall:   Max Score: "+str(max(highs))+"   Average high Score: "+str(sum(highs)/len(highs))+"   Total Average: "+str(sum(averages)/len(averages))+'\n')
                F1.write("\n")
    F1.write("Maxiumum ave: "+str(max(Maxes)) + " Run: " + str(runnames[Maxes.index(max(Maxes))])) 
F1.close()
