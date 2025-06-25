from analyzer.doc_analyzer import analyze_documentation
from analyzer.model_parser import analyze_model_code
from analyzer.data_checker import analyze_dataset
from analyzer.ethics_report import generate_report

# Example file paths (replace with CLI args later or automate with main.py)
doc_path = "examples/example_README.md"
model_path = "examples/example_model.py"
data_path = "examples/mock_dataset.csv"

# Run each analyzer
doc_results = analyze_documentation(doc_path)
model_results = analyze_model_code(model_path)
data_results = analyze_dataset(data_path)

# Combine results
combined_results = {
    **doc_results,
    **model_results,
    **data_results
}

# Generate report
generate_report(combined_results, "reports/example_report.json")