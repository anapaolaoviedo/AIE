'''
Pretty terminal summary of the ethics report.

Renders the JSON report (the source of truth) with rich if available,
otherwise falls back to plain print.
'''

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# Max points per category, mirroring the scoring in analyzer/ethics_report.py
CATEGORY_MAX = {
    "Fairness": 4,
    "Transparency": 2,
    "Privacy": 2,
    "Accountability": 2,
}


def _risk_color(ethics_score):
    if "Low" in ethics_score:
        return "green"
    if "Medium" in ethics_score:
        return "yellow"
    return "red"


def print_report(report, report_path):
    if RICH_AVAILABLE:
        _print_rich(report, report_path)
    else:
        _print_plain(report, report_path)


def _print_rich(report, report_path):
    console = Console()
    ethics_score = report.get("ethics_score", "Unknown")
    color = _risk_color(ethics_score)

    console.print()
    console.print(Panel(f"[bold {color}]{ethics_score}[/bold {color}]",
                        title="AIE — Ethics Score", expand=False))

    table = Table(title="Score Breakdown")
    table.add_column("Category", style="bold")
    table.add_column("Score", justify="right")
    for category, score in report.get("score_summary", {}).items():
        max_score = CATEGORY_MAX.get(category)
        shown = f"{score}/{max_score}" if max_score else str(score)
        table.add_row(category, shown)
    console.print(table)

    red_flags = report.get("red_flags", [])
    if red_flags:
        console.print("\n[bold red]🚩 Red Flags[/bold red]")
        for flag in red_flags:
            console.print(f"  [red]•[/red] {flag}")

    recommendations = report.get("recommendations", [])
    if recommendations:
        console.print("\n[bold cyan]💡 Recommendations[/bold cyan]")
        for rec in recommendations:
            console.print(f"  [cyan]•[/cyan] {rec}")

    console.print(f"\n📄 Full JSON report: [bold]{report_path}[/bold]\n")


def _print_plain(report, report_path):
    ethics_score = report.get("ethics_score", "Unknown")

    print()
    print("=" * 40)
    print(f"  AIE — Ethics Score: {ethics_score}")
    print("=" * 40)

    print("\nScore Breakdown:")
    for category, score in report.get("score_summary", {}).items():
        max_score = CATEGORY_MAX.get(category)
        shown = f"{score}/{max_score}" if max_score else str(score)
        print(f"  {category:<15} {shown}")

    red_flags = report.get("red_flags", [])
    if red_flags:
        print("\nRed Flags:")
        for flag in red_flags:
            print(f"  - {flag}")

    recommendations = report.get("recommendations", [])
    if recommendations:
        print("\nRecommendations:")
        for rec in recommendations:
            print(f"  - {rec}")

    print(f"\nFull JSON report: {report_path}\n")
