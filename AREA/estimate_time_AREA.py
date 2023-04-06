# estimate the time it will take the test loop to run

runCount=0
secpergen = 5
generations = 50

for a in range(0,101,10): #RC
    for b in range(0,101,10): #RM
        for c in range(0,101,10):  #TC
          for d in range(0,101,10): #TM
            p = a+b+c+d
            if p==100:
              for h in range(0,11,1):
                runCount=runCount+1

batches = runCount/250
seconds = generations*secpergen*batches
minutes = int(seconds/60)
r_sec = seconds - (minutes*60)
hours = int(minutes/60)
r_min = minutes - (hours*60)

print("Jobs: "+str(runCount)+" in "+ str(batches)+" Batches") 
print("Hours:  "+ str(hours) + " Min: "+ str(r_min)+ " Sec: "+ str(r_sec))
