from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
import pandas as pd

def scale_features(X_train, X_test):
    """
    feat: add feature scaling with StandardScaler
    """
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled, scaler

def balance_data(X, y):
    """
    Nhiệm vụ: Vừa Under-sampling lớp BENIGN, vừa SMOTE các lớp thiểu số.
    """
    rus = RandomUnderSampler(sampling_strategy='not minority', random_state=42)
    X_res, y_res = rus.fit_resample(X, y)
    
    # 2. Tăng cường các lớp tấn công bằng SMOTE
    # feat: apply SMOTE for minority classes
    smote = SMOTE(sampling_strategy='auto', random_state=42)
    X_final, y_final = smote.fit_resample(X_res, y_res)
    
    return X_final, y_final