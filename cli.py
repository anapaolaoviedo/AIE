'''
AIE command-line interface.

Runs the analyzers on the files the user provides, generates the JSON
ethics report, then renders a terminal summary (and optionally HTML)
derived from that report.
'''

import argparse
import json
import os
import sys

from analyzer.doc_analyzer import analyze_documentation
from analyzer.model_parser import analyze_model_code
from analyzer.ethics_report import generate_report

try:
    from analyzer.data_checker import analyze_dataset
except ImportError:
    analyze_dataset = None

DEFAULT_OUTPUT = "reports/ethics_report.json"


def build_parser():
    parser = argparse.ArgumentParser(
        prog="aie",
        description="AIE — AI Ethical Analyzer: scan ML projects for ethical risks."
    )
    subparsers = parser.add_subparsers(dest="command")

    analyze = subparsers.add_parser(
        "analyze",
        help="Analyze model code, documentation, and/or a dataset."
    )
    analyze.add_argument("--model", help="Path to a Python file with model code")
    analyze.add_argument("--docs", help="Path to documentation (.md, .txt, .json)")
    analyze.add_argument("--data", help="Path to a CSV dataset")
    analyze.add_argument(
        "--output", default=DEFAULT_OUTPUT,
        help=f"Where to save the JSON report (default: {DEFAULT_OUTPUT})"
    )
    analyze.add_argument(
        "--html", action="store_true",
        help="Also generate a self-contained HTML report next to the JSON one"
    )
    return parser


def _run_analyzer(name, func, path):
    """Run one analyzer, warning and skipping on any failure."""
    if not path:
        print(f"[SKIP] No {name} file provided.")
        return None
    if not os.path.exists(path):
        print(f"[WARN] {name.capitalize()} file not found, skipping: {path}")
        return None
    try:
        return func(path)
    except Exception as e:
        print(f"[WARN] {name.capitalize()} analysis failed, skipping: {e}")
        return None


def run_analysis(model_path, docs_path, data_path, output_path, html=False):
    results = {}

    doc_results = _run_analyzer("documentation", analyze_documentation, docs_path)
    if doc_results:
        results.update(doc_results)

    model_results = _run_analyzer("model", analyze_model_code, model_path)
    if model_results:
        results.update(model_results)

    if data_path and analyze_dataset is None:
        print("[WARN] pandas is not installed — skipping dataset analysis. "
              "Run: pip install -r requirements.txt")
    else:
        data_results = _run_analyzer("dataset", analyze_dataset, data_path)
        if data_results:
            results.update(data_results)

    if not results:
        print("\nNothing to analyze. Provide at least one of --model, --docs, --data.")
        return 1

    generate_report(results, output_path)

    # The JSON report is the source of truth — render everything from it.
    with open(output_path, "r", encoding="utf-8") as f:
        report = json.load(f)

    from reporter.terminal import print_report
    print_report(report, output_path)

    if html:
        from reporter.html_report import generate_html_report
        html_path = os.path.splitext(output_path)[0] + ".html"
        generate_html_report(report, html_path)
        print(f"🌐 HTML report saved to: {html_path}")

    return 0


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command != "analyze":
        parser.print_help()
        return 1

    return run_analysis(args.model, args.docs, args.data, args.output, args.html)


if __name__ == "__main__":
    sys.exit(main())
