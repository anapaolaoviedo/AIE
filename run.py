from analyzer.doc_analyzer import analyze_documentation
from analyzer.ethics_report import generate_report

doc_path = "examples/example_README.md"
report_path = "reports/example_report.json"

results = analyze_documentation(doc_path)

if results:
    generate_report(results, report_path)