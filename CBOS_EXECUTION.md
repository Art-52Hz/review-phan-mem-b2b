# CBOS Article + Image execution

Implemented 2026-10-02 in the existing Hugo site. Python 3.10+, standard library.
CBOS source remains D:\CBOS. No existing writer, article, key or theme is replaced.

## Workflow

1. Strategy uses the 13-step framework: niche/offer evaluation; customer segments
   and geography; unmet needs and benefits; key message/channel; content/tracking;
   traffic pilot; optimize only from measured results.
2. Research and Article + Image review produce a Sprint 011 review bundle.
3. `cbos_bridge.py stage` rebuilds that bundle through CBOS, compares manifest and
   all file bytes, verifies image hashes, then writes a fresh Hugo draft package.
4. Operator reviews the package and approves its exact receipt SHA-256.
5. `import-draft` imports that approved package into this website, still draft=true.
6. `publish` is the explicit publishing action. It promotes the approved draft,
   builds Hugo, commits only package files and pushes the existing main branch.
   Existing GitHub Pages workflow handles deployment. PUSHED_DEPLOY_PENDING is
   not evidence of successful deployment, visible article, indexing or revenue.

Commands from this repository (paths are examples, not supplied live inputs):

```powershell
python -B cbos_bridge.py stage --bundle C:\private\review-BUNDLEID --output C:\private\staging --slug article-slug
python -B cbos_bridge.py import-draft --package C:\private\staging\PACKAGE --approve-sha256 RECEIPT_HASH
python -B cbos_bridge.py publish --package C:\private\staging\PACKAGE --approve-sha256 RECEIPT_HASH --journal C:\private\publication-journal
```

Output/staging/journal directories must already exist. Keep them outside Git.
Fixtures need --allow-fixture for staging and can never be imported/published.
PARTIAL bundles are rejected. Existing articles are never overwritten on import.
The content remains the reviewed CBOS article; the adapter does not turn audit
labels into marketing copy, translate it or invent product experience.

## Publication boundary

Publication checks the exact imported files, requires main, empty staging index,
no unrelated tracked edits, and local/remote main equality. It reserves one local
publication attempt per Asia/Saigon calendar day in an external journal. Use one
shared journal for all runs. Reusing a daily journal file is rejected.
Unknown/failed attempts keep their reservation and require inspection. No retry,
force push, git add ., lock deletion, broad privilege elevation, browser or paid
provider calls. Site credentials remain in the existing Git/user environment.

This is an operator-invoked local executor, callable by an existing Hermes process
with exact arguments. No Hermes installation/service was located or connected in
this task. The legacy auto-publish.bat/tudong_gemini.py remains a separate unsafe
publication path; do not run it alongside this executor. No new schedule is created.

## Validation and limits

Run `python -B -m unittest discover -s tests -p "test_cbos_bridge.py"`.
Tests use synthetic CBOS data and temporary local repositories. Publication tests
push to a local bare repository with Hugo mocked; a separate actual Hugo build
verifies the website. No provider generation, live post or live revenue is proven.

The marked affiliate links in CBOS articles render with rel=sponsored and a local
tracking script. It sends affiliate_click to the site's already configured GA
only when gtag is available and Do Not Track is not enabled. Event payload includes
destination domain and article pathname, never referral parameters or link text.
It does not infer conversions or attach SubIDs. Legacy unmarked affiliate links
are not automatically reclassified. Actual GA event ingestion is unverified.

Validation completed: 16 bridge tests; six tracking scenarios; a retained fixture
passed the real CLI and actual Hugo rendering, including images/affiliate markers.
Full CBOS regression: 601 run, 597 passed, four skipped. Full Hugo site build passed.
Offline demo: D:\CBOS_workspace\aipro-execution-smoke-20261002-v3\SMOKE_RESULT.json.

At most 30 minutes/day is an operating target, not a verified outcome. Start by
reviewing one ready package, delivery state, affiliate status and actual traffic;
record operator time. Missing source evidence/rights/links blocks publication.
