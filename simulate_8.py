from os.path import join
import sys

import numpy as np

from numba import cuda


def load_data(load_dir, bid):
    SIZE = 512
    u = np.zeros((SIZE + 2, SIZE + 2))
    u[1:-1, 1:-1] = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{bid}_interior.npy"))
    return u, interior_mask

@cuda.jit
def jacobi(u, interior_mask, u_out):
    i, j = cuda.grid(2)

    if i > 0 and i < u.shape[0] - 1 and j > 0 and j < u.shape[1] - 1:
        if interior_mask[i-1, j-1]:  # Adjust indices for interior_mask
            # Compute average of left, right, up and down neighbors, see eq. (1)
            u_out[i, j] = 0.25 * (u[i, j-1] + u[i, j+1] + u[i-1, j] + u[i+1, j])
        else:
            # Grid points on walls are fixed to their initial values and not updated [4]
            u_out[i, j] = u[i, j]

def jacobi_helper(u, interior_mask, max_iter):
    u_gpu = cuda.to_device(u)
    u_out_gpu = cuda.device_array_like(u_gpu)
    u_out_gpu[:] = u_gpu
    interior_mask_gpu = cuda.to_device(interior_mask)
    m, n = u.shape
    tpb_x, tpb_y = 16, 16
    tpb = (tpb_x, tpb_y)
    bpg_x = get_grid(m, tpb_x)
    bpg_y = get_grid(n, tpb_y)
    bpg = (bpg_x, bpg_y)
    for _ in range(max_iter):
        jacobi[bpg, tpb](u_gpu, interior_mask_gpu, u_out_gpu)
        cuda.synchronize()
        u_gpu, u_out_gpu = u_out_gpu, u_gpu  # Swap references for next iteration
    return u_gpu.copy_to_host()

def get_grid(n, tpb):
    return (n + (tpb - 1)) // tpb  # Blocks per grid

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

    # Run jacobi iterations for each floor plan
    MAX_ITER = 20_000
    ABS_TOL = 1e-4

    all_u = np.empty_like(all_u0)
    for i, (u0, interior_mask) in enumerate(zip(all_u0, all_interior_mask)):
        u = jacobi_helper(u0, interior_mask, MAX_ITER)
        all_u[i] = u

    # Print summary statistics in CSV format
    stat_keys = ['mean_temp', 'std_temp', 'pct_above_18', 'pct_below_15']
    print('building_id, ' + ', '.join(stat_keys))  # CSV header
    for bid, u, interior_mask in zip(building_ids, all_u, all_interior_mask):
        stats = summary_stats(u, interior_mask)
        print(f"{bid},", ", ".join(str(stats[k]) for k in stat_keys))