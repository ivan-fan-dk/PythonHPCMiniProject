import sys
import time
import multiprocessing as mp

from utils import load_building_ids, load_padded_data, summary_stats
from reference import jacobi


def process_building(bid, max_iter=20_000, atol=1e-4):
    u0, interior_mask = load_padded_data(bid)
    u = jacobi(u0, interior_mask, max_iter=max_iter, atol=atol)
    stats = summary_stats(u, interior_mask)
    return bid, stats


def worker_chunk(bids, max_iter=20_000, atol=1e-4):
    results = []
    for bid in bids:
        results.append(process_building(bid, max_iter=max_iter, atol=atol))
    return results


def chunk_list(lst, n_chunks):
    """Split list into n_chunks as evenly as possible."""
    k, m = divmod(len(lst), n_chunks)
    return [
        lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)]
        for i in range(n_chunks)
    ]


def main():
    if len(sys.argv) < 3:
        print("Usage: python parallel_static.py <N> <n_workers>")
        sys.exit(1)

    N = int(sys.argv[1])
    n_workers = int(sys.argv[2])

    building_ids = load_building_ids()[:N]
    chunks = chunk_list(building_ids, n_workers)

    t0 = time.perf_counter()

    with mp.Pool(processes=n_workers) as pool:
        chunk_results = pool.map(worker_chunk, chunks)

    t1 = time.perf_counter()

    # flatten results
    results = [item for chunk in chunk_results for item in chunk]

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