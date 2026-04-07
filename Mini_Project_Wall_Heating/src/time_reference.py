import sys
from time import perf_counter

from utils import load_building_ids, load_padded_data, summary_stats
from reference import jacobi


def main(n_buildings=5, max_iter=20_000, atol=1e-4):
    building_ids = load_building_ids()[:n_buildings]

    t0 = perf_counter()

    for bid in building_ids:
        u0, interior_mask = load_padded_data(bid)
        u = jacobi(u0, interior_mask, max_iter=max_iter, atol=atol)
        stats = summary_stats(u, interior_mask)
        print(bid, stats)

    t1 = perf_counter()

    total_time = t1 - t0
    avg_time = total_time / n_buildings

    print(f"\nProcessed {n_buildings} buildings")
    print(f"Total time: {total_time:.3f} s")
    print(f"Average time per building: {avg_time:.3f} s")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        n_buildings = int(sys.argv[1])
    else:
        n_buildings = 5

    main(n_buildings=n_buildings)
