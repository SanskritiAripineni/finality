# Implementation and evaluation plan

## Current foundation

The current foundation includes a sourced problem statement, project brief, architecture, deterministic review engine, seven synthetic scenarios, an evidence report, and automated tests. It establishes the review workflow and a baseline for evaluating future agent capabilities.

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

## Development with IBM Bob

We plan to use IBM Bob to help organize the codebase, implement agent tools, generate tests for payment-review failure cases, debug issues, and maintain documentation. Team members will review generated changes and verify their behavior. Bob supports development; the proposed watsonx agent workflow will perform invoice review. Bob has not been used to build the current prototype.

## Evaluation framework

1. Rules-only baseline: current engine.
2. Agent-assisted review: document extraction and evidence coordination with the same policy engine.
3. Later combined assessment: uncertainty estimates and payment scheduling where data supports evaluation.

Report field extraction accuracy, discrepancy recall, false holds, human review agreement, time to prepare a case, tool-call failures, and evidence citation correctness. Statistical forecasts require temporal splits and comparison against simple baselines. Synthetic cases demonstrate behavior but do not establish real fraud-detection performance or financial savings.

## Current evaluation boundary

The seven scenarios are curated acceptance cases, not a representative benchmark. Unit checks cover arithmetic, decision precedence, threshold boundaries, date horizons, currency handling, report escaping, and input immutability. Broad schema validation, persistent state, authentication, concurrent reservations, and live integration are not implemented.

## User validation

Usability sessions can use fictional cases to measure whether participants understand the findings and can identify the required next action. Compare review time and decisions with the existing process. Operational validation with representative data is a separate future milestone.
