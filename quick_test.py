import os

REQUIRED_PATHS = [
    "README.md",
    "requirements.txt",
    "main.py",
    "src",
    "outputs",
    "outputs/reports",
    "outputs/figures",
    "models",
    "models/selected_features.json",
]

OPTIONAL_OUTPUTS = [
    "outputs/reports/model_comparison.csv",
    "outputs/reports/classification_report_Random_Forest.txt",
    "outputs/reports/classification_report_KNN.txt",
    "outputs/reports/classification_report_Logistic_Regression.txt",
    "outputs/reports/classification_report_SVM.txt",
    "outputs/reports/classification_report_Naive_Bayes.txt",
    "outputs/figures/confusion_matrix_Random_Forest.png",
    "outputs/figures/confusion_matrix_KNN.png",
    "outputs/figures/confusion_matrix_logistic_regression.png",
    "outputs/figures/confusion_matrix_SVM.png",
    "outputs/figures/confusion_matrix_naive_bayes.png",
    "outputs/figures/attack_distribution.png",
    "outputs/figures/correlation_heatmap.png",
    "models/best_model.pkl",
    "alerts.log",
]


def _exists(path):
    return os.path.exists(path)


def run_checks():
    print("===== QUICK TEST (NO TRAINING) =====")

    missing_required = [path for path in REQUIRED_PATHS if not _exists(path)]
    if missing_required:
        print("[FAIL] Missing required paths:")
        for path in missing_required:
            print(f"  - {path}")
    else:
        print("[PASS] All required paths exist.")

    missing_optional = [path for path in OPTIONAL_OUTPUTS if not _exists(path)]
    if missing_optional:
        print("[WARN] Optional outputs not found (OK for fresh clone):")
        for path in missing_optional:
            print(f"  - {path}")
    else:
        print("[PASS] Optional outputs present.")

    print("===== QUICK TEST COMPLETE =====")


if __name__ == "__main__":
    run_checks()
