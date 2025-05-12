# analyzer/ethics_report.py

import json
import os

def generate_ethics_score(results: dict) -> str:
    score = sum(results.values())
    if score >= 7:
        return "🟢 Low Risk"
    elif score >= 4:
        return "🟡 Medium Risk"
    else:
        return "🔴 High Risk"

def generate_report(results: dict, report_path: str):
    score = generate_ethics_score(results)

    report_data = {
        "ethical_flags": results,
        "ethics_score": score
    }

    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=4)

    print(f"\n✅ Ethics report saved to: {report_path}\n")
    print("📊 Ethics Score:", score)