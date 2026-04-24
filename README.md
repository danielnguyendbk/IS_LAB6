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

```
data/
├── Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv
├── ...
```

---

## Project Structure

```
Network-Intrusion-Detection-ML/
│
├── data/                # Dataset (ignored in Git)
├── models/              # Saved models (.pkl)
├── output/              # Results, plots
├── src/
│   ├── config.py        # Configuration
│   ├── data_loader.py   # Load & merge dataset
│   ├── preprocessing.py # Data cleaning (to be implemented)
│   ├── eda.py           # Exploratory Data Analysis
│   ├── balance.py       # Handling imbalance
│   ├── feature.py       # Feature selection
│   ├── train_model.py   # Model training
│   ├── evaluate.py      # Evaluation
│   ├── realtime_alert.py# Real-time detection
│
├── main.py              # Main pipeline
├── requirements.txt
├── README.md
├── alerts.log
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

* Merged dataset (sample): `data/merged_data_sample.csv`
* Console logs showing loading & merging progress

---

## 🧠 Machine Learning Models (Planned)

The following models will be implemented and compared:

* Logistic Regression
* Support Vector Machine (SVM)
* Naive Bayes
* K-Nearest Neighbors (KNN)
* Random Forest (Best Model)

---

## 📈 Evaluation Metrics

Models will be evaluated using:

* Accuracy
* Precision
* Recall (**important for attack detection**)
* F1-score
* Confusion Matrix

---

## ⚡ Real-time Detection

The final system will:

* Accept a network flow input
* Predict using trained model
* Generate alert if attack detected

Example:

```
[ALERT] Suspicious traffic detected: DDoS. Destination Port: 80
```

---

## 📦 Deliverables

* Source code (modular, clean)
* Trained model (.pkl)
* README documentation
* Model comparison results
* Optional: alerts.log

---



