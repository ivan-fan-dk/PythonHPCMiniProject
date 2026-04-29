# %%
from os.path import join
import numpy as np
import matplotlib.pyplot as plt

def load_data(load_dir, bid):
    SIZE = 512
    u = np.zeros((SIZE + 2, SIZE + 2))
    u[1:-1, 1:-1] = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{bid}_interior.npy"))
    return u, interior_mask

# %% [markdown]
# # Task 1

# %%
# Load data
LOAD_DIR = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'
with open(join(LOAD_DIR, 'building_ids.txt'), 'r') as f:
    building_ids = f.read().splitlines()
N = 2
building_ids = building_ids[:N]

# Load floor plans
all_u0 = np.empty((N, 514, 514))
all_interior_mask = np.empty((N, 512, 512), dtype='bool')
for i, bid in enumerate(building_ids):
    u0, interior_mask = load_data(LOAD_DIR, bid)
    all_u0[i] = u0
    all_interior_mask[i] = interior_mask

fig, ax = plt.subplots(N, 2, figsize=(10, 9), squeeze=False)
for i in range(N):
    ax[i, 0].imshow(all_u0[i])
    ax[i, 0].set_title(f'Initial Temperature on floor plan {i+1}')
    ax[i, 1].imshow(all_interior_mask[i])
    ax[i, 1].set_title(f'Interior Mask on floor plan {i+1}')