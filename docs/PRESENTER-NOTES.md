# Midpoint speaking notes

## One-sentence introduction

FINALITY helps businesses review supplier payments by bringing invoice evidence, recipient checks, and cash consequences into one understandable decision.

## Ninety-second version

Before a business pays a supplier, someone has to check whether the invoice is supported, the recipient is correct, and the payment makes sense given upcoming obligations. Published research shows why those checks matter: AFP reports widespread attempted or actual payment fraud, while Federal Reserve survey findings show uneven cash flow affects half of surveyed small employer firms.

FINALITY proposes a focused review workflow. An Invoice Agent will inspect documents, a Risk Agent will compare supplier details and payment patterns, a Treasury Agent will assess cash consequences, and a Policy Agent will assemble the permitted next step. Deterministic rules will enforce approval limits and execution permissions.

At midpoint, I have a reproducible rules-based prototype with seven fictional scenarios. It identifies changed recipient details, blocks an already-paid invoice, and shows how a legitimate invoice can breach a cash reserve. It also distinguishes a base cash schedule from a case without unconfirmed receipts.

Existing tools already solve parts of this problem. My hypothesis is that some users need a simpler way to assemble and inspect the whole payment decision. Next I will add IBM agent integration and document extraction, then compare that workflow against the current baseline. I am measuring useful behavior rather than claiming real-world savings before evaluation.

## Before the checkpoint

- Open the presentation and the offline report before the call.
- Know the distinction between implemented rules and planned agent features.
- Use the three submission sections in IBM-MIDPOINT.md if a form is required.
- Confirm the actual portal fields and course completion status.
- Keep the repository private unless you decide to publish it. Reviewers need access to a private repository.
