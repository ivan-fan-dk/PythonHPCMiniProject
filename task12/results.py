import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read dataframes
df1 = pd.read_csv('results_cuda_0_1000.csv')
df2 = pd.read_csv('results_cuda_1000_2000.csv')
df3 = pd.read_csv('results_cuda_2000_3000.csv')
df4 = pd.read_csv('results_cuda_3000_4000.csv')
df5 = pd.read_csv('results_cuda_4000_4571.csv')

# Combine dataframes
df = pd.concat([df1, df2, df3, df4, df5], ignore_index=True)

# Plot distribution of the mean temperatures
plt.hist(df["mean_temp"], bins=100)
plt.xlabel("Mean Temperature")
plt.ylabel("Frequency")
plt.title("Distribution of Mean Temperatures")
plt.savefig("mean_temp_histogram_cuda.png", dpi=300, bbox_inches="tight")
plt.close()

# Print results
print(f"Average mean temperature: {np.mean(df['mean_temp'])}")
print(f"Average temperature standard deviation: {np.mean(df['std_temp'])}")
print(f"Buildings that had at least 50% of their area above 18ºC: {len(df[df['pct_above_18'] >= 50])}")
print(f"Buildings that had at least 50% of their area below 15ºC: {len(df[df['pct_below_15'] >= 50])}")

