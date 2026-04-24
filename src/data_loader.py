# src/data_loader.py

import pandas as pd
import os
from src.config import DATA_DIR, DATA_FILES, MERGED_FILE


def load_single_file(file_path):
    print(f"[INFO] Loading: {file_path}")

    df = pd.read_csv(file_path, low_memory=False)

    # Strip column names
    df.columns = df.columns.str.strip()

    return df


def load_and_merge_data():
    dataframes = []

    for file in DATA_FILES:
        file_path = os.path.join(DATA_DIR, file)

        if not os.path.exists(file_path):
            print(f"[WARNING] File not found: {file_path}")
            continue

        df = load_single_file(file_path)
        dataframes.append(df)

    print("[INFO] Merging all files...")
    merged_df = pd.concat(dataframes, ignore_index=True)

    print(f"[INFO] Final shape: {merged_df.shape}")

    return merged_df



def save_merged_data(df, mode="sample"):

    if mode == "sample":
        sample_path = MERGED_FILE.replace(".csv", "_sample.csv")
        df.sample(n=min(10000, len(df))).to_csv(sample_path, index=False)
        print(f"[INFO] Saved SAMPLE data to {sample_path}")

    elif mode == "full":
        df.to_csv(MERGED_FILE, index=False)
        print(f"[INFO] Saved FULL data to {MERGED_FILE}")

    elif mode == "parquet":
        parquet_path = MERGED_FILE.replace(".csv", ".parquet")
        df.to_parquet(parquet_path)
        print(f"[INFO] Saved PARQUET data to {parquet_path}")

    else:
        print("[WARNING] Unknown save mode. Skipping save.")