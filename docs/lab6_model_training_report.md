# LAB 6 - Train 5 Models and Evaluation Report

## 1. Muc tieu

Bao cao tap trung vao viec huan luyen va danh gia 5 mo hinh: Logistic Regression, SVM, Naive Bayes, KNN, va Random Forest tren bai toan Network Intrusion Detection. Muc tieu chinh la nhan dien cac lop tan cong (attack classes), vi vay chi so recall cho cac lop attack duoc uu tien hon so voi chi nhin vao accuracy.

## 2. Dataset va tien xu ly du lieu

Cac file du lieu va tep phu tro da sinh trong qua trinh xu ly:

- [ouputs/reports/merged_dataset.csv](../ouputs/reports/merged_dataset.csv): du lieu sau khi gop cac file CSV.
- [ouputs/reports/merged_head.csv](../ouputs/reports/merged_head.csv): mau du lieu (preview) sau khi gop.
- [ouputs/reports/preprocessed_dataset.csv](../ouputs/reports/preprocessed_dataset.csv): du lieu sau tien xu ly (lam sach, loai trung, toi uu).
- [models/selected_features.json](../models/selected_features.json): danh sach dac trung duoc chon.
- [models/label_encoder.pkl](../models/label_encoder.pkl): bo ma hoa nhan.

Trong bai toan nay, BENIGN la lop binh thuong, cac lop con lai la attack classes.

## 3. Cac mo hinh da huan luyen

| Mo hinh | Vai tro | Dac diem ngan gon |
|---|---|---|
| Logistic Regression | Baseline tuyen tinh | Don gian, nhanh, de dien giai |
| SVM | Mo hinh phan tach bien | Hoat dong tot khi bien ro rang |
| Naive Bayes | Mo hinh xac suat | Nhanh, gia dinh doc lap dac trung |
| KNN | Lang gieng gan nhat | Du doan dua tren mau gan nhat |
| Random Forest | Ensemble cay quyet dinh | Manh voi du lieu tabular |

## 4. Ket qua danh gia tung mo hinh

So lieu duoc lay tu cac file classification report.

### Logistic Regression

- Accuracy: 0.74
- Macro Precision: 0.26
- Macro Recall: 0.62
- Macro F1-score: 0.30
- Weighted F1-score: 0.82

Nhan xet:
- Diem manh: Weighted F1 cao do du doan tot lop BENIGN.
- Diem yeu: Macro F1 thap, cho thay hieu nang kem tren cac lop attack nho.
- Co dau hieu thien lech ve BENIGN.

### SVM

- Accuracy: 0.72
- Macro Precision: 0.25
- Macro Recall: 0.61
- Macro F1-score: 0.29
- Weighted F1-score: 0.80

Nhan xet:
- Diem manh: Weighted F1 kha, xu ly lop BENIGN on.
- Diem yeu: Macro F1 thap, nhieu lop attack nho co hieu nang kem.
- Thien lech ve BENIGN.

### Naive Bayes

- Accuracy: 0.11
- Macro Precision: 0.12
- Macro Recall: 0.32
- Macro F1-score: 0.08
- Weighted F1-score: 0.14

Nhan xet:
- Diem manh: Toc do nhanh.
- Diem yeu: Hieu nang tong the rat thap, nhan dien attack kem.
- Khong phu hop cho bai toan nay.

### KNN

- Accuracy: 0.98
- Macro Precision: 0.58
- Macro Recall: 0.64
- Macro F1-score: 0.60
- Weighted F1-score: 0.98

Nhan xet:
- Diem manh: Hieu nang tot tren nhieu lop attack, weighted F1 cao.
- Diem yeu: Van con lop attack nho co chi so thap.
- It thien lech BENIGN hon so voi cac mo hinh tuyen tinh.

### Random Forest

- Accuracy: 1.00
- Macro Precision: 0.65
- Macro Recall: 0.65
- Macro F1-score: 0.65
- Weighted F1-score: 1.00

Nhan xet:
- Diem manh: Hieu nang tong the cao, macro F1 cao nhat trong 5 mo hinh.
- Diem yeu: Mot so lop co support = 0 nen chi so bang 0.
- Nhan dien attack tot hon cac mo hinh con lai.

## 5. Confusion Matrix

Confusion matrix giup quan sat cac lop bi nham lan voi nhau.

- ![KNN](../ouputs/figures/confusion_matrix_KNN.png)
- ![Logistic Regression](../ouputs/figures/confusion_matrix_logistic_regression.png)
- ![Naive Bayes](../ouputs/figures/confusion_matrix_naive_bayes.png)
- ![Random Forest](../ouputs/figures/confusion_matrix_Random_Forest.png)
- ![SVM](../ouputs/figures/confusion_matrix_SVM.png)

## 6. Bang so sanh model

So lieu duoc lay tu [ouputs/reports/model_comparison.csv](../ouputs/reports/model_comparison.csv).

| Model | Accuracy | Precision (weighted) | Recall (weighted) | F1-score (weighted) | Macro F1 |
|---|---:|---:|---:|---:|---:|
| Random Forest | 0.9956 | 0.9956 | 0.9956 | 0.9956 | 0.8088 |
| KNN | 0.9810 | 0.9839 | 0.9810 | 0.9821 | 0.6972 |
| Logistic Regression | 0.7417 | 0.9500 | 0.7417 | 0.8176 | 0.3238 |
| SVM | 0.7160 | 0.9441 | 0.7160 | 0.7953 | 0.3136 |
| Naive Bayes | 0.1138 | 0.8572 | 0.1138 | 0.1389 | 0.0901 |

Nhan xet: Random Forest co Macro F1 cao nhat va cac chi so weighted gan nhu toi uu, do do la ung vien tot nhat.

## 7. Chon best model

Theo tieu chi uu tien Macro F1-score va recall cua cac lop attack, Random Forest duoc chon lam best model vi:

- Hieu nang tong the cao nhat.
- Macro F1 vuot troi so voi cac mo hinh con lai.
- Kha nang nhan dien attack on hon, giam nguy co bo sot tan cong.
- Phu hop voi du lieu tabular.

## 8. Cac file dau ra

| Nhom file | Mo ta |
|---|---|
| [ouputs/reports/classification_report_KNN.txt](../ouputs/reports/classification_report_KNN.txt) | Report chi tiet cho KNN |
| [ouputs/reports/classification_report_Logistic_Regression.txt](../ouputs/reports/classification_report_Logistic_Regression.txt) | Report chi tiet cho Logistic Regression |
| [ouputs/reports/classification_report_Naive_Bayes.txt](../ouputs/reports/classification_report_Naive_Bayes.txt) | Report chi tiet cho Naive Bayes |
| [ouputs/reports/classification_report_Random_Forest.txt](../ouputs/reports/classification_report_Random_Forest.txt) | Report chi tiet cho Random Forest |
| [ouputs/reports/classification_report_SVM.txt](../ouputs/reports/classification_report_SVM.txt) | Report chi tiet cho SVM |
| [ouputs/figures/confusion_matrix_KNN.png](../ouputs/figures/confusion_matrix_KNN.png) | Confusion matrix cho KNN |
| [ouputs/figures/confusion_matrix_logistic_regression.png](../ouputs/figures/confusion_matrix_logistic_regression.png) | Confusion matrix cho Logistic Regression |
| [ouputs/figures/confusion_matrix_naive_bayes.png](../ouputs/figures/confusion_matrix_naive_bayes.png) | Confusion matrix cho Naive Bayes |
| [ouputs/figures/confusion_matrix_Random_Forest.png](../ouputs/figures/confusion_matrix_Random_Forest.png) | Confusion matrix cho Random Forest |
| [ouputs/figures/confusion_matrix_SVM.png](../ouputs/figures/confusion_matrix_SVM.png) | Confusion matrix cho SVM |
| [ouputs/reports/model_comparison.csv](../ouputs/reports/model_comparison.csv) | Bang so sanh metric giua cac mo hinh |
| [models/selected_features.json](../models/selected_features.json) | Danh sach dac trung duoc chon |
| [models/best_random_forest_pipeline.pkl](../models/best_random_forest_pipeline.pkl) | Pipeline Random Forest tot nhat |
| [models/best_by_macro_f1_random_forest_pipeline.pkl](../models/best_by_macro_f1_random_forest_pipeline.pkl) | Pipeline Random Forest toi uu theo Macro F1 |

## 9. Ket luan

Bai lab da hoan thanh viec huan luyen 5 mo hinh, sinh classification report, confusion matrix, va bang so sanh metric. Best model duoc chon la Random Forest theo tieu chi Macro F1 va recall cho cac lop attack. Trong bai toan can bang khong dong deu, recall cho attack classes quan trong hon viec chi nhin vao accuracy.
