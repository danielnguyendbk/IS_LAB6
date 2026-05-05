import os

import pandas as pd

from src.config import DATA_FILES, DATA_RAW_DIR, MERGED_FILE


def load_single_file(file_path):
    print(f"[INFO] Loading: {file_path}")

    df = pd.read_csv(file_path, low_memory=False)

    # Chuẩn hóa tên cột
    df.columns = df.columns.str.strip()

    return df


def _load_merged_fallback(path, label):
    if os.path.exists(path):
        print(f"[INFO] Using {label}: {path}")
        return load_single_file(path)
    return None


def merge_raw_csvs(output_path=MERGED_FILE):
    raw_paths = [os.path.join(DATA_RAW_DIR, file) for file in DATA_FILES]
    if not all(os.path.exists(path) for path in raw_paths):
        return None

    dataframes = [load_single_file(path) for path in raw_paths]
    print("[INFO] Merging all files...")
    merged_df = pd.concat(dataframes, ignore_index=True)
    print(f"[INFO] Final shape: {merged_df.shape}")

    merged_df.to_csv(output_path, index=False)
    print(f"[INFO] Saved merged dataset to: {output_path}")
    return merged_df


def load_and_merge_data():
    raw_paths = [os.path.join(DATA_RAW_DIR, file) for file in DATA_FILES]
    if all(os.path.exists(path) for path in raw_paths):
        return merge_raw_csvs(MERGED_FILE)

    if os.path.exists(MERGED_FILE):
        print(
            "[INFO] Raw CIC-IDS2017 CSV files not found or incomplete. "
            "Using data/merged_dataset.csv instead."
        )
        merged_df = _load_merged_fallback(MERGED_FILE, "data/merged_dataset.csv")
        if merged_df is not None:
            return merged_df

    reports_merged = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "outputs",
        "reports",
        "merged_dataset.csv",
    )
    merged_df = _load_merged_fallback(
        reports_merged,
        "outputs/reports/merged_dataset.csv",
    )
    if merged_df is not None:
        return merged_df

    raise FileNotFoundError(
        "No dataset found. Please place the 8 raw CIC-IDS2017 CSV files in data/raw/, "
        "or provide data/merged_dataset.csv, or outputs/reports/merged_dataset.csv."
    )
