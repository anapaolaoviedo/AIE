# analyzer/ethics_report.py
import json
import os

def generate_ethics_score(score_summary: dict) -> str:
    total_score = sum(score_summary.values())
    if total_score >= 6:
        return "🟢 Low Risk"
    elif total_score >= 3:
        return "🟡 Medium Risk"
    else:
        return "🔴 High Risk"

def generate_report(results: dict, report_path: str):
    # Categorize flags
    score_summary = {
        "Fairness": int(results.get("uses_fairlearn", False)) + int(results.get("uses_bias_mitigation_toolkit", False)) + int(results.get("handles_class_imbalance", False)),
        "Transparency": int(results.get("has_explainability", False)) + int(results.get("has_model_card", False)),
        "Privacy": int(results.get("uses_privacy_enhancing_tech", False)),
        "Accountability": 1 - int(results.get("hardcoded_threshold", False)) + 1 - int(results.get("missing_validation", False))
    }

    ethics_score = generate_ethics_score(score_summary)

    red_flags = []
    recommendations = []

    if results.get("missing_validation", False):
        red_flags.append("No validation techniques found in model")
        recommendations.append("Use cross-validation to reduce overfitting.")

    if not results.get("handles_class_imbalance", False):
        red_flags.append("No fairness-aware data handling (SMOTE, class weights)")
        recommendations.append("Add class balancing (e.g., SMOTE or class_weight).")

    if not results.get("uses_privacy_enhancing_tech", False):
        red_flags.append("No privacy-enhancing technologies")
        recommendations.append("Use differential privacy or federated learning.")

    if not results.get("has_explainability", False):
        recommendations.append("Include explainability tools like SHAP or LIME.")

    if not results.get("has_model_card", False):
        recommendations.append("Add a model card to document intended use, risks, and performance.")

    report_data = {
        "ethics_score": ethics_score,
        "score_summary": score_summary,
        "ethical_flags": results,
        "red_flags": red_flags,
        "recommendations": recommendations
    }

    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=4)

    print(f"\n✅ Ethics report saved to: {report_path}\n")
    print("📊 Ethics Score:", ethics_score)