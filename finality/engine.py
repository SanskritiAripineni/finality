"""Evidence checks and deterministic cash projection. All money is integer cents.

This module has no language model, bank connection, or payment execution capability.
Each review is independent and does not reserve funds for other reviews.
"""
from datetime import date

def money(cents):
    return f"${cents / 100:,.2f}"

def validate(case):
    invoice, company = case["invoice"], case["company"]
    for key in ("amount_cents",):
        if type(invoice[key]) is not int or invoice[key] <= 0:
            raise ValueError("Invoice amount must be a positive integer number of cents")
    for key in ("balance_cents", "minimum_cash_cents", "approval_limit_cents"):
        if type(company[key]) is not int or company[key] < 0:
            raise ValueError(f"{key} must be nonnegative integer cents")
    start, end = date.fromisoformat(company["as_of"]), date.fromisoformat(company["horizon_end"])
    if start > end:
        raise ValueError("Forecast horizon ends before its start")
    if not start <= date.fromisoformat(invoice["pay_on"]) <= end:
        raise ValueError("Payment date must be within the forecast horizon")
    for event in company["cash_events"]:
        date.fromisoformat(event["date"])
        if type(event["amount_cents"]) is not int:
            raise ValueError("Cash events require integer cents")
    return invoice, company

def project_cash(company, invoice, stress=False):
    """Exclude uncertain receipts in stress mode. Same-day outflows precede receipts.

    Conservative ordering avoids assuming receipts arrive before that day's payments.
    Balances are scenario arithmetic, not a trained statistical forecast.
    """
    events = [dict(e) for e in company["cash_events"]
              if company["as_of"] <= e["date"] <= company["horizon_end"]
              and not (stress and e["amount_cents"] > 0 and not e.get("confirmed", False))]
    events.append({"date": invoice["pay_on"], "label": "Proposed supplier payment", "amount_cents": -invoice["amount_cents"]})
    events.sort(key=lambda e: (e["date"], e["amount_cents"] >= 0, e["label"]))
    balance = minimum = company["balance_cents"]
    timeline = []
    for e in events:
        balance += e["amount_cents"]
        minimum = min(minimum, balance)
        timeline.append({**e, "balance_cents": balance})
    return {"minimum_cents": minimum, "closing_cents": balance, "timeline": timeline}

def review(case):
    invoice, company = validate(case)
    supplier = case["supplier"]
    findings = []
    def add(role,code,severity,explanation,evidence):
        findings.append(dict(role=role,code=code,severity=severity,explanation=explanation,evidence=evidence))
    if invoice["currency"] != company["currency"]:
        # Never add unlike currencies. Currency conversion is outside this prototype.
        add("Policy", "CURRENCY_UNSUPPORTED", "hold", "Currency conversion requires review before a cash assessment.", "Invoice currency differs from company currency")
        return {"case_id": case["id"], "title":case["title"], "status":"HOLD", "findings":findings, "base":None, "stress":None, "next_action":"Review currency and provide an approved conversion before reassessment.", "mode":"Deterministic simulation"}
    paid = {(p["supplier_id"],p["invoice_number"].strip().casefold()) for p in case["paid_invoices"]}
    if (invoice["supplier_id"],invoice["invoice_number"].strip().casefold()) in paid:
        add("Invoice", "ALREADY_PAID", "block", "This supplier invoice already appears in the paid ledger.", "Supplier ID and normalized invoice number match a paid record")
    if not supplier.get("verified") or supplier["id"] != invoice["supplier_id"]:
        add("Risk", "SUPPLIER_UNVERIFIED", "hold", "The supplier lacks a matching verified record.", "Supplier master record")
    if supplier["approved_account_ref"] != invoice["account_ref"]:
        add("Risk", "RECIPIENT_CHANGED", "hold", "Payment details differ from the approved supplier record.", "Approved reference: " + supplier["approved_account_ref"] + "; invoice reference: " + invoice["account_ref"])
    if not case.get("purchase_order"):
        add("Invoice", "SUPPORT_MISSING", "review", "No purchase order supports this invoice.", "Purchase order unavailable")
    elif case["purchase_order"]["supplier_id"] != invoice["supplier_id"] or case["purchase_order"]["amount_cents"] != invoice["amount_cents"]:
        add("Invoice", "ORDER_MISMATCH", "hold", "Invoice supplier or amount does not match the purchase order.", "Purchase order " + case["purchase_order"]["id"])
    if invoice["amount_cents"] >= company["approval_limit_cents"]:
        add("Policy", "APPROVAL_REQUIRED", "review", "The amount meets or exceeds the manager approval limit.", "Configured limit: " + money(company["approval_limit_cents"]))
    if invoice["amount_cents"] > supplier["typical_invoice_cents"] * 2:
        add("Risk", "UNUSUAL_AMOUNT", "review", "The amount is more than twice this supplier's typical invoice.", "Synthetic typical amount: " + money(supplier["typical_invoice_cents"]))
    base, stress = project_cash(company, invoice), project_cash(company, invoice, stress=True)
    floor = company["minimum_cash_cents"]
    if base["minimum_cents"] < floor:
        add("Treasury", "CASH_RESERVE_BREACH", "hold", "The proposed payment leaves projected cash below the required reserve.", "Base minimum " + money(base["minimum_cents"]) + "; reserve " + money(floor))
    elif stress["minimum_cents"] < floor:
        add("Treasury", "RECEIPT_DEPENDENCY", "review", "Cash stays above reserve only if expected, unconfirmed receipts arrive.", "Without unconfirmed receipts, minimum cash is " + money(stress["minimum_cents"]))
    if not findings:
        add("Policy", "CHECKS_PASSED", "info", "Available records match and both cash scenarios remain above reserve.", "Supplier record, purchase order, paid ledger, cash schedule, and policy")
    status = next((status for severity,status in [("block","BLOCK"),("hold","HOLD"),("review","REVIEW")] if any(f["severity"] == severity for f in findings)), "READY")
    actions = {"BLOCK":"Do not proceed. Reconcile the paid ledger before creating another request.","HOLD":"Resolve the evidence or cash exception, then run the checks again.","REVIEW":"Ask a manager to review the cited evidence and assumptions.","READY":"Ready for the next approval step. This prototype does not send money."}
    return {"case_id":case["id"],"title":case["title"],"status":status,"findings":findings,"base":base,"stress":stress,"next_action":actions[status],"mode":"Deterministic simulation"}
