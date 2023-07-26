"""Estimate the time it will take the test loop to run."""

# Establish constants
run_count = 0
population = 100
generations = 50

# loop over variables to find number of runs
for rank in range(0, 101, 10):
    for roulette in range(0, 101, 10):
        for tournament in range(0, 101, 10):
            if rank + roulette + tournament == population:
                for reproduction in range(0, 17, 4):
                    for crossover in range(72, 100, 4):
                        for mutation in range(4, 17, 4):
                            operators = reproduction + crossover + mutation
                            if operators <= population:
                                for sigma in range(10, 11, 1):
                                    for test in range(1, 11, 1):
                                        run_count = run_count + 1

# solve for time
# assume each generation takes 3 seconds
batches = int(run_count / 250) + 1
seconds = (3*generations) * batches
minutes = int(seconds / 60)
r_sec = seconds - (minutes * 60)
hours = int(minutes / 60)
r_min = minutes - (hours * 60)

print(f"Jobs: {run_count} in {batches} Batches")
print(f"Hours: {hours} Min: {r_min} Sec: {r_sec}")
