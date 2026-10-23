# FINALITY

Project brief by AI builders

## Preliminary Idea & Description

FINALITY is a proposed AI assistant that helps businesses review supplier invoices before making a payment. It is designed for owners, bookkeepers, and finance teams who need to check a bill against supplier records, purchase orders, and upcoming expenses.

The idea starts with a practical question: should this invoice be paid now? FINALITY would bring the relevant information together, flag anything that needs attention, and explain the next step. An invoice might match its purchase order but contain different payment details. Another might be legitimate but leave too little cash for payroll. These situations need different responses, and the recommendation should make that clear.

We have built an initial rules-based prototype using fictional business records. Our next step is to add document understanding and specialist AI agents, then test the complete review process.

## Value Proposition

Payment mistakes can be costly, and checking every bill takes time. In AFP's 2026 survey, 76% of respondents' organizations reported attempted or actual payment fraud in 2025 [1]. Separately, the Federal Reserve Banks' 2026 report found that 50% of surveyed small employer firms faced uneven cash flow [2].

FINALITY aims to help businesses make better-informed payment decisions with less manual checking. A reviewer would see the invoice, the supporting evidence, and the effect on available cash in one place, with a clear explanation of any issue.

Existing tools already automate invoices and forecast cash. Our focus is the review between receiving a bill and authorizing payment, especially where people still piece together information from separate records. We will assess the approach by measuring review time, discrepancies found, and unnecessary alerts.

## AI-Use Justification

Invoice review involves reading documents that vary in format and finding relevant details across several records. AI can help with that interpretation and coordination, while software rules handle the calculations and approval limits.

We plan to use specialist agents to read invoices, check supplier information, assess cash consequences, and apply company policy. Each would contribute findings to a shared review. If information is missing or a payment detail has changed, the system would ask for verification before proceeding.

We plan to explore IBM watsonx for the agent workflow. Payment approvals would remain under human control during development, and any payment integration would use a sandbox. We will compare the agent-assisted process with our current prototype to see whether it improves accuracy and reduces review effort.

## Sources

[1] [AFP, 2026 Payments Fraud and Control Survey](https://www.financialprofessionals.org/training-resources/resources/survey-research-economic-data/details/payments-fraud)

[2] [Federal Reserve Banks, 2026 Report on Employer Firms, p. 3](https://www.fedsmallbusiness.org/-/media/project/clevelandfedtenant/fsbsite/reports/2026/2026-report-on-employer-firms/2026-report-on-employer-firms.pdf)
