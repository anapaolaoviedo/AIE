# 🕊️ AIE — AI Ethical Analyzer

AIE (AI Ethical Analyzer) is a **static analysis CLI tool** that scans ML projects for ethical risks — bias in data, missing fairness practices in code, and gaps in documentation. It outputs a structured JSON report with a risk score, red flags, and recommendations, plus a colored terminal summary and an optional HTML report. Everything runs locally and offline; it is meant as a quick ethical risk scan before deploying an ML model.

---

## 📦 Installation

```bash
pip install -r requirements.txt
```

Requires Python 3.9+.

---

## 🚀 Usage

```bash
python cli.py analyze \
  --model examples/example_model.py \
  --docs examples/example_README.md \
  --data examples/mock_dataset.csv \
  --output reports/my_report.json
```

All file arguments are optional — analyzers for files you don't provide are skipped gracefully. `--output` defaults to `reports/ethics_report.json`.

Add `--html` to also generate a self-contained HTML report next to the JSON one:

```bash
python cli.py analyze --model examples/example_model.py --html
```

You can also run it as a module from the repo root:

```bash
python . analyze --data examples/mock_dataset.csv
```

### What each flag analyzes

| Flag | Input | Checks |
|---|---|---|
| `--model` | Python model code | validation, explainability (SHAP/LIME), fairness libraries, class-imbalance handling, privacy tech, ML framework used |
| `--docs` | `.md` / `.txt` / `.json` | presence of 8 ethics keywords (fairness, bias, transparency, explainability, consent, privacy, accountability, auditability) |
| `--data` | CSV dataset | missing data, class imbalance, proxy attributes (zip, race, ethnicity, …) |

---

## 📊 Example output

```
✅ Ethics report saved to: reports/ethics_report.json

📊 Ethics Score: 🟡 Medium Risk

╭─ AIE — Ethics Score ─╮
│ 🟡 Medium Risk       │
╰──────────────────────╯
      Score Breakdown
┏━━━━━━━━━━━━━━━━┳━━━━━━━┓
┃ Category       ┃ Score ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━┩
│ Fairness       │   1/4 │
│ Transparency   │   0/2 │
│ Privacy        │   0/2 │
│ Accountability │   2/2 │
└────────────────┴───────┘

🚩 Red Flags
  • Detected significant class imbalance in dataset
  • Missing data found in: ['income']
  • No privacy-enhancing technologies
  • Sensitive proxy fields found: ['zip_code']

💡 Recommendations
  • Balance dataset using techniques like SMOTE or reweighting.
  • Use differential privacy or federated learning.
  • Include explainability tools like SHAP or LIME.
  • Add a model card to document intended use, risks, and performance.
  • Review dataset columns like ZIP, ethnicity for proxy bias.

📄 Full JSON report: reports/ethics_report.json
```

---

## ⚠️ Limitations

This is not deep statistical bias detection like fairness-aware modeling (e.g. disparate impact tests) — it's a quick ethical risk scan. Think of it as a **"first alert" system** for suspicious data, code, and documentation, not a full fairness audit.

---

## 🗂️ Project structure

```
AIE/
├── analyzer/            # core analysis logic
│   ├── data_checker.py    # CSV: missing data, imbalance, proxy attributes
│   ├── doc_analyzer.py    # docs: ethics keyword coverage
│   ├── model_parser.py    # code: fairness/validation/explainability flags
│   └── ethics_report.py   # scoring + JSON report generation
├── reporter/
│   ├── terminal.py        # colored terminal summary (rich, with plain fallback)
│   └── html_report.py     # self-contained HTML report (--html)
├── examples/            # sample model, README, and dataset to try it out
├── reports/             # generated reports
├── cli.py               # main entry point
├── __main__.py          # module entry point
└── run.py               # legacy hardcoded runner (kept for backwards compat)
```
