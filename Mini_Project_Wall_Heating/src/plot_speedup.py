import matplotlib.pyplot as plt

workers = [1, 2, 4, 6, 8]
times = [644.857, 360.628, 183.896, 151.165, 129.523]

T1 = times[0]
speedup = [T1 / t for t in times]
ideal = workers

plt.figure(figsize=(6, 4))
plt.plot(workers, speedup, marker='o', label="Measured speedup")
plt.plot(workers, ideal, linestyle='--', label="Ideal speedup")

plt.xlabel("Number of workers")
plt.ylabel("Speedup")
plt.title("Speedup as a Function of Number of Workers")
plt.xticks(workers)
plt.grid(True)
plt.legend()

plt.savefig("results/figures/task5a_speedup.png", dpi=300, bbox_inches="tight")
plt.show()