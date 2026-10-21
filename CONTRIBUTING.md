# Contributing

Useful contributions include independent translation reviews, well-specified scenario families, evaluator bug fixes, collection adapters, and external reproductions. Start with an issue describing the failure or proposed extension. Never claim a fixture result is an empirical model result.

Run `python -m unittest discover -s tests -v` and the README example before submitting. For metric changes, supply counterexamples that would be scored incorrectly before the change. Preserve schema compatibility or document a version change. Do not bundle formatting-only edits with scoring changes.

New scenarios need provenance, permitted redistribution, expected decisions/actions, split assignment, and all paired translations in the same split. Add no real patient data, identifying conversations, credentials, or unlicensed audio. Mark unreviewed translations draft. Disclose AI assistance and credit human reviewers with permission.

For results, provide reproducible manifests and distinguish hypotheses, synthetic checks, and measured findings. Research ownership and affiliation must be accurate; organizational attribution is not assumed.
