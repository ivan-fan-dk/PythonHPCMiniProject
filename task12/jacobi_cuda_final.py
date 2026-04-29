from os.path import join
import sys
import numpy as np
from numba import cuda
import matplotlib.pyplot as plt
import time
import csv

def load_data(load_dir, bid):
    SIZE = 512
    u = np.zeros((SIZE + 2, SIZE + 2))
    u[1:-1, 1:-1] = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{bid}_interior.npy"))
    return u, interior_mask

@cuda.jit
def jacobi_kernel(u_old, u_new, interior_mask):
    nx, ny = u_old.shape
    i, j = cuda.grid(2)
    # Loop through interior
    if (0 < i and i < nx-1 and 0 < j and j < ny-1): # Interior mask shape is (nx-2,ny-2)
        if interior_mask[i-1, j-1]: # Interior mask shape is (nx-2,ny-2)
            # Compute neighbour average
            avg = 0.25 * (u_old[i-1, j] + u_old[i, j+1] + u_old[i+1, j] + u_old[i, j-1])
            # Update u
            u_new[i, j] = avg
        else:
            u_new[i, j] = u_old[i, j]

def helper(u_old, u_new, interior_mask):
    # Launches kernel 20_000 times
    tpb = 16, 16
    bpg = ((u_old.shape[0] + tpb[0] - 1) // tpb[0], 
           (u_old.shape[1] + tpb[1] - 1) // tpb[1])
    for _ in range(20000):
        jacobi_kernel[bpg, tpb](u_old, u_new, interior_mask)
        u_old, u_new = u_new, u_old
    return u_old

def summary_stats(u, interior_mask):
    u_interior = u[1:-1, 1:-1][interior_mask]
    mean_temp = u_interior.mean()
    std_temp = u_interior.std()
    pct_above_18 = np.sum(u_interior > 18) / u_interior.size * 100
    pct_below_15 = np.sum(u_interior < 15) / u_interior.size * 100
    return {
        'mean_temp': mean_temp,
        'std_temp': std_temp,
        'pct_above_18': pct_above_18,
        'pct_below_15': pct_below_15,
    }

if __name__ == '__main__':
    # Load data
    LOAD_DIR = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'
    with open(join(LOAD_DIR, 'building_ids.txt'), 'r') as f:
        building_ids = f.read().splitlines()
    
    N1, N2 = [int(n) for n in sys.argv[1:]]
    building_ids = building_ids[N1:N2]
    N = len(building_ids)

    # Load floor plans
    all_u0 = np.empty((N, 514, 514))
    all_interior_mask = np.empty((N, 512, 512), dtype='bool')
    for i, bid in enumerate(building_ids):
        u0, interior_mask = load_data(LOAD_DIR, bid)
        all_u0[i] = u0
        all_interior_mask[i] = interior_mask

    # Launch kernel once
    jacobi_kernel[((512+16-1)//16,(512+16-1)//16), (16,16)](np.empty((514,514)), np.empty((514,514)), np.empty((512, 512)))

    # Run jacobi iterations for each floor plan
    t = time.time()
    all_u = np.empty_like(all_u0)
    for i, (u0, interior_mask) in enumerate(zip(all_u0, all_interior_mask)):
        # Manual memory transfer
        d_u0 = cuda.to_device(u0) 
        d_interior_mask = cuda.to_device(interior_mask)
        d_u_new = cuda.device_array_like(d_u0)
        # Run jacobi
        d_u = helper(d_u0, d_u_new, d_interior_mask)
        cuda.synchronize()   
        u = d_u.copy_to_host()
        # Update solution array
        all_u[i] = u
    print(f"Time: {time.time()-t} sec\n")

    # Print summary statistics in CSV format
    #stat_keys = ['mean_temp', 'std_temp', 'pct_above_18', 'pct_below_15']
    #print('building_id, ' + ', '.join(stat_keys))  # CSV header
    #for bid, u, interior_mask in zip(building_ids, all_u, all_interior_mask):
    #    stats = summary_stats(u, interior_mask)
    #    print(f"{bid},", ", ".join(str(stats[k]) for k in stat_keys))
    
    # Save summary statistics in CSV
    stat_keys = ['mean_temp', 'std_temp', 'pct_above_18', 'pct_below_15']
    out_file = f'results_cuda_{N1}_{N2}.csv'
    with open(out_file, mode="w", newline="") as f:
        writer = csv.writer(f)
        f.flush()
        # Header
        writer.writerow(["building_id"] + stat_keys)
        # Data rows
        for bid, u, interior_mask in zip(building_ids, all_u, all_interior_mask):
            stats = summary_stats(u, interior_mask)
            writer.writerow([bid] + [stats[k] for k in stat_keys])
            f.flush()
            print(f"Results for {bid} saved...")
    print(f"All results saved to {out_file}")


    # Plot first 3 images
    #fig, axes = plt.subplots(3, 3, figsize=(10, 4 * 3))
    #for i in range(3):
    #    # Plot interior mask
    #    ax = axes[i, 0]
    #    im1 = ax.imshow(all_interior_mask[i], cmap='gray')
    #    ax.set_title(f"all_interior_mask[{i}]")
    #    ax.axis("off")
    #    # Plot u0 (full grid with boundary)
    #    ax = axes[i, 1]
    #    im0 = ax.imshow(all_u0[i], cmap='viridis')
    #    ax.set_title(f"all_u0[{i}]")
    #    ax.axis("off")
    #    fig.colorbar(im0, ax=ax)
    #    # Plot u (full solution grid)
    #    ax = axes[i, 2]
    #    im1 = ax.imshow(all_u[i], cmap='viridis')
    #    ax.set_title(f"all_u[{i}]")
    #    ax.axis("off")
    #    fig.colorbar(im1, ax=ax)
    #plt.tight_layout()

    # Save plot
    #output_path = 'visualizaion_cuda.png'
    #plt.savefig(output_path, dpi=300, bbox_inches="tight")