# --- Dataset Analysis Function ---
# this file evaluates the data that trains the model 
#becuase biased or incomplete datasets are one of the most common sources of unethical AI
import pandas as pd
from collections import Counter
import os

def analyze_dataset(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset not found: {filepath}")

    df = pd.read_csv(filepath)
    results = {}

    # --- Missing Data Detection ---
    missing_cols = df.columns[df.isnull().any()].tolist()
    results["missing_data_columns"] = missing_cols

    # --- Class Imbalance Detection ---
    # Try to detect a likely target column
    target_col = None
    for col in df.columns[::-1]:  # Check last columns first
        if df[col].nunique() <= 10 and df[col].dtype in ['int64', 'object']:
            target_col = col
            break

    if target_col:
        label_counts = dict(Counter(df[target_col]))
        total = sum(label_counts.values())
        most_common = max(label_counts.values())
        imbalance_ratio = most_common / total

        results["target_column"] = target_col
        results["class_imbalance_detected"] = imbalance_ratio > 0.8
        results["most_common_label_ratio"] = round(imbalance_ratio, 2)
        results["label_distribution"] = label_counts
    else:
        results["class_imbalance_detected"] = False
        results["target_column"] = None

    # --- Proxy Attribute Warning ---
    proxy_keywords = ["zip", "location", "surname", "ethnicity", "race"]
    proxy_cols = [col for col in df.columns if any(p in col.lower() for p in proxy_keywords)]
    results["proxy_fields"] = proxy_cols

    return results


'''
LIMITATIONS
This is not deep statistical bias detection like fairness-aware modeling
(e.g. disparate impact tests), but it’s a quick ethical risk scan.
Think of it as a “first alert” system for suspicious data.
'''