import os
import matplotlib.pyplot as plt

from utils import load_building_ids, load_raw_data, load_padded_data
from reference import jacobi

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def plot_combined_results(building_ids, max_iter=20_000, atol=1e-4, out_dir=None):
    if out_dir is None:
        out_dir = os.path.join(BASE_DIR, "results", "figures")
    os.makedirs(out_dir, exist_ok=True)

    n = len(building_ids)

    fig, axes = plt.subplots(n, 3, figsize=(14, 5 * n))

    if n == 1:
        axes = [axes]

    # Hold styr på temperatur plots til fælles colorbar
    temp_images = []

    for row, bid in enumerate(building_ids):
        domain, interior_mask_raw = load_raw_data(bid)
        u0, interior_mask = load_padded_data(bid)
        u, _ = jacobi(u0, interior_mask, max_iter=max_iter, atol=atol, return_iter=True)

        # --- Initial temperature ---
        im0 = axes[row][0].imshow(domain, vmin=0, vmax=25, cmap="viridis")
        axes[row][0].set_title(f"Initial Temperature (Floor {row+1})")

        # --- Interior mask ---
        im1 = axes[row][1].imshow(interior_mask_raw, cmap="gray", vmin=0, vmax=1)
        axes[row][1].set_title(f"Interior Mask (Floor {row+1})")

        # --- Final temperature ---
        im2 = axes[row][2].imshow(u[1:-1, 1:-1], vmin=0, vmax=25, cmap="viridis")
        axes[row][2].set_title(f"Final Temperature (Floor {row+1})")

        temp_images.append(im2)

        for col in range(3):
            axes[row][col].set_xticks([0, 250, 500])
            axes[row][col].set_yticks([0, 250, 500])

    # --- Fælles colorbar for temperatur ---
    cbar = fig.colorbar(temp_images[0], ax=axes[:, :], fraction=0.02, pad=0.04)
    cbar.set_label("Temperature (°C)")

    # --- Colorbar til mask ---
    cbar_mask = fig.colorbar(im1, ax=axes[:, 1], fraction=0.02, pad=0.02)
    cbar_mask.set_label("Interior (1=True)")

    plt.subplots_adjust(wspace=0.3, hspace=0.4)

    save_path = os.path.join(out_dir, "combined_results.png")
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Saved combined figure to: {save_path}")


if __name__ == "__main__":
    building_ids = load_building_ids()[:2]
    plot_combined_results(building_ids)