import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.makedirs('outputs/figures', exist_ok=True)

def plot_attack_distribution(df):
    """
    Vẽ biểu đồ phân bố các loại tấn công (cột Label) và lưu vào outputs/figures/
    """
    plt.figure(figsize=(12, 6))

    sns.countplot(data=df, x='Label', order=df['Label'].value_counts().index, palette='viridis')
    
    plt.title('Distribution of Attack Classes')
    plt.xlabel('Class Label')
    plt.ylabel('Count')

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    save_path = 'outputs/figures/attack_distribution.png'
    plt.savefig(save_path)
    plt.close() 
    
    print(f"Đã lưu biểu đồ phân bố tại: {save_path}")


