# Research and competitive context

Sources checked October 22, 2026. Statistics refer to their stated populations and periods.

## The payment decision problem

A supplier invoice requires several distinct judgments: supporting evidence, recipient identity, authorization, and payment timing. The proposed opportunity is to make those judgments easier to assemble and inspect in one review. Whether the intended users lack a satisfactory existing solution remains a validation question.

| Claim | Source and scope | Product implication |
| --- | --- | --- |
| 76% of respondents' organizations experienced attempted or actual payment fraud in 2025 | [AFP 2026 Payments Fraud and Control Survey](https://www.financialprofessionals.org/training-resources/resources/survey-research-economic-data/details/payments-fraud), 465 corporate professionals | Payment checks address a documented concern. This is broader than invoice fraud and includes unsuccessful attempts. |
| 54% cited difficulty paying operating expenses and 50% cited uneven cash flow | [Federal Reserve Banks 2026 Report on Employer Firms](https://www.fedsmallbusiness.org/-/media/project/clevelandfedtenant/fsbsite/reports/2026/2026-report-on-employer-firms/2026-report-on-employer-firms.pdf), printed page 3, 2025 survey | Payment timing deserves explicit attention. These survey results do not show that software can eliminate funding shortfalls. |
| Fraudulent supplier impersonation induced two US internet companies to transfer over $120 million | [DOJ sentencing release, December 19, 2019](https://www.justice.gov/usao-sdny/pr/lithuanian-man-sentenced-5-years-prison-theft-over-120-million-fraudulent-business), scheme operated around 2013–2015 | Check payment details against independently trusted supplier records. The release does not name the victims. |
| Verify account-number and payment-procedure changes with the requester through a trusted route | [FBI business email compromise guidance](https://www.fbi.gov/how-we-can-help-you/common-frauds-and-scams/business-email-compromise) | A changed recipient creates a verification task. The invoice itself cannot verify the new recipient. |

The Federal Reserve survey uses a convenience sample with weighting. The fraud and cash-flow statistics describe different populations and cannot be combined into a joint prevalence estimate. Neither supports a forecast of savings for FINALITY.

## Existing solutions

| Product or initiative | Documented capabilities | Implication |
| --- | --- | --- |
| [Ramp AP agents](https://support.ramp.com/ap-agents-available-in-ramp-bill-pay) | Invoice extraction, fraud and duplicate checks, policy review, payment automation | Multiple invoice agents alone are not a differentiator. |
| [BILL AI](https://www.bill.com/product/ai) and [approval controls](https://www.bill.com/product/payment-approvals) | Invoice automation, unusual amount alerts, duplicate checks, approval routing | An approval dashboard alone has substantial overlap. |
| [Float](https://www.floatapp.com/integrations) | Cash forecasts and scenarios using accounting data | Connecting invoices to a forecast is established functionality. |
| [Google AP2](https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol) | Agent payment authorization and supporting evidence | Do not claim the first permission layer for agent payments. Protocol compatibility is future exploration. |

Provider pages establish advertised capabilities, not independently measured effectiveness. This comparison is not an exhaustive market survey and does not establish absent features in competing products.

## Differentiation hypothesis

A portable payment-review assistant may help businesses that still assemble supporting evidence, cash consequences, and approvals manually. The intended contribution is a clear decision record with explicit evidence and uncertainty, configurable policies, and eventually an approval bound to the exact executable payment. These are design choices to validate, not claims of first invention.

## Validation questions

- How does the intended user prepare a payment run today?
- Which information is missing, duplicated, or slow to obtain?
- What do current tools already solve, and why are they insufficient for this user?
- Would evidence-backed recommendations change a real review decision?
- Does integration effort outweigh the time saved?

The current project uses synthetic records only. No customer deployment, interview, revenue, loss prevention, or product-market fit has been established.
