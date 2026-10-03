# CBOS Article + Image execution

Implemented 2026-10-02 in the existing Hugo site. Python 3.10+, standard library.
CBOS source remains D:\CBOS. No existing writer, article, key or theme is replaced.

## Workflow

### Legacy writer safety update — 2026-10-02

`auto-publish.bat` now performs a read-only preflight. It does not elevate privileges,
remove Git locks, call a paid generator, or publish automatically. `tudong_gemini.py`
requires explicit `--generate-draft` for an existing paid Claude call. It skips any
slug already present (including drafts), limits selection to one candidate, requires
a reviewed image, and writes `draft: true`. Today's live publication blocks generation;
lastmod refreshes do not count as new posts. Day boundaries use UTC+07:00.

This writer is not the production publishing executor. `push_to_github` fails closed;
reviewed publication still uses the bridge below. No paid generation was run in this
update. Scheduled Task inspection found no named AIPro/CBOS/Claude/Blog publishing
task; this does not establish the absence of differently named or external schedulers.

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
this task. The legacy auto-publish.bat/tudong_gemini.py now defaults to read-only
preflight; paid draft generation requires its explicit generation flag and its
Git push function is disabled. Reviewed publication uses this executor. No new
schedule is created.

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

## Daily publication check — October 3 update

Before reserving a journal day, publish reads existing posts in both YAML and JSON
frontmatter. A live post whose publication date falls on the current Asia/Saigon
day blocks another publication, including a post added manually. Offset-aware
timestamps are converted to Vietnam time; drafts do not consume the daily limit.
The journal still serializes cooperating bridge executors and retains unknown
write outcomes for inspection. Direct Git edits can bypass the executor, so an
operator making a manual publication must also check the same inventory first.

Current validation: 17 bridge tests, 6 content preflight tests and 2 JSON inventory
tests passed. These are local tests, not evidence of remote publication or revenue.
Two prepared guides remain draft:true and must not be counted as live articles.
For a read-only daily operator summary, run:
`python -B tools/daily_status.py --output D:\CBOS_workspace\AIPRO_DAILY_STATUS.md`.
It reads current repository inventory and cached catalog evidence, without browser,
provider, publishing, or payment calls. Live results still require dashboard readback.
After building, compare account-issued catalog URLs with rendered links using
`python -B tools/affiliate_audit.py <build-directory>`. This checks local account
paths/fragments, unexpected query keys and sponsored/tracking markers for the four
catalog programs; it does not verify redirects, cookie attribution or conversions.
GitHub Pages runs the inventory/audit tests, tracking privacy checks and both
rendered-site audits before uploading its production artifact. Both the executor
and CI exclude future-dated content; review previews may include future drafts.
Do not use --buildDrafts or --buildFuture for production publication just to meet
an article KPI; previewing future drafts is a separate local review operation.

Murf referral anchors use `rel="sponsored noopener"` with
`referrerpolicy="strict-origin"`: HTTPS referrals send the website origin only,
without the article path or query. This avoids the source masking caused by
`noreferrer`, which conflicts with Murf's public affiliate terms:
https://murf.ai/legal/affiliate-program-terms-of-service . Other catalog programs
retain their existing `noreferrer` policy. Four affiliate audit tests include
regressions for masked, missing and overly permissive Murf policies. This is a
referral-source compatibility fix, not proof of account approval or attribution.
