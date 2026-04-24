# main.py

from src.data_loader import load_and_merge_data, save_merged_data


def main():
    print("===== IDS PIPELINE START =====")

    # Step 1: Load + Merge
    df = load_and_merge_data()

    # Step 2: Save merged dataset
    save_merged_data(df)

    print("===== DONE =====")


if __name__ == "__main__":
    main()