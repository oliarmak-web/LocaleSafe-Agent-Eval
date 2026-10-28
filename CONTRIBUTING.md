# Contribute to LocaleSafe

Help make multilingual agent evaluation more reliable. **Review a translation, reproduce a finding or contribute a new failure case.** You do not need a GPU or paid API to get started.

## Choose a starting point

### 1. Review a language or domain case

Check whether a request preserves corrections, permission, conditions, dates and record IDs. Flag ambiguous wording or unrealistic policy assumptions. Independent review is the highest-priority research need.

**Submit:** case ID, language variety and locale, original wording, proposed change and a short explanation. State your relevant language/domain experience and any AI assistance. Use the [language-review issue form](https://github.com/oliarmak-web/LocaleSafe-AI-Agentic-Demo/issues/new?template=language-review.yml); the [review guide](docs/LANGUAGE_REVIEW_GUIDE.md) explains what to check.

**Acceptance:** explain how the wording or policy affects the expected action, including competing interpretations where relevant. Accepted corrections go into a new versioned case set with review provenance; frozen cases and published scores stay intact. Reviewer attribution requires consent.

### 2. Reproduce a finding

Run an archived study's scoring with Python 3.11+. Start with the [reproduction guide](docs/QUICKSTART.md); no model download or inference is needed.

**Submit:** experiment name, exact commit, command, Python version and observed result. For a discrepancy, include the expected result, case ID if applicable and a minimal error log. Open an [issue](https://github.com/oliarmak-web/LocaleSafe-AI-Agentic-Demo/issues).

**Acceptance:** another contributor can follow the steps and verify the result or reproduce the discrepancy. Report mismatches as well as successful reproductions; do not repair raw model replies to match a score.

### 3. Add a failure case

Write a fictional request where an agent could lose a correction, confuse a record, misapply a policy or act without current permission. New situation families are especially useful. Start with the [checkpoint export and scoring guide](docs/DOMAIN_AND_SPEECH_STUDY.md#try-the-checkpoints-locally).

**Submit:** visible request and policy, expected action, explanation and a minimal example. Label any supplied response as model-generated or synthetic. For model outputs, retain the untouched reply, model revision, prompt and generation settings. Discuss a new case in an [issue](https://github.com/oliarmak-web/LocaleSafe-AI-Agentic-Demo/issues) before expanding it into a large dataset.

**Acceptance:** the expected action follows from the supplied evidence, ambiguity is documented and provenance is clear. Language comparisons must preserve task meaning and declare locale explicitly. Unreviewed translations remain marked draft. New cases must not overwrite frozen studies or leak into their evaluation splits.

## Before opening a pull request

- Explain what changed, why and how you checked it. Link the relevant issue when available.
- For code or evaluator changes, run `python -m unittest discover -s tests -v` and include a focused counterexample for a behavior fix. For documentation-only changes, verify affected instructions and links.
- Preserve archived inputs, outputs, failed attempts, family-level splits and hashes. Put new runs in separate directories; distinguish code fixes, new fixtures and new model results.
- Disclose AI assistance and source licenses. Add no credentials, private conversations, identifying patient/customer data or unlicensed recordings. See [security guidance](SECURITY.md).

Synthetic cases test the evaluator; recorded model outputs support bounded experiments. Neither alone establishes production safety or a general language ranking.

For study context and evidence, see the [research index](docs/RESEARCH_INDEX.md). Evaluator fixes, model adapters and independent replications are also welcome.
