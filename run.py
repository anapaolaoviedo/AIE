from analyzer.doc_analyzer import analyze_documentation
from analyzer.model_parser import analyze_model_code
from analyzer.ethics_report import generate_report

doc_results = analyze_documentation("examples/example_README.md")
code_results = analyze_model_code("examples/example_model.py")

# Merge both results
combined_results = {**doc_results, **code_results}

# Generate report
generate_report(combined_results, "reports/example_report.json")