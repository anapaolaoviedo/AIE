# analyzer/doc_analyzer.py

import re

# Define keywords we expect in ethical ML documentation
ETHICS_KEYWORDS = [
    "fairness",
    "bias",
    "transparency",
    "explainability",
    "consent",
    "privacy",
    "accountability",
    "auditability"
]

def analyze_documentation(file_path):
    """
    Parses a documentation file and flags which ethical concepts are present or missing.
    Supports .md, .txt, and .json files.
    Returns a dict with keyword presence.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().lower()

        results = {}
        for keyword in ETHICS_KEYWORDS:
            results[keyword] = bool(re.search(rf"\b{keyword}\b", content))
        
        return results

    except FileNotFoundError:
        print(f"[ERROR] File not found: {file_path}")
        return None
    except Exception as e:
        print(f"[ERROR] Analyzing documentation failed: {e}")
        return None