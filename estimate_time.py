# estimate the time it will take the test loop to run

seconds = 0
sigma= 5

for a in range(2,3,2):
    for b in range(2,3,2):
        for c in range(6,7,2):
            r = a+b+c
            if r==10:
                for d in range(0,1,6):
                    for e in range(70,101,6):
                        de=d+e
                        for f in range(5,16,5):
                            if f != 0:
                                sigma=5
                            if f == 0:
                                sigma=1
                            for g in range(1,sigma+1,1):
                                for h in range(1,6,1):
                                    for i in range(0,51):
                                        seconds=seconds+1

minutes = int(seconds/60)
r_sec = seconds - (minutes*60)
hours = int(minutes/60)
r_min = minutes - (hours*60)

print("Hours:  "+ str(hours) + " Min: "+ str(r_min) + " Sec: " + str(r_sec))
                                
