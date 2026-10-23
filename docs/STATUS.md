# Implementation status

## Available in the research prototype

- Deterministic invoice, supplier, policy, and cash checks.
- Seven independent synthetic scenarios.
- Evidence-linked findings and explicit decision precedence.
- Offline HTML report and structured JSON results.
- Automated tests and continuous integration.

## Planned capabilities

- PDF and image invoice extraction with source references.
- IBM watsonx integration and specialist agent orchestration.
- Statistical cash forecasts and evaluated risk models.
- Authenticated approvals and persistent audit records.
- Shared cash reservations and approval bound to the executable payment.
- Sandbox payments with reconciliation across retries.

## Evaluation scope

The current tests establish behavior on curated scenarios. They do not measure real-world fraud detection, customer savings, or production reliability. Cash results use scheduled arithmetic rather than a trained forecasting model. No external AI service or payment system is connected. Each review runs independently and does not reserve shared funds.
