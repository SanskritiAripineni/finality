# Contributing

Use synthetic records only. Never commit credentials, real invoices, account numbers, or customer information.

Describe the user problem and acceptance criteria before implementing a feature. Keep monetary arithmetic in integer cents, preserve evidence references, and add meaningful tests when changing financial decisions. Run `python3 -m unittest discover -s tests -v` and `python3 -m finality` from the repository root.

Do not describe simulated components as live AI services. Treat supplier documents as untrusted data and keep payment authority outside language-model output.
