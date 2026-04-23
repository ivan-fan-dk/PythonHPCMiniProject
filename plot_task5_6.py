# %% Plot static and dynamic runtime
import numpy as np
import matplotlib.pyplot as plt
static_scheduling = np.array([
        1529.822,  843.585,  586.013,  428.083,  402.75 ,  353.868,
        299.354,  335.367,  282.723,  260.041,  256.774,  237.326,
        220.128,  220.664,  193.15 ,  192.01 ,  197.618,  195.37 ,
        202.073,  194.706,  194.252,  196.658,  191.72 ,  197.733])
dynamic_scheduling = np.array([1522.824,  811.824,  578.186,  446.176,  353.923,  313.41 ,
        265.141,  241.773,  228.108,  207.054,  200.664,  183.573,
        188.302,  184.884,  183.896,  178.104,  180.962,  183.156,
        186.795,  189.291,  187.012,  191.416,  192.546,  193.153])
x_lim = np.arange(1, 25)
plt.figure(figsize=(10, 6))
plt.plot(x_lim, static_scheduling, 'o-', label='static')
plt.plot(x_lim, dynamic_scheduling, 'o-', label='dynamic')
plt.xlabel('num_workers')
plt.ylabel('Time')
plt.title('Time Comparison of Static vs Dynamic')
plt.legend()
plt.xticks(x_lim)
plt.grid(True, ls="--")
plt.tight_layout()
plt.show()

# %% Plot static and dynamic speedup and Amdahl's Law
static_speedup = static_scheduling[0] / static_scheduling
dynamic_speedup = dynamic_scheduling[0] / dynamic_scheduling
p_static, p_dynamic = np.mean((1/static_speedup[1:] - 1) * (x_lim[1:]/(1-x_lim[1:]))), np.mean((1/dynamic_speedup[1:] - 1) * (x_lim[1:]/(1-x_lim[1:])))
plt.figure(figsize=(10, 6))
plt.plot(x_lim, static_speedup, 'o-', label='static')
plt.plot(x_lim, dynamic_speedup, 'o-', label='dynamic')
plt.plot(x_lim, 1/(1 - p_static + p_static/x_lim), 'k--', label=f'static,  Amdahl\'s Law (f={p_static:.2f})')
plt.plot(x_lim, 1/(1 - p_dynamic + p_dynamic/x_lim), 'r--', label=f'dynamic, Amdahl\'s Law (f={p_dynamic:.2f})')
plt.xlabel('num_workers')
plt.ylabel('Speedup')
plt.title('Speedup of Static vs Dynamic')
plt.legend()
plt.xticks(x_lim)
plt.grid(True, ls="--")
plt.tight_layout()
plt.show()

# %% Plot only static scheduling
static_speedup = static_scheduling[0] / static_scheduling
# dynamic_speedup = dynamic_scheduling[0] / dynamic_scheduling
p_static, p_dynamic = np.mean((1/static_speedup[1:] - 1) * (x_lim[1:]/(1-x_lim[1:]))), np.mean((1/dynamic_speedup[1:] - 1) * (x_lim[1:]/(1-x_lim[1:])))
plt.figure(figsize=(10, 6))
plt.plot(x_lim, static_speedup, 'o-', label='static')
# plt.plot(x_lim, dynamic_speedup, 'o-', label='dynamic')
plt.plot(x_lim, 1/(1 - p_static + p_static/x_lim), 'k--', label=f'static,  Amdahl\'s Law (f={p_static:.2f})')
# plt.plot(x_lim, 1/(1 - p_dynamic + p_dynamic/x_lim), 'r--', label=f'dynamic, Amdahl\'s Law (f={p_dynamic:.2f})')
plt.xlabel('num_workers')
plt.ylabel('Speedup')
plt.title('Speedup for static scheduling')
plt.legend()
plt.xticks(x_lim)
plt.grid(True, ls="--")
plt.tight_layout()
plt.show()
