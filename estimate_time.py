"""Estimate the time it will take the test loop to run."""

# Establish constants
run_count = 0
population = 100
generations = 50

# loop over variables to find number of runs
for rank in range(60, 61, 1):
    for roulette in range(20, 21, 1):
        for tournament in range(20, 21, 1):
            if rank + roulette + tournament == population:
                for reproduction in range(0, 1, 1):
                    for crossover in range(96, 97, 1):
                        if reproduction + crossover <= population:
                            for mutation_rate in range(25, 26, 1):
                                for sigma in range(6, 7, 1):
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
