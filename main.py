import argparse
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
  sys.path.insert(0, PROJECT_ROOT)

if "src" in sys.modules:
  del sys.modules["src"]

from sklearn.model_selection import train_test_split

from src.data_loader import load_and_merge_data
from src.preprocessing import run_preprocessing
from src.eda import run_eda
from src.train_models import train_and_evaluate_models
from validate_dataset import validate_dataframe


DEFAULT_SAMPLE_SIZE = 20000
QUICK_SAMPLE_SIZE = 10000
RANDOM_STATE = 42


def _sample_dataframe(df, sample_size, random_state=RANDOM_STATE):
  if sample_size is None or sample_size <= 0:
    return df
  if sample_size >= len(df):
    print(f"[INFO] sample_size >= dataset size ({len(df)}). Using full data.")
    return df

  stratify = df["Label"] if "Label" in df.columns else None
  _, df_sampled = train_test_split(
    df,
    test_size=sample_size,
    stratify=stratify,
    random_state=random_state,
  )
  return df_sampled


def _ensure_output_dirs():
  os.makedirs("outputs/reports", exist_ok=True)
  os.makedirs("outputs/figures", exist_ok=True)
  os.makedirs("models", exist_ok=True)


def main():
  parser = argparse.ArgumentParser(
    description="NIDS pipeline with sampled training (CIC-IDS2017)."
  )
  parser.add_argument(
    "--quick",
    action="store_true",
    help=f"Use quick mode with sample size {QUICK_SAMPLE_SIZE}.",
  )
  parser.add_argument(
    "--sample-size",
    type=int,
    default=None,
    help="Number of samples to use for training/evaluation.",
  )

  args = parser.parse_args()

  sample_size = args.sample_size
  if args.quick and sample_size is None:
    sample_size = QUICK_SAMPLE_SIZE
  if sample_size is None:
    sample_size = DEFAULT_SAMPLE_SIZE

  print("===== IDS PIPELINE START =====")
  print(f"[INFO] Using sample size: {sample_size} (random_state={RANDOM_STATE})")

  _ensure_output_dirs()

  # Step 1: Load + Merge full dataset
  try:
    df = load_and_merge_data()
  except FileNotFoundError as error:
    print(f"[ERROR] {error}")
    print("[INFO] Please add the CIC-IDS2017 CSV files to data/ and retry.")
    return

  print("[DEBUG] Protocol before preprocessing:", "Protocol" in df.columns)

  # Step 2: Preprocess
  df = run_preprocessing(df)

  print("[DEBUG] Protocol after preprocessing:", "Protocol" in df.columns)

  if not validate_dataframe(df, source_label="preprocessed dataset"):
    print("[ERROR] Dataset validation failed. Please fix the missing columns.")
    return

  # Step 3: Sample for quick/reproduce mode
  df_sampled = _sample_dataframe(df, sample_size)

  # Step 4: Save preprocessed sampled data for reference
  df_sampled.to_csv("outputs/reports/preprocessed_dataset.csv", index=False)

  # Step 5: EDA (on sampled data)
  run_eda(df_sampled)

  # Step 6: Train + Evaluate models (on sampled data)
  train_and_evaluate_models(df_sampled, random_state=RANDOM_STATE)

  print("===== IDS PIPELINE COMPLETE =====")


if __name__ == "__main__":
  main()
