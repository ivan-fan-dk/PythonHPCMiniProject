from os.path import join
import numpy as np


LOAD_DIR = "/dtu/projects/02613_2025/data/modified_swiss_dwellings"


def load_building_ids(load_dir=LOAD_DIR):
    with open(join(load_dir, "building_ids.txt"), "r") as f:
        return f.read().splitlines()


def load_raw_data(bid, load_dir=LOAD_DIR):
    domain = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{bid}_interior.npy"))
    return domain, interior_mask


def load_padded_data(bid, load_dir=LOAD_DIR):
    size = 512
    u = np.zeros((size + 2, size + 2), dtype=np.float64)
    domain = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{bid}_interior.npy"))

    u[1:-1, 1:-1] = domain
    return u, interior_mask


def summary_stats(u, interior_mask):
    u_interior = u[1:-1, 1:-1][interior_mask]

    mean_temp = u_interior.mean()
    std_temp = u_interior.std()
    pct_above_18 = np.sum(u_interior > 18) / u_interior.size * 100
    pct_below_15 = np.sum(u_interior < 15) / u_interior.size * 100

    return {
        "mean_temp": mean_temp,
        "std_temp": std_temp,
        "pct_above_18": pct_above_18,
        "pct_below_15": pct_below_15,
    }
