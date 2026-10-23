# FINALITY

Project brief by AI builders

## Preliminary Idea & Description

FINALITY is a proposed AI agent that helps business owners, bookkeepers, and finance teams review supplier invoices before making a payment. It addresses a practical problem: deciding whether a bill is supported by the right records, whether the recipient details are correct, and whether paying now would leave enough cash for upcoming expenses.

The agent would read an invoice, retrieve relevant supplier records and purchase orders, check for discrepancies, and assess the payment's cash consequences. It would then explain whether the invoice is ready for approval, needs further verification, or should be held. For example, a familiar supplier's invoice might contain changed bank details, while another legitimate invoice could create a cash shortage before payroll.

We have built an initial rules-based prototype using fictional business records to test these situations. Our next step is to add document understanding and specialist agents for invoice review, supplier risk, cash assessment, and company policy. During development, people will retain payment approval, and any payment integration will use a sandbox.

## Value Proposition

For business owners, bookkeepers, and finance teams who need to verify supplier bills while keeping enough cash for upcoming expenses, our agent delivers a clear payment recommendation supported by relevant records and cash calculations.

The need is reflected in published research. AFP's 2026 survey found attempted or actual payment fraud at 76% of respondents' organizations in 2025. Separately, the Federal Reserve Banks' 2026 report found that 50% of surveyed small employer firms faced uneven cash flow.

FINALITY aims to reduce the time spent piecing together a payment decision. A reviewer would see what needs attention, why it matters, and what to do next. Our focus is businesses that still assemble these checks manually across separate records. We will evaluate the approach through review time, discrepancies identified, and unnecessary alerts.

## AI-Use Justification

Fixed rules work well for calculating cash balances and enforcing approval limits. AI is useful for interpreting invoices in different formats and connecting their contents with supporting records.

An agentic workflow would go beyond extracting text. It would select relevant checks, call tools to retrieve supplier and purchase-order information, assess cash consequences, and combine the findings into a recommendation. Missing information would prompt a request for verification. A manual process can perform these tasks, but requires someone to gather and compare the records each time.

We plan to use IBM Bob as our development assistant to help organize the code, implement the agents' tools, write tests for cases such as duplicate invoices and changed recipients, debug issues, and maintain documentation. We will review and test its output. IBM watsonx is our proposed platform for the agent workflow. Explicit software rules will continue to control calculations and payment permissions.

## Sources

[1] [AFP, 2026 Payments Fraud and Control Survey](https://www.financialprofessionals.org/training-resources/resources/survey-research-economic-data/details/payments-fraud)

[2] [Federal Reserve Banks, 2026 Report on Employer Firms, p. 3](https://www.fedsmallbusiness.org/-/media/project/clevelandfedtenant/fsbsite/reports/2026/2026-report-on-employer-firms/2026-report-on-employer-firms.pdf)
