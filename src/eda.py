import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

os.makedirs('outputs/figures', exist_ok=True)

def plot_attack_distribution(df):
    """
    Vẽ biểu đồ phân bố các loại tấn công (cột Label) và lưu vào outputs/figures/
    """
    plt.figure(figsize=(12, 6))

    sns.countplot(
        data=df,
        x='Label',
        hue='Label',
        order=df['Label'].value_counts().index,
        palette='viridis',
        legend=False,
    )
    
    plt.title('Distribution of Attack Classes')
    plt.xlabel('Class Label')
    plt.ylabel('Count')

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    save_path = 'outputs/figures/attack_distribution.png'
    plt.savefig(save_path)
    plt.close() 
    
    print(f"Đã lưu biểu đồ phân bố tại: {save_path}")


def plot_correlation_heatmap(df):
    """
    Vẽ biểu đồ heatmap thể hiện mức độ tương quan giữa các đặc trưng số.
    """
    plt.figure(figsize=(16, 12))

    numeric_df = df.select_dtypes(include=[np.number])
    corr_matrix = numeric_df.corr()

    sns.heatmap(corr_matrix, annot=False, cmap='coolwarm', linewidths=0.5)
    
    plt.title('Feature Correlation Heatmap')
    plt.tight_layout()

    save_path = 'outputs/figures/correlation_heatmap.png'
    plt.savefig(save_path)
    plt.close()
    
    print(f"Đã lưu heatmap tương quan tại: {save_path}")

def run_eda(df):
    """
    Hàm tổng hợp để chạy toàn bộ pipeline EDA.
    """
    print("Bắt đầu vẽ biểu đồ phân bố Attack Classes...")
    plot_attack_distribution(df)
    
    print("Bắt đầu vẽ biểu đồ Correlation Heatmap...")
    plot_correlation_heatmap(df)
    
    print("EDA hoàn tất! Các biểu đồ đã được lưu trong outputs/figures/")

