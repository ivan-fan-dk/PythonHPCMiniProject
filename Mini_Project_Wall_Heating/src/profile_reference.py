from utils import load_building_ids, load_padded_data
from reference import jacobi

def main():
    building_ids = load_building_ids()
    bid = building_ids[0]   # bare én bygning til profiling
    u0, interior_mask = load_padded_data(bid)

    jacobi(u0, interior_mask, max_iter=20_000, atol=1e-4)


if __name__ == "__main__":
    main()
