# Network Intrusion Detection System (NIDS) using Machine Learning

## 📌 Project Overview

This project implements a **Real-time Network Intrusion Detection System (NIDS)** using Machine Learning techniques on the **CIC-IDS2017 dataset**.

The system is designed to:

* Analyze network traffic data
* Detect malicious activities (DoS, DDoS, PortScan, Web Attacks, etc.)
* Generate real-time alerts for suspicious traffic

---

## Dataset

* **Dataset Name:** CIC-IDS2017
* **Source:** https://www.kaggle.com/datasets/chethuhn/network-intrusion-dataset
* **Features:** 79 columns (78 numerical + 1 label)
* **Classes:** BENIGN + multiple attack types
* **Challenge:** Highly imbalanced dataset

> ⚠️ Note: Dataset is **not included** in this repository due to large size.

### 📥 How to use dataset

1. Download dataset from the link above
2. Extract all CSV files
3. Place them into the `data/` folder:

```text
data/
├── Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv
├── Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv
├── Friday-WorkingHours-Morning.pcap_ISCX.csv
├── Monday-WorkingHours.pcap_ISCX.csv
├── Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv
├── Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv
├── Tuesday-WorkingHours.pcap_ISCX.csv
└── Wednesday-workingHours.pcap_ISCX.csv
```

---

## Project Structure

```text
Network-Intrusion-Detection-ML/
│
├── data/                # Dataset CSV files (ignored in Git)
├── models/              # Saved models (.pkl)
├── outputs/             # Results, plots, reports
├── src/
│   ├── config.py        # Configuration paths and constants
│   ├── data_loader.py   # Load and merge 8 CIC-IDS2017 CSV files
│   ├── preprocessing.py # Clean NaN/inf values, remove duplicates, optimize data
│   ├── eda.py           # Attack distribution plot and correlation heatmap
│   ├── balance.py       # LabelEncoder, SMOTE, RandomUnderSampler
│   ├── features.py      # Select 18 core features
│   ├── pipeline_builder.py # Build imblearn preprocessing pipeline
│   ├── train_models.py  # Train ML models
│   ├── evaluate.py      # Reports and confusion matrices
│   └── realtime_alert.py# Save/load model and generate alerts
│
├── main.py              # Main pipeline
├── requirements.txt
├── README.md
└── alerts.log
```

---

## 🏗️ Architecture

```text
Raw CSV files (8 files)
       ↓
  data_loader.py   ← Merge into 1 DataFrame
       ↓
preprocessing.py   ← Clean, handle NaN/inf, deduplicate, downcast
       ↓
     eda.py         ← Attack distribution plot, correlation heatmap
       ↓
   balance.py       ← LabelEncode → SMOTE → RandomUnderSampler
       ↓
   features.py      ← Select 18 core features
       ↓
pipeline_builder.py ← Assemble imblearn Pipeline
       ↓
 train_models.py    ← Train 5 ML models
       ↓
  evaluate.py       ← Classification reports, confusion matrices
       ↓
realtime_alert.py   ← Save .pkl → Load → Real-time prediction → Suricata alert
```

---

## ⚙️ Installation

### 1. Clone repository

```bash
git clone https://github.com/<your-username>/Network-Intrusion-Detection-ML.git
cd Network-Intrusion-Detection-ML
```

### 2. Create virtual environment (optional)

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

### Run the pipeline

```bash
python main.py
```

### Output

* Merged dataset: `data/merged_data.csv`
* Figures: `outputs/figures/`
* Evaluation reports: `outputs/reports/`
* Saved model bundle: `models/best_model.pkl`
* Alert log: `alerts.log`

---

## 🧠 Machine Learning Models & Results

The following 5 models were trained on the preprocessed CIC-IDS2017 dataset with 18 selected features:

| Model               | Accuracy | Precision | Recall | F1-Score |
|---------------------|----------|-----------|--------|----------|
| Logistic Regression | ~TBD%    | ~TBD      | ~TBD   | ~TBD     |
| SVM                 | ~TBD%    | ~TBD      | ~TBD   | ~TBD     |
| Naive Bayes         | ~TBD%    | ~TBD      | ~TBD   | ~TBD     |
| K-Nearest Neighbors | ~TBD%    | ~TBD      | ~TBD   | ~TBD     |
| **Random Forest**   | **~TBD%**| **~TBD**  | **~TBD**| **~TBD** |

> ✅ **Best Model: Random Forest** — selected based on highest F1-score and Recall on attack classes.
> In cybersecurity, missing a real attack (low Recall) is more dangerous than a false alarm.

> ⚠️ Replace `~TBD` values with actual metrics after running the pipeline.

---

## 📈 Evaluation Metrics

Models are evaluated using:

* Accuracy
* Precision
* Recall (**important for attack detection**)
* F1-score
* Confusion Matrix

Reports and confusion matrices should be saved under `outputs/reports/` after training and evaluation.

---

## ⚡ Real-time Alert Generation

The system uses the saved Random Forest model (`models/best_model.pkl`) to classify live network flows.

### How it works

1. A single network flow (18 features) is received as a Python dict
2. It is scaled using the saved StandardScaler
3. The Random Forest predicts the traffic class
4. If NOT BENIGN → a Suricata-style alert is printed and logged

### Alert format

```text
[ALERT] Suspicious traffic detected: DDoS. Destination Port: 80.
[INFO] Normal traffic detected.
```

### Run real-time demo

```bash
python main.py
# Or standalone:
python -m src.realtime_alert
python -c "
from src.realtime_alert import load_best_model, run_realtime_demo
bundle = load_best_model()
run_realtime_demo(bundle, n_samples=10)
"
```

Alert logs are saved to `alerts.log` in the project root.

---

## 💾 Saved Model

* **File:** `models/best_model.pkl`
* **Saved with:** `joblib`
* **Contents:** `{ "model": RandomForestClassifier, "label_encoder": LabelEncoder, "scaler": StandardScaler }`
* **Size:** If `best_model.pkl` is larger than 100MB, store it with Git LFS or provide a Google Drive link here.

Load and use:

```python
from src.realtime_alert import load_best_model, predict_single_flow

bundle = load_best_model()
label, message = predict_single_flow(your_flow_dict, model=bundle)
```

---

## 📦 Deliverables

* Source code (modular, clean)
* Trained model (`models/best_model.pkl`)
* README documentation
* Model comparison results
* Real-time alert generation
* Optional: `alerts.log`

---

## Project Architecture

The IDS project follows this flow:

```text
data_loader.py -> preprocessing.py -> eda.py -> balance.py -> features.py
-> pipeline_builder.py -> train_models.py -> evaluate.py -> realtime_alert.py
```

Thanh's responsibility is the final deployment and alert layer in `src/realtime_alert.py`: load/save the best Random Forest model, prepare one flow with the selected 18 features, predict one flow, print a BENIGN info line or a Suricata-style alert, and append attack alerts to `alerts.log`.

## Installation

```bash
pip install -r requirements.txt
```

Use Python from the project root so relative paths like `models/best_model.pkl` and `alerts.log` resolve correctly.

## How to run full pipeline

```bash
python main.py
```

After training is integrated, the pipeline should save the best Random Forest deployment bundle to:

```text
models/best_model.pkl
```

## How to run real-time alert demo

```bash
python -m src.realtime_alert
```

The demo loads `models/best_model.pkl`, creates one sample flow, and calls `predict_single_flow(...)`. If the file is missing, the module prints:

```text
Best model not found. Please train and save Random Forest model first.
```

## Best Model Deployment

The deployed best model is **Random Forest**. It is saved with `joblib` through:

```python
from src.realtime_alert import save_best_model

save_best_model(model, model_path="models/best_model.pkl")
```

The saved bundle may include:

```text
model: trained RandomForestClassifier
label_encoder: fitted LabelEncoder
scaler: fitted StandardScaler
```

If `models/best_model.pkl` is larger than 100MB, do not commit it directly with normal Git. Use Git LFS or replace it with a Google Drive download link in this README.

## alerts.log explanation

`alerts.log` stores only suspicious non-BENIGN predictions when `write_log=True`. Console output stays concise:

```text
[INFO] Normal traffic detected.
[ALERT] Suspicious traffic detected: <label>. Destination Port: <port>.
```

Log entries include a timestamp before the alert message, for example:

```text
2026-05-02 21:30:00 [ALERT] Suspicious traffic detected: DDoS. Destination Port: 80.
```

If the input flow does not include `Destination Port`, `Dst Port`, or `dst_port`, the alert uses `Destination Port: N/A.`

## Model comparison table

Replace the placeholder values after the full training/evaluation run.

| Model | Accuracy | Precision | Recall | F1-Score | Deployment |
|-------|----------|-----------|--------|----------|------------|
| Logistic Regression | TBD | TBD | TBD | TBD | No |
| SVM | TBD | TBD | TBD | TBD | No |
| Naive Bayes | TBD | TBD | TBD | TBD | No |
| K-Nearest Neighbors | TBD | TBD | TBD | TBD | No |
| Random Forest | TBD | TBD | TBD | TBD | Yes, best model |
