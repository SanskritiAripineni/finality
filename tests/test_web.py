"""Exercise actual HTTP requests against the local dashboard and existing engine."""
from copy import deepcopy
from http.client import HTTPConnection
import json
from pathlib import Path
from threading import Thread
import unittest

from finality.web import make_server


class DashboardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = json.loads((Path(__file__).resolve().parents[1] / 'data/scenarios.json').read_text())
        cls.original = deepcopy(cls.cases)
        cls.server = make_server(cls.cases, port=0)
        cls.thread = Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=3)

    def request(self, method, path, payload=None, raw=None, headers=None):
        connection = HTTPConnection('127.0.0.1', self.server.server_port, timeout=3)
        body = raw if raw is not None else (json.dumps(payload).encode() if payload is not None else None)
        request_headers = {'Content-Type': 'application/json'}
        request_headers.update(headers or {})
        connection.request(method, path, body=body, headers=request_headers)
        response = connection.getresponse()
        result = response.status, dict(response.getheaders()), response.read()
        connection.close()
        return result

    def post(self, payload):
        status, _, body = self.request('POST', '/api/review', raw=json.dumps(payload).encode())
        return status, json.loads(body)

    def test_all_seven_scenarios_through_http(self):
        for case in self.cases:
            with self.subTest(case=case['id']):
                status, data = self.post({'case_id':case['id']})
                self.assertEqual(status, 200)
                self.assertEqual(data['result']['status'], case['expected_status'])

    def test_edited_recipient_is_held_and_source_records_stay_trusted(self):
        status, data = self.post({'case_id':'normal', 'overrides':{'account_ref':'DEMO-ACCT-B'}})
        self.assertEqual(status, 200)
        self.assertEqual(data['result']['status'], 'HOLD')
        self.assertIn('RECIPIENT_CHANGED', [f['code'] for f in data['result']['findings']])
        self.assertEqual(data['case']['supplier']['approved_account_ref'], 'DEMO-ACCT-A')
        _, clean = self.post({'case_id':'normal'})
        self.assertEqual(clean['result']['status'], 'READY')

    def test_edited_balance_exposes_exact_shortfall(self):
        status, data = self.post({'case_id':'normal','overrides':{'balance_cents':1000000}})
        self.assertEqual(status, 200)
        self.assertEqual(data['result']['status'], 'HOLD')
        self.assertEqual(data['result']['base']['minimum_cents'], 80000)
        self.assertIn('CASH_RESERVE_BREACH', [f['code'] for f in data['result']['findings']])

    def test_edited_amount_preserves_purchase_order(self):
        status, data = self.post({'case_id':'normal','overrides':{'amount_cents':800000}})
        self.assertEqual(status, 200)
        self.assertEqual(data['case']['purchase_order']['amount_cents'],120000)
        self.assertEqual(data['result']['base']['minimum_cents'],400000)
        self.assertIn('ORDER_MISMATCH',[f['code'] for f in data['result']['findings']])

    def test_bad_fields_and_types_never_become_ready(self):
        requests = [None, [], {}, {'case_id':'unknown'}, {'case_id':True},
                    {'case_id':'normal','overrides':None},
                    {'case_id':'normal','overrides':{'verified':True}},
                    {'case_id':'normal','extra':1}]
        for value in (0,-1,True,1.5,'120000',10**12+1):
            requests.append({'case_id':'normal','overrides':{'amount_cents':value}})
        for value in (-1,False,'0'):
            requests.append({'case_id':'normal','overrides':{'balance_cents':value}})
        for value in ('','  ','x'*121,'bad\nref',None,123):
            requests.append({'case_id':'normal','overrides':{'account_ref':value}})
        for payload in requests:
            with self.subTest(payload=payload):
                status, data = self.post(payload)
                self.assertEqual(status,400)
                self.assertIn('error',data)
                self.assertNotIn('result',data)

    def test_zero_balance_is_valid_and_held(self):
        status,data = self.post({'case_id':'normal','overrides':{'balance_cents':0}})
        self.assertEqual(status,200)
        self.assertEqual(data['result']['status'],'HOLD')

    def test_bad_json_and_large_body_rejected(self):
        self.assertEqual(self.request('POST','/api/review',raw=b'{broken')[0],400)
        self.assertEqual(self.request('POST','/api/review',raw=b'x'*8193)[0],413)
        self.assertEqual(self.request('POST','/api/review',raw=b'\xff')[0],400)
        self.assertEqual(self.request('POST','/api/review',raw=b'{}',headers={'Content-Type':'text/plain'})[0],415)

    def test_cross_origin_and_rebound_host_rejected(self):
        self.assertEqual(self.request('POST','/api/review',{'case_id':'normal'},headers={'Origin':'https://example.org'})[0],403)
        self.assertEqual(self.request('GET','/api/scenarios',headers={'Host':'example.org'})[0],403)

    def test_static_routes_and_no_source_exposure(self):
        status,headers,body = self.request('GET','/')
        self.assertEqual(status,200)
        self.assertIn(b'FINALITY',body)
        self.assertIn("frame-ancestors 'none'",headers['Content-Security-Policy'])
        for path in ('/app.js','/style.css'):
            self.assertEqual(self.request('GET',path)[0],200)
        for path in ('/../data/scenarios.json','/finality/engine.py','/.git/config'):
            self.assertEqual(self.request('GET',path)[0],404)

    def test_requests_never_mutate_stored_scenarios(self):
        self.post({'case_id':'normal','overrides':{'amount_cents':999999,'account_ref':'edited','balance_cents':0}})
        _,_,body = self.request('GET','/api/scenarios')
        self.assertEqual(json.loads(body),self.original)
        self.assertEqual(self.cases,self.original)


if __name__ == '__main__':
    unittest.main()
