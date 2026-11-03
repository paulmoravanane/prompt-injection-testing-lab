import csv
from pathlib import Path

FILES = {
    "Baseline": "baseline_results.csv",
    "Mitigation": "mitigation_results.csv",
    "Unseen tests": "unseen_results.csv",
}

def load_results(filename):
    path = Path(filename)
    if not path.exists():
        raise FileNotFoundError(f"Missing results file: {filename}")
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def summarize(rows):
    passed = sum(r["result"] == "PASS" for r in rows)
    failed = sum(r["result"] == "FAIL" for r in rows)
    errors = sum(r["result"] == "ERROR" for r in rows)
    indicators = sum(
        r.get("injection_indicator", "NO") == "YES" for r in rows
    )
    completed = passed + failed
    pass_rate = 100 * passed / completed if completed else 0
    failure_rate = 100 * failed / completed if completed else 0
    indicator_rate = 100 * indicators / len(rows) if rows else 0
    return {
        "trials": len(rows),
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "indicators": indicators,
        "pass_rate": pass_rate,
        "failure_rate": failure_rate,
        "indicator_rate": indicator_rate,
    }

def main():
    reports = {}
    all_rows = {}

    for label, filename in FILES.items():
        rows = load_results(filename)
        all_rows[label] = rows
        reports[label] = summarize(rows)

    lines = [
        "# Prompt Injection Lab — Results Comparison",
        "",
        "## Overall results",
        "",
        "| Experiment | Trials | Pass | Fail | Errors | Injection indicators | Pass rate | Task failure rate |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for label, s in reports.items():
        lines.append(
            f"| {label} | {s['trials']} | {s['passed']} | "
            f"{s['failed']} | {s['errors']} | {s['indicators']} | "
            f"{s['pass_rate']:.1f}% | {s['failure_rate']:.1f}% |"
        )

    lines += ["", "## Results by test case", ""]

    for label, rows in all_rows.items():
        lines += [f"### {label}", "", "| Test case | Trials | Pass | Fail | Errors | Injection indicators |",
                  "|---|---:|---:|---:|---:|---:|"]
        test_ids = sorted(set(r["test_id"] for r in rows))
        for test_id in test_ids:
            subset = [r for r in rows if r["test_id"] == test_id]
            s = summarize(subset)
            lines.append(
                f"| {test_id} | {s['trials']} | {s['passed']} | "
                f"{s['failed']} | {s['errors']} | {s['indicators']} |"
            )
        lines.append("")

    lines += [
        "## Interpretation",
        "",
        "The baseline experiment showed failures on the two original injection "
        "cases. The mitigation and unseen-test runs reported passing outputs "
        "for their recorded test cases.",
        "",
        "These results apply only to the prompts, model, and configuration tested. "
        "The mitigation prompt differs from the baseline prompt, so this comparison "
        "does not isolate which change caused the improvement. Passing these small "
        "test sets does not prove general prompt-injection resistance.",
        "",
        "## Reproducibility notes",
        "",
        "- Model: qwen2.5:3b",
        "- Runtime: Ollama",
        "- Temperature: 0",
        "- Source data: baseline_results.csv, mitigation_results.csv, unseen_results.csv",
        "- Review the CSV outputs if any errors or unexpected counts appear.",
    ]

    output = Path("comparison_report.md")
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("\n=== COMPARISON SUMMARY ===")
    for label, s in reports.items():
        print(
            f"{label}: {s['trials']} trials, {s['passed']} pass, "
            f"{s['failed']} fail, {s['errors']} errors, "
            f"{s['indicators']} injection indicators"
        )
    print(f"\nReport saved to: {output}")

if __name__ == "__main__":
    main()
