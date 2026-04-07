import sys
import time
import multiprocessing as mp

from utils import load_building_ids, load_padded_data, summary_stats
from reference import jacobi


def process_building(args):
    bid, max_iter, atol = args
    u0, interior_mask = load_padded_data(bid)
    u = jacobi(u0, interior_mask, max_iter=max_iter, atol=atol)
    stats = summary_stats(u, interior_mask)
    return bid, stats


def main():
    if len(sys.argv) < 3:
        print("Usage: python parallel_dynamic.py <N> <n_workers>")
        sys.exit(1)

    N = int(sys.argv[1])
    n_workers = int(sys.argv[2])

    max_iter = 20_000
    atol = 1e-4

    building_ids = load_building_ids()[:N]
    tasks = [(bid, max_iter, atol) for bid in building_ids]

    t0 = time.perf_counter()

    with mp.Pool(processes=n_workers) as pool:
        results = list(pool.imap_unordered(process_building, tasks, chunksize=1))

    t1 = time.perf_counter()

    # sort results by building id for clean output
    results.sort(key=lambda x: x[0])

    stat_keys = ['mean_temp', 'std_temp', 'pct_above_18', 'pct_below_15']
    print("building_id," + ",".join(stat_keys))
    for bid, stats in results:
        print(f"{bid}," + ",".join(str(stats[k]) for k in stat_keys))

    total_time = t1 - t0
    print(f"\nProcessed {N} buildings with {n_workers} workers")
    print(f"Total time: {total_time:.3f} s")
    print(f"Average time per building: {total_time / N:.3f} s")


if __name__ == "__main__":
    main()