import argparse
import json
from pathlib import Path
from .engine import review
from .report import render

def main():
    p=argparse.ArgumentParser(description="Run FINALITY's synthetic payment-review scenarios.")
    p.add_argument("--input",default="data/scenarios.json")
    p.add_argument("--report",default="artifacts/demo-report.html")
    args=p.parse_args()
    cases=json.loads(Path(args.input).read_text())
    results=[review(c) for c in cases]
    for r in results:
        print(f"{r['status']:6} {r['case_id']}: {r['title']}")
    target=Path(args.report);target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(render(cases,results))
    target.with_suffix('.json').write_text(json.dumps(results,indent=2))
    print(f"Report: {target.resolve()}")

if __name__ == "__main__":
    main()
