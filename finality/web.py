"""Local-only interactive demo over the existing deterministic review engine."""
from copy import deepcopy
from functools import partial
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from urllib.parse import urlsplit

from .engine import review

STATIC = Path(__file__).with_name("static")
MAX_BODY = 8192
MAX_CENTS = 10**12


def review_request(cases, payload):
    """Accept only controlled edits to a known synthetic case; never mutate it."""
    if not isinstance(payload, dict) or set(payload) - {"case_id", "overrides"}:
        raise ValueError("Provide a case_id and optional overrides only.")
    case_id = payload.get("case_id")
    if not isinstance(case_id, str):
        raise ValueError("Select a sample scenario.")
    source = next((c for c in cases if c["id"] == case_id), None)
    if source is None:
        raise ValueError("Unknown sample scenario.")
    edits = payload.get("overrides", {})
    if not isinstance(edits, dict) or set(edits) - {"amount_cents", "account_ref", "balance_cents"}:
        raise ValueError("Only amount, recipient reference, and starting balance can be edited.")
    case = deepcopy(source)
    for name, minimum in (("amount_cents", 1), ("balance_cents", 0)):
        if name in edits:
            value = edits[name]
            if type(value) is not int or not minimum <= value <= MAX_CENTS:
                raise ValueError(f"{name} must be integer cents between {minimum} and {MAX_CENTS}.")
            target = case["invoice"] if name == "amount_cents" else case["company"]
            target[name] = value
    if "account_ref" in edits:
        value = edits["account_ref"]
        if not isinstance(value, str) or not value.strip() or len(value) > 120 or not value.isprintable():
            raise ValueError("Recipient reference must contain 1–120 printable characters.")
        case["invoice"]["account_ref"] = value.strip()
    return {"case": case, "result": review(case)}


class DemoHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, cases, **kwargs):
        self.cases = cases
        super().__init__(*args, **kwargs)

    def respond(self, status, body, content_type="application/json; charset=utf-8"):
        if not isinstance(body, bytes):
            body = json.dumps(body, allow_nan=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(body)

    def local_request(self):
        host = self.headers.get("Host", "")
        allowed = {f"127.0.0.1:{self.server.server_port}", f"localhost:{self.server.server_port}"}
        if host not in allowed:
            self.respond(403, {"error": "Use the localhost address printed by FINALITY."})
            return False
        return True

    def do_GET(self):
        if not self.local_request():
            return
        path = urlsplit(self.path).path
        if path == "/api/scenarios":
            self.respond(200, self.cases)
            return
        assets = {"/": ("index.html", "text/html; charset=utf-8"),
                  "/app.js": ("app.js", "text/javascript; charset=utf-8"),
                  "/style.css": ("style.css", "text/css; charset=utf-8")}
        if path not in assets:
            self.respond(404, {"error": "Not found."})
            return
        filename, content_type = assets[path]
        self.respond(200, (STATIC / filename).read_bytes(), content_type)

    def do_POST(self):
        if not self.local_request():
            return
        if urlsplit(self.path).path != "/api/review":
            self.respond(404, {"error": "Not found."})
            return
        origin = self.headers.get("Origin")
        if origin and origin != "http://" + self.headers["Host"]:
            self.respond(403, {"error": "Cross-origin review requests are not allowed."})
            return
        if self.headers.get_content_type() != "application/json":
            self.respond(415, {"error": "Send the review request as application/json."})
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            size = 0
        if not 0 < size <= MAX_BODY:
            self.respond(413, {"error": "Review request must be between 1 and 8192 bytes."})
            return
        try:
            payload = json.loads(self.rfile.read(size))
            result = review_request(self.cases, payload)
        except (ValueError, UnicodeDecodeError) as exc:
            self.respond(400, {"error": str(exc)})
            return
        self.respond(200, result)

    def log_message(self, format, *args):
        # The local demo has no user identities or payment credentials to log.
        return


def make_server(cases, port=8000):
    return ThreadingHTTPServer(("127.0.0.1", port), partial(DemoHandler, cases=deepcopy(cases)))


def serve(cases, port=8000):
    with make_server(cases, port) as server:
        print(f"FINALITY interactive demo: http://127.0.0.1:{server.server_port}", flush=True)
        print("Synthetic records only. No funds move. Press Ctrl+C to stop.", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nDemo stopped.")
