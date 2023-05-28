# Estimate the time it will take the test loop to run.
# Also, print amount of runs to be done.

sigma = 5
runCount = 0

for a in range(2, 3, 2):
    for b in range(2, 3, 2):
        for c in range(6, 7, 2):
            r = a+b+c
            if r == 10:
                for d in range(0, 21, 4):
                    for e in range(80, 101, 4):
                        de = d + e
                        for f in range(10, 21, 5):
                            if f != 0:
                                sigma = 7
                            if f == 0:
                                sigma = 3
                            for g in range(3, sigma+1, 1):
                                for h in range(1, 10, 1):
                                    runCount = runCount+1

batches = runCount/250
seconds = 60*10*batches
minutes = int(seconds/60)
r_sec = seconds - (minutes*60)
hours = int(minutes/60)
r_min = minutes - (hours*60)

print("Jobs: " + str(runCount) + " in " + str(batches) + " Batches")
print("Hours:  " + str(hours) + " Min: " + str(r_min) + " Sec: " + str(r_sec))
