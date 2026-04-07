import os
import matplotlib.pyplot as plt
import numpy as np
from utils import load_building_ids, load_raw_data


def inspect_building(bid, out_dir="../results/figures"):
    domain, interior_mask = load_raw_data(bid)

    print(f"Building ID: {bid}")
    print(f"domain shape: {domain.shape}")
    print(f"interior_mask shape: {interior_mask.shape}")
    print(f"domain unique values: {np.unique(domain)}")
    print(f"interior unique values: {np.unique(interior_mask)}")
    print(f"number of interior points: {interior_mask.sum()}")

    os.makedirs(out_dir, exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    im0 = axes[0].imshow(domain)
    axes[0].set_title(f"Initial Temperature (Building {bid})")
    plt.colorbar(im0, ax=axes[0])

    im1 = axes[1].imshow(interior_mask, cmap="gray")
    axes[1].set_title(f"Interior Mask (Building {bid})")
    plt.colorbar(im1, ax=axes[1])

    plt.tight_layout()
    save_path = os.path.join(out_dir, f"{bid}_input.png")
    plt.savefig(save_path, dpi=200, bbox_inches="tight")
    plt.close()

    print(f"Saved figure to: {save_path}")


if __name__ == "__main__":
    building_ids = load_building_ids()

    for bid in building_ids[:3]:
        inspect_building(bid)

