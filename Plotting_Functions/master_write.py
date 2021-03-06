# read in fitness score data and save to file

import csv
import numpy as np

with open('Master_file.txt', "w") as F1:
    F1.write("Master Files \n")
    F1.write("\n")
    Maxes = []
    runnames = []
    for d in range(0,10,3):
        for e in range(32,51,6):
            de = d + e
            if (de < 50):
                for f in range(0,11,5):
                    for g in range(1,6,1):
                        highs = []
                        averages = []
                        run_name = str(d) + '_' + str(e) + '_' + str(f) + '_' + str(g)
                        F1.write(run_name + '\n')
                        for h in range(1,6,1):
                            scores=[]
                            with open(run_name + '_' + str(h) + '_50_fitnessScores.csv') as F2:
                                txt_read = csv.reader(F2, delimiter =",")
                                for i, row in enumerate(txt_read):
                                    if i>2:
                                        scores.append(float(row[0]))
                                highs.append(max(scores))
                                averages.append(sum(scores)/len(scores))
                            F2.close()
                            F1.write("      Run:"+str(h)+"      High Score:"+str(max(scores))+"      Average Score:"+str(sum(scores)/len(scores))+"\n")
                        Maxes.append(sum(highs)/len(highs))
                        runnames.append(run_name)
                        F1.write("   Overall:   Max Score: "+str(max(highs))+"   Average high Score: "+str(sum(highs)/len(highs))+"   Total Average: "+str(sum(averages)/len(averages))+'\n')
                        F1.write("\n")
    F1.write("Maxiumum ave: "+str(max(Maxes)) + " Run: " + str(runnames[Maxes.index(max(Maxes))])) 
F1.close()
