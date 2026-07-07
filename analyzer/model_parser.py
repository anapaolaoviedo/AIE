'''
This code's pupose is to read ML code 
'''
def detect_framework(code):
    if "sklearn" in code or "scikit-learn" in code:
        return "sklearn"
    if "torch" in code:
        return "pytorch"
    if "tensorflow" in code or "keras" in code:
        return "tensorflow"
    return "unknown"


def analyze_model_code(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()

    flags = {
        "framework": detect_framework(code),
        "uses_fairlearn": "fairlearn" in code,
        "hardcoded_threshold": "if " in code and ">" in code,
        "has_explainability": "shap" in code or "lime" in code,
        "missing_validation": not any(k in code for k in [
            "train_test_split", "cross_val_score", "KFold", "StratifiedKFold"
        ]),
        "handles_class_imbalance": "class_weight='balanced'" in code or "SMOTE" in code,
        "uses_privacy_enhancing_tech": any(k in code for k in [
            "differential_privacy", "dp_optimizer", "PySyft", "FederatedAveraging"
        ]),
        "uses_bias_mitigation_toolkit": "aif360" in code or "DisparateImpactRemover" in code,
        "has_model_card": "model_card" in code
    }

    return flags 