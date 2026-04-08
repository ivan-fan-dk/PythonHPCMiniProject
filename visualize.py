from os.path import join
import sys
import numpy as np
import matplotlib.pyplot as plt

def load_data(load_dir, bid):
    SIZE = 512
    u = np.zeros((SIZE + 2, SIZE + 2))
    u[1:-1, 1:-1] = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{bid}_interior.npy"))
    return u, interior_mask

# Load data
LOAD_DIR = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'
with open(join(LOAD_DIR, 'building_ids.txt'), 'r') as f:
    building_ids = f.read().splitlines()

if len(sys.argv) < 2:
     N = 1
else:
    N = int(sys.argv[1])
building_ids = building_ids[:N]

# Load floor plans
all_u0 = np.empty((N, 514, 514))
all_interior_mask = np.empty((N, 512, 512), dtype='bool')
for i, bid in enumerate(building_ids):
    u0, interior_mask = load_data(LOAD_DIR, bid)
    all_u0[i] = u0
    all_interior_mask[i] = interior_mask

# Plot first N images
fig, axes = plt.subplots(N, 2, figsize=(10, 4 * N))
for i in range(N):
    # Plot u0 (full grid with boundary)
    ax = axes[i, 0] if N > 1 else axes[0]
    im0 = ax.imshow(all_u0[i], cmap='viridis')
    ax.set_title(f"all_u0[{i}]")
    ax.axis("off")
    fig.colorbar(im0, ax=ax)
    # Plot interior mask
    ax = axes[i, 1] if N > 1 else axes[1]
    im1 = ax.imshow(all_interior_mask[i], cmap='gray')
    ax.set_title(f"all_interior_mask[{i}]")
    ax.axis("off")
plt.tight_layout()

# Save plot
output_path = 'FirstVisualization.png'
plt.savefig(output_path, dpi=300, bbox_inches="tight")



    

    