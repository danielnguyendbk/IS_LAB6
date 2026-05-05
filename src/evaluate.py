import os

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import (
	ConfusionMatrixDisplay,
	accuracy_score,
	classification_report,
	confusion_matrix,
	f1_score,
	precision_recall_fscore_support,
)


def save_classification_report(y_true, y_pred, labels, target_names, output_path):
	report = classification_report(
		y_true,
		y_pred,
		labels=labels,
		target_names=target_names,
		digits=4,
		zero_division=0,
	)
	os.makedirs(os.path.dirname(output_path), exist_ok=True)
	with open(output_path, "w", encoding="utf-8") as file:
		file.write(report)


def save_confusion_matrix(y_true, y_pred, labels, target_names, output_path):
	cm = confusion_matrix(y_true, y_pred, labels=labels)
	disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=target_names)
	fig, ax = plt.subplots(figsize=(10, 8))
	disp.plot(include_values=False, cmap="Blues", ax=ax, xticks_rotation=45)
	plt.tight_layout()
	os.makedirs(os.path.dirname(output_path), exist_ok=True)
	plt.savefig(output_path)
	plt.close(fig)


def build_model_comparison_row(model_name, y_true, y_pred):
	accuracy = accuracy_score(y_true, y_pred)
	precision, recall, f1_weighted, _ = precision_recall_fscore_support(
		y_true,
		y_pred,
		average="weighted",
		zero_division=0,
	)
	f1_macro = f1_score(y_true, y_pred, average="macro", zero_division=0)

	return {
		"Model": model_name,
		"Accuracy": accuracy,
		"Precision": precision,
		"Recall": recall,
		"F1-score": f1_weighted,
		"Macro F1": f1_macro,
	}


def save_model_comparison(rows, output_path):
	df = pd.DataFrame(rows)
	os.makedirs(os.path.dirname(output_path), exist_ok=True)
	df.to_csv(output_path, index=False)
	return df
