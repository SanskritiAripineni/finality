import json
import unittest
from copy import deepcopy
from pathlib import Path
from finality.engine import review, project_cash
from finality.report import render

CASES=json.loads((Path(__file__).resolve().parents[1]/'data/scenarios.json').read_text())

class ReviewTests(unittest.TestCase):
    def test_all_scenario_outcomes(self):
        for case in CASES:
            with self.subTest(case=case['id']):
                self.assertEqual(review(case)['status'],case['expected_status'])
    def test_cash_shortfall_arithmetic(self):
        result=review(CASES[3])
        self.assertEqual(result['base']['minimum_cents'],400000)
        self.assertEqual(result['stress']['minimum_cents'],400000)
    def test_stress_excludes_only_unconfirmed_receipts(self):
        result=review(CASES[6])
        self.assertEqual(result['base']['minimum_cents'],880000)
        self.assertEqual(result['stress']['minimum_cents'],480000)
    def test_duplicate_normalization_and_precedence(self):
        c=deepcopy(CASES[1]);c['paid_invoices']=[{'supplier_id':'SUP-001','invoice_number':' INV-1008 '}]
        self.assertEqual(review(c)['status'],'BLOCK')
    def test_currency_mismatch_does_not_compute_cash(self):
        c=deepcopy(CASES[0]);c['invoice']['currency']='EUR'
        r=review(c);self.assertEqual(r['status'],'HOLD');self.assertIsNone(r['base'])
    def test_negative_and_fractional_amounts_rejected(self):
        for value in (-100,0,1.5,True):
            c=deepcopy(CASES[0]);c['invoice']['amount_cents']=value
            with self.assertRaises(ValueError):review(c)
    def test_threshold_boundary_requires_review(self):
        c=deepcopy(CASES[0]);c['company']['approval_limit_cents']=c['invoice']['amount_cents']
        self.assertEqual(review(c)['status'],'REVIEW')
    def test_cash_reserve_boundary_is_allowed(self):
        c=deepcopy(CASES[0]);c['company']['balance_cents']=1420000
        self.assertEqual(review(c)['status'],'READY')
    def test_out_of_horizon_payment_rejected(self):
        c=deepcopy(CASES[0]);c['invoice']['pay_on']='2027-01-01'
        with self.assertRaises(ValueError):review(c)
    def test_outside_horizon_cash_events_ignored(self):
        c=deepcopy(CASES[0]);c['company']['cash_events'].append({'date':'2027-01-01','amount_cents':-99999999,'label':'Outside horizon'})
        self.assertEqual(review(c)['base'],review(CASES[0])['base'])
    def test_same_day_receipt_does_not_mask_shortfall(self):
        c=deepcopy(CASES[0]);c['company']['balance_cents']=550000
        c['company']['cash_events']=[{'date':c['invoice']['pay_on'],'label':'Receipt','amount_cents':1000000,'confirmed':True}]
        self.assertEqual(review(c)['status'],'HOLD')
    def test_supplier_mismatch_is_held(self):
        c=deepcopy(CASES[0]);c['supplier']['id']='SUP-OTHER'
        self.assertEqual(review(c)['status'],'HOLD')
    def test_report_escapes_untrusted_text(self):
        c=deepcopy(CASES[0]);c['title']='<script>alert(1)</script>'
        html=render([c],[review(c)])
        self.assertNotIn('<script>',html);self.assertIn('&lt;script&gt;',html)
    def test_review_does_not_mutate_input(self):
        c=deepcopy(CASES[0]);before=deepcopy(c);review(c);self.assertEqual(c,before)

if __name__=='__main__':unittest.main()
