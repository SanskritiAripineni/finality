# Project brief

FINALITY supports evidence-based supplier payment review. This brief describes the proposed solution, its value, and the role of AI.

## Preliminary idea and description

FINALITY is an agentic AI payment-review assistant designed to help businesses check supplier invoices before payment. It brings together invoice evidence, approved supplier details, company approval rules, and the cash consequences of paying now. The intended user is a business owner, bookkeeper, or finance manager who currently assembles this information across separate records.

The proposed workflow reads an invoice, retrieves supporting evidence, identifies discrepancies, assesses scheduled cash obligations, and produces an understandable recommendation: ready for the next approval step, manager review required, hold for an unresolved exception, or block a duplicate. Future payment integration will operate in a sandbox. The project uses a fictional company and synthetic data.

The current deterministic prototype demonstrates seven payment-review scenarios, including changed recipient details, duplicate invoices, missing purchase orders, cash shortages, approval thresholds, and dependence on uncertain customer receipts. Agent orchestration and trained models remain planned.

## Value proposition

FINALITY aims to reduce the manual work required to assemble a payment decision and make overlooked exceptions easier to identify. It answers: Is the invoice supported? Do payment details match trusted records? What happens to cash if we pay now? Every finding includes its evidence and a next action.

The need is grounded in published research. AFP's 2026 survey reports attempted or actual payment fraud at 76% of respondents' organizations during 2025. Separately, the Federal Reserve Banks' 2026 small-business report shows that 50% of surveyed employer firms faced uneven cash flow and 54% faced challenges paying operating expenses. These findings establish relevant problems, not the effectiveness of FINALITY.

Existing products already provide invoice automation, fraud checks, and cash forecasting. Our differentiation hypothesis is that a lightweight, configurable review workflow can help users who still combine those checks manually. We will evaluate review time, discrepancy detection, unnecessary holds, and whether users find the evidence useful. No customer savings or fraud-prevention rate is claimed.

## AI-use justification

Invoices and supporting documents vary in format and often require context from several sources. AI can extract structured fields, retrieve relevant records, identify inconsistencies, and coordinate follow-up tasks. We propose specialist Invoice, Risk, Treasury, and Policy agents with explicit input and output contracts.

Deterministic software will calculate cash balances and enforce approval rules. An agent can recommend an action but cannot grant itself payment authority. A future executor will verify the approved recipient, amount, currency, and current decision before sandbox execution. Missing evidence will trigger review rather than a fabricated confidence score.

We will compare the agent-assisted workflow against the current rules-only prototype. If a simpler method performs equally well, that component will stay simple. IBM watsonx services are proposed integration targets, subject to account access and program requirements. No IBM service is connected in the current prototype.

## Evidence links

- [AFP 2026 survey, covering 2025](https://www.financialprofessionals.org/training-resources/resources/survey-research-economic-data/details/payments-fraud)
- [Federal Reserve Banks 2026 report, printed page 3](https://www.fedsmallbusiness.org/-/media/project/clevelandfedtenant/fsbsite/reports/2026/2026-report-on-employer-firms/2026-report-on-employer-firms.pdf)
- [Research and competitor comparison](RESEARCH.md)
