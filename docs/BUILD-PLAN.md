# Implementation and evaluation plan

## Midpoint deliverables

The initial package contains the research, three submission narratives, architecture, reproducible deterministic review prototype, seven synthetic scenarios, tests, demo report, presentation, and presenter notes. It establishes the decision workflow before adding language models.

## Next milestones

| Milestone | Deliverable | Acceptance criterion |
| --- | --- | --- |
| Document intake | PDF or image extraction with source references | Required fields match hand-labeled invoices and missing fields trigger review |
| IBM agent integration | Specialist agents calling typed evidence tools | Findings cite available records, invalid tool output triggers review, no model controls payment credentials |
| Cash assessment | Baseline forecast and uncertainty comparison | Time-based evaluation against simple recurring-obligation and historical-average baselines |
| Risk assessment | Rules plus candidate anomaly model | Measure precision, recall, and unnecessary reviews on held-out patterns, not just regenerated training templates |
| Approval workflow | Review screen and durable state transitions | Role checks, changed-recipient invalidation, expiry, and duplicate-request tests pass |
| Sandbox execution | Isolated payment adapter and reconciliation | One authorized request creates at most one intended sandbox payment across retries |
| Portfolio demonstration | Screenshots, demo recording, final narrative | Every shown feature maps to reproducible behavior and its stated limitations |

Sequence is intentional. Confirm IBM access before model-dependent implementation. Complete document extraction and evidence grounding before treating generated explanations as useful.

## Evaluation framework

1. Rules-only baseline: current engine.
2. Agent-assisted review: document extraction and evidence coordination with the same policy engine.
3. Later combined assessment: uncertainty estimates and payment scheduling where data supports evaluation.

Report field extraction accuracy, discrepancy recall, false holds, human review agreement, time to prepare a case, tool-call failures, and evidence citation correctness. Statistical forecasts require temporal splits and comparison against simple baselines. Synthetic cases demonstrate behavior but do not establish real fraud-detection performance or financial savings.

## Current evaluation boundary

The seven scenarios are curated acceptance cases, not a representative benchmark. Unit checks cover arithmetic, decision precedence, threshold boundaries, date horizons, currency handling, report escaping, and input immutability. Broad schema validation, persistent state, authentication, concurrent reservations, and live integration are not implemented.

## User research without business deployment

A future usability session may use fictional cases and ask participants to review evidence. Participation and any external-work arrangements should be resolved independently before company-specific implementation. The present deliverable requires no business access or real records.
