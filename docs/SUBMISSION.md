# Final submission checklist

## Verified implementation

- Start from the repository root with Python 3.9+: `python3 -m finality --serve`.
- Open http://127.0.0.1:8000 on the same computer.
- Seven fictional cases produce READY, REVIEW, HOLD, or BLOCK using the existing Python policy engine.
- Edit invoice amount, recipient reference, or opening balance, then rerun the review.
- Read the findings, supporting records, required next action, and dated base/stress cash timelines.
- Export reviewed inputs and the decision as JSON. Export is disabled when inputs change until review succeeds.
- The original `python3 -m finality` offline report command remains available.
- Run `python3 -m unittest discover -s tests -v` before recording or publishing changes.

## Submission materials

1. Publicly accessible three-minute video URL; verify it without signing in.
2. Written problem and solution statement, no more than 500 words.
3. Written technology statement describing actual IBM Bob use, no more than 500 words.
4. Code repository containing the demonstrated version and required Bob task-session evidence.

The program guide also mentions a working-prototype link. The dashboard is local-only; its localhost URL will not work on another person's computer. Provide repository run instructions and, if the form requires a public prototype link, arrange hosting or ask the program support team what link they accept. Do not represent a localhost URL as a public deployment.

## Bob evidence still requires capture

In Bob IDE, open Tasks, select the relevant FINALITY task, and select its header to display the task-session consumption summary. Save a screenshot of that summary. Include screenshots for all relevant tasks in `bob_sessions/` before submitting. An account subscription screen is not a substitute for task evidence. Do not include authentication callback URLs, credentials, or unrelated private information in screenshots.

Bob's completed repository-assessment session is confirmed. Any additional review or test-generation task must finish and be inspected before claiming its contribution.

## Demo sequence

1. Ordinary invoice: $1,200, trusted account DEMO-ACCT-A, READY.
2. Changed recipient: invoice has DEMO-ACCT-B while trusted account remains DEMO-ACCT-A, HOLD.
3. Cash shortfall: legitimate $8,000 invoice leaves minimum cash of $4,000 versus a $5,000 reserve, HOLD.
4. Optional: uncertain receipt case has base minimum $8,800 and stress minimum $4,800, REVIEW.
5. State the current limits and next steps honestly.

## Final checks requiring the team

- The public video is uploaded and playable.
- Bob session-summary screenshots are included in the submitted code revision.
- Both statements describe only completed, verified features.
- The correct team member submits through My Teams → Submissions and verifies a submission entry/status.
- Mandatory SkillsBuild learning activities are completed and marked complete.
- The exact November 22 cutoff time has not been confirmed; the daily counter's midnight EST reset is not deadline evidence.

## Current limitations

No connected runtime AI, document extraction, trained fraud classifier, statistical forecast, authenticated approvals, persistent audit database, shared cash reservations, or payment execution. Every scenario is synthetic and independent. The exported JSON is a decision snapshot, not a tamper-proof audit system. READY means the implemented checks passed; it does not authorize payment. Existing presentation PDFs describe earlier project stages and should not be used to claim planned features work.
