# Three-minute midpoint walkthrough

## Preparation

From the repository root, run `python3 -m finality`. Open `artifacts/demo-report.html` in a browser. The committed HTML works offline without running Python. Each scenario runs independently with synthetic records.

## 0:00–0:25: The problem

“A payment can look ordinary while its recipient details or cash consequences need attention. FINALITY assembles those checks and explains the next step.”

## 0:25–1:00: Ordinary invoice

Show Ordinary supplier invoice. Its $1,200 amount matches the purchase order, its recipient matches the supplier master record, and both cash scenarios remain above reserve. Explain that READY means checks passed, not that money moved.

## 1:00–1:35: Changed recipient

Show Supplier payment details changed. The amount remains ordinary, but the recipient differs. FINALITY returns HOLD and cites both account references. The next step is independent verification through a trusted contact, not trusting another message from the same source.

## 1:35–2:10: Cash shortfall

Show Legitimate invoice creates a cash shortfall. The $8,000 invoice matches its order, but cash falls to $4,000 against a $5,000 configured reserve after payroll and rent. FINALITY returns HOLD.

## 2:10–2:35: Uncertain receipt

Show Payment depends on an uncertain customer receipt. The base minimum is $8,800, while the stress minimum is $4,800. FINALITY returns REVIEW because the decision depends on an unconfirmed receipt.

## 2:35–3:00: Implementation status

“The working midpoint prototype uses deterministic checks and scheduled cash calculations. The next phase adds IBM agent orchestration and document understanding. We will measure whether agents improve evidence collection and review efficiency over this baseline.”

## Likely questions

**What makes it agentic?** The planned system coordinates document interpretation, evidence retrieval, and follow-up tasks through specialist agents. The current prototype is a deterministic baseline and does not claim autonomous agents.

**How is it different from Ramp or BILL?** Those products already cover substantial functionality. We are testing a lightweight, configurable workflow for users who still assemble checks manually. Its advantage remains a hypothesis.

**Did you train a fraud model?** No. Current risk checks use explicit rules. Training and evaluation require appropriate data and held-out testing.

**Did it prevent real fraud?** No. It flags simulated failure cases. Real effectiveness would require representative evaluation.

**Does this use real company data?** No. All companies, account references, transactions, and invoices are fictional.
