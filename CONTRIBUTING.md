# Contribute

Useful work: translation review, original scenario families, simulator/evaluator fixes, collection adapters, and independent reproduction.

- Describe the failure and supply a counterexample.
- Run `python -m unittest discover -s tests -v`.
- Keep task semantics fixed in language comparisons; declare locale explicitly.
- Mark unreviewed translations draft. Disclose AI assistance and credit reviewers with consent.
- Preserve family-level splits, provenance, licenses, and all failed attempts.
- Add no credentials, real patient data, identifying conversations, or unlicensed audio.

Synthetic controls verify code. Model traces support experiments. Neither establishes real-world safety or impact on its own.

## Start with a reproducible result

1. Run the [local quickstart](docs/QUICKSTART.md) to inspect a permission failure, or [reproduce the sales-pilot analysis](docs/SALES_PILOT_FINDINGS.md#inspect-and-reproduce-the-analysis) without downloading a model.
2. Open an issue with the experiment, exact commit, case ID, expected result and observed output. Use fictional data.
3. For language review, identify the language variety and explain whether a translation changes the task meaning. Record reviewer consent before adding attribution.
4. Submit changes with the relevant checks and a clear distinction between code fixes, new cases and new model results. Preserve frozen experiment artifacts; put new runs in separate directories.

The highest-priority research gaps are independent language/domain review, stronger English task competence and untouched situation families for testing whether observed differences generalize.

For the five-domain suite, follow the [language and domain review guide](docs/LANGUAGE_REVIEW_GUIDE.md). The [checkpoint quickstart](docs/DOMAIN_AND_SPEECH_STUDY.md#try-the-checkpoints-locally) exports prompts and scores agent replies without calling an API.
