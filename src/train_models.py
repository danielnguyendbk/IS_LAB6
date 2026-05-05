import os

import numpy as np
from imblearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

from src.balance import encode_labels, get_balancing_steps
from src.evaluate import (
	build_model_comparison_row,
	save_classification_report,
	save_confusion_matrix,
	save_model_comparison,
)
from src.features import select_core_features
from src.pipeline_builder import build_preprocessing_pipeline
from src.realtime_alert import save_best_model


MODEL_OUTPUTS = {
	"Logistic Regression": {
		"report": "classification_report_Logistic_Regression.txt",
		"confusion": "confusion_matrix_logistic_regression.png",
	},
	"SVM": {
		"report": "classification_report_SVM.txt",
		"confusion": "confusion_matrix_SVM.png",
	},
	"Naive Bayes": {
		"report": "classification_report_Naive_Bayes.txt",
		"confusion": "confusion_matrix_naive_bayes.png",
	},
	"KNN": {
		"report": "classification_report_KNN.txt",
		"confusion": "confusion_matrix_KNN.png",
	},
	"Random Forest": {
		"report": "classification_report_Random_Forest.txt",
		"confusion": "confusion_matrix_Random_Forest.png",
	},
}


def _build_models(random_state=42):
	return {
		"Logistic Regression": LogisticRegression(max_iter=2000),
		"SVM": SVC(kernel="rbf", probability=True),
		"Naive Bayes": GaussianNB(),
		"KNN": KNeighborsClassifier(n_neighbors=5),
		"Random Forest": RandomForestClassifier(
			n_estimators=200,
			random_state=random_state,
			n_jobs=-1,
		),
	}


def train_and_evaluate_models(
	df,
	random_state=42,
	test_size=0.2,
	reports_dir="outputs/reports",
	figures_dir="outputs/figures",
):
	if "Label" not in df.columns:
		raise ValueError("Dataset must include a Label column.")

	X = select_core_features(df)
	y_raw = df["Label"]
	y, label_encoder = encode_labels(y_raw)

	X_train, X_test, y_train, y_test = train_test_split(
		X,
		y,
		test_size=test_size,
		stratify=y,
		random_state=random_state,
	)

	over, under = get_balancing_steps(y_train, random_state=random_state)
	preprocessing = build_preprocessing_pipeline(over, under)

	labels = np.unique(y)
	target_names = label_encoder.inverse_transform(labels)

	comparison_rows = []

	for model_name, model in _build_models(random_state).items():
		pipeline = Pipeline(steps=preprocessing.steps + [("model", model)])
		pipeline.fit(X_train, y_train)

		y_pred = pipeline.predict(X_test)

		report_path = os.path.join(reports_dir, MODEL_OUTPUTS[model_name]["report"])
		confusion_path = os.path.join(figures_dir, MODEL_OUTPUTS[model_name]["confusion"])

		save_classification_report(
			y_test,
			y_pred,
			labels=labels,
			target_names=target_names,
			output_path=report_path,
		)
		save_confusion_matrix(
			y_test,
			y_pred,
			labels=labels,
			target_names=target_names,
			output_path=confusion_path,
		)

		comparison_rows.append(
			build_model_comparison_row(model_name, y_test, y_pred)
		)

		if model_name == "Random Forest":
			scaler = pipeline.named_steps.get("scaler")
			save_best_model(
				pipeline.named_steps.get("model"),
				label_encoder=label_encoder,
				scaler=scaler,
				model_path="models/best_model.pkl",
			)

	comparison_path = os.path.join(reports_dir, "model_comparison.csv")
	save_model_comparison(comparison_rows, comparison_path)
