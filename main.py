from src.data_loader import load_and_merge_data, save_merged_data


def main():
    print("===== IDS PIPELINE START =====")

    # Step 1: Load + Merge full dataset
    df = load_and_merge_data()

    # Step 2: (OPTIONAL) Save full dataset
    save_merged_data(df)

    print("===== DATA READY FOR NEXT MODULES =====")


if __name__ == "__main__":
    main()