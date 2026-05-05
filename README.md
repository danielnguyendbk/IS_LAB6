# Network Intrusion Detection System (NIDS) using Machine Learning GROUP15

## Project overview

This project implements a real-time Network Intrusion Detection System (NIDS) using machine learning on the CIC-IDS2017 dataset. The system:

- Analyzes network traffic data
- Detects malicious activities (DoS, DDoS, PortScan, Web Attacks, etc.)
- Generates real-time alerts for suspicious traffic

## Dataset

- Dataset: CIC-IDS2017
- Source: https://www.kaggle.com/datasets/chethuhn/network-intrusion-dataset
- Features: 79 columns (78 numerical + 1 label)
- Classes: BENIGN + multiple attack types
- Challenge: Highly imbalanced dataset

Note: The dataset is not included in this repository due to size.
Because CIC-IDS2017 is large, this project trains and evaluates on a sampled subset
for quick and reproducible runs on lab machines.

Feature note:
- The Lab 6 spec lists 18 core features including `Protocol`.
- The CIC-IDS2017 CSV version used in this project does not include `Protocol`.
- We do not fabricate `Protocol`; the pipeline falls back to the remaining 17 core features.

### How to use the dataset

1. Download the dataset from the link above
2. Extract all CSV files
3. Place them into the `data/raw/` folder:

```text
data/raw/
├── Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv
├── Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv
├── Friday-WorkingHours-Morning.pcap_ISCX.csv
├── Monday-WorkingHours.pcap_ISCX.csv
├── Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv
├── Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv
├── Tuesday-WorkingHours.pcap_ISCX.csv
└── Wednesday-workingHours.pcap_ISCX.csv
```

## Project structure

```text
Network-Intrusion-DetectionML/
│
├── data/                  # Dataset files (ignored in Git)
│   ├── raw/               # 8 CSV files from CIC-IDS2017
│   └── merged_dataset.csv # Optional merged dataset fallback
├── models/                # Saved models (.pkl)
├── outputs/               # Results, plots, reports
│   ├── figures/
│   └── reports/
├── src/
│   ├── config.py          # Configuration paths and constants
│   ├── data_loader.py     # Load and merge CIC-IDS2017 CSV files
│   ├── preprocessing.py   # Clean NaN/inf values, remove duplicates, optimize data
│   ├── eda.py             # Attack distribution plot and correlation heatmap
│   ├── balance.py         # LabelEncoder, SMOTE, RandomUnderSampler
│   ├── features.py        # Select core features
│   ├── pipeline_builder.py# Build imblearn preprocessing pipeline
│   ├── train_models.py    # Train ML models
│   ├── evaluate.py        # Reports and confusion matrices
│   └── realtime_alert.py  # Save/load model and generate alerts
│
├── main.py                # Main pipeline
├── requirements.txt
├── README.md
└── alerts.log
```

## Architecture

```text
Raw CSV files (8 files)
       ↓
       data_loader.py   -> Load raw CSVs or use merged dataset fallback
       ↓
preprocessing.py   -> Clean, handle NaN/inf, deduplicate, downcast
       ↓
     eda.py        -> Attack distribution plot, correlation heatmap
       ↓
   balance.py      -> LabelEncode -> SMOTE -> RandomUnderSampler
       ↓
   features.py     -> Select core features
       ↓
pipeline_builder.py -> Assemble imblearn Pipeline
       ↓
 train_models.py   -> Train 5 ML models (sampled subset)
       ↓
  evaluate.py      -> Classification reports, confusion matrices
       ↓
realtime_alert.py  -> Save .pkl -> Load -> Real-time prediction -> Alert
```

## Installation

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

Quick checks (no training):

```bash
python quick_test.py
```

Train/evaluate on a sampled subset:

```bash
python main.py --quick
python main.py --sample-size 10000
```

If you run without arguments, the pipeline still uses a default sampled subset
and prints the sample size being used.

### Outputs

- Figures: `outputs/figures/`
- Evaluation reports: `outputs/reports/`
- Preprocessed dataset (sampled): `outputs/reports/preprocessed_dataset.csv`
- Model comparison: `outputs/reports/model_comparison.csv`
- Saved model bundle: `models/best_model.pkl`
- Alert log: `alerts.log`

Note: The outputs already present in the repository are trained from a sampled
subset for quick reproduction. Re-running the code will overwrite or regenerate
outputs in the same format.

Data loading priority:
1. `data/raw/` (8 CSV files)
2. `data/merged_dataset.csv`
3. `outputs/reports/merged_dataset.csv`

## Results

The following metrics are from `outputs/reports/model_comparison.csv` (weighted averages),
computed on a sampled subset for reproducibility:

| Model | Accuracy | Precision | Recall | F1-score |
|-------|----------|-----------|--------|----------|
| Random Forest | 0.9956 | 0.9956 | 0.9956 | 0.9956 |
| KNN | 0.9810 | 0.9839 | 0.9810 | 0.9821 |
| Logistic Regression | 0.7417 | 0.9500 | 0.7417 | 0.8176 |
| SVM | 0.7160 | 0.9441 | 0.7160 | 0.7953 |
| Naive Bayes | 0.1138 | 0.8572 | 0.1138 | 0.1389 |

Best model: Random Forest (highest weighted F1-score and recall).

Per-class classification reports are saved in `outputs/reports/`:

- classification_report_Random_Forest.txt
- classification_report_KNN.txt
- classification_report_Logistic_Regression.txt
- classification_report_SVM.txt
- classification_report_Naive_Bayes.txt

## Real-time alert generation

The system uses the saved Random Forest model (`models/best_model.pkl`) to classify live network flows.

### How it works

1. A single network flow (selected features) is received as a Python dict
2. It is scaled using the saved StandardScaler
3. The model predicts the traffic class
4. If NOT BENIGN, an alert is printed and logged

### Alert format

```text
[ALERT] Suspicious traffic detected: DDoS. Destination Port: 80.
[INFO] Normal traffic detected.
```

### Run real-time demo

```bash
python -m src.realtime_alert
```

Alert logs are saved to `alerts.log` in the project root.

## Saved model

- File: `models/best_model.pkl`
- Saved with: joblib
- Contents: { "model": RandomForestClassifier, "label_encoder": LabelEncoder, "scaler": StandardScaler }

Load and use:

```python
from src.realtime_alert import load_best_model, predict_single_flow

bundle = load_best_model()
label, message = predict_single_flow(your_flow_dict, model=bundle)
```
