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

# ─────────────────────────────────────────────────────────────
# STEP: Real-time Alert System (Thành - Người 5)
# ─────────────────────────────────────────────────────────────
from src.realtime_alert import (
    save_best_model,
    load_best_model,
    run_realtime_demo
)

def run_realtime_phase(best_model, label_encoder, scaler):
    """
    Call this after the training phase is complete and you have:
      - best_model: the trained Random Forest classifier
      - label_encoder: the fitted LabelEncoder from balance.py
      - scaler: the fitted StandardScaler from pipeline_builder.py

    This function will:
      1. Save the model to models/best_model.pkl
      2. Load it back (to verify it works)
      3. Run a 5-flow real-time demo and write alerts to alerts.log
    """
    print("\n[STEP 6] Saving best model...")
    save_best_model(best_model, label_encoder, scaler)

    print("[STEP 6] Loading model back for verification...")
    model_bundle = load_best_model()

    print("[STEP 6] Running real-time demo...")
    run_realtime_demo(model_bundle, n_samples=5, write_to_log=True)

# NOTE TO TEAMMATES (Thái - Người 4):
# After you train Random Forest, call:
#   run_realtime_phase(rf_model, label_encoder, scaler)
# from your section in main.py, OR just call it directly below
# if main.py runs everything sequentially.
