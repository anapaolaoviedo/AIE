from analyzer.doc_analyzer import analyze_documentation

results = analyze_documentation("examples/example_README.md")
for k, v in results.items():
    print(f"{k.title()}: {'Found' if v else 'Missing'}")