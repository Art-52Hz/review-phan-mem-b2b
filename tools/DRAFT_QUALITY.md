# Legacy Claude draft quality check

`tudong_gemini.py` now calls `validate_generated_draft` before creating the
article directory or writing Markdown. This path has no supplied test records,
so numeric ratings (including rating metadata) and first-person testing claims
are rejected with `DraftReviewRequired`. The rejected text is not saved by this
writer and no automatic publication follows. An operator must review the cause;
this check does not request another model response.

The prompt also stops requiring a predetermined winner, invented current
prices, or a minimum word count. Missing vendor facts must be marked for review.
Sample exercises must be labelled as proposed, not completed tests.

This is a conservative text check, not a fact checker. It can reject a quoted
rating or legitimate testing sentence because this generation route has no
verified evidence attached. It does not catch every unsupported claim, evaluate
sources, inspect image text, approve affiliate links or establish legal rights.
It does not scan or automatically alter existing published articles, and does
not cover a different authoring route such as CBOS bundles or manual Markdown.

Every accepted draft still needs source review, current plan/offer verification,
image review and the existing explicit publication handoff. A passing test or
saved draft is not evidence of Google indexing, attribution or revenue.

Offline verification, without credentials or paid model calls:

```text
python -B -m unittest discover -s tests -p test_draft_quality.py
```

The integration test loads only the writer's save function, not the module's
credential-loading code. It proves rejected content creates neither an article
nor its parent directory. CI and the local Hermes check run this test suite.
