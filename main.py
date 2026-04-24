# main.py

from src.data_loader import load_and_merge_data, save_merged_data


def main():
    print("===== IDS PIPELINE START =====")

    # Step 1: Load + Merge
    df = load_and_merge_data()

    # Step 2: Save (chọn mode an toàn)
    save_merged_data(df, mode="sample")  #KHÔNG dùng "full"

    print("===== DONE =====")


if __name__ == "__main__":
    main()