# AIProFreelancer editorial images — v2

Use this standard when preparing Article + Image packages. Create original art
with the built-in imagegen tool in the chat; this is not an unattended image API.
The legacy writer consumes approved images from data/reviewed_covers.json.
Unmapped articles retain their existing fallback. No paid image API is enabled.

## Visual brief

- One recognizable subject that directly matches the article's buying decision.
- Landscape approximately 16:9; dark navy, cyan accent and restrained orange light
  for hosting. Vary the subject and composition for other categories.
- Main headline 3–6 words, at most two lines. Optional short benefit subtitle.
- Keep important content inside generous safe margins. Inspect at 360px width.
- Original editorial art; do not fabricate vendor screenshots, logos, awards,
  prices, benchmark results, ratings or earnings.
- Avoid excessive props, tiny captions and copying the entire article title.
- Save a versioned image in static/images. Keep old assets. Encode as WebP for
  delivery, ideally under 250 KB, without altering the approved composition.
- Inspect actual image text and crop, then update the article cover and alt text.
- Record provenance and approval in reviewed_covers.json. Build, audit and verify
  the live image URL after publication. Visual quality is not proof of higher CTR.

## Approved sample prompt

Create a premium landscape editorial cover for the UltaHost VPS buying checklist.
A prominent physically rendered dark server tower, electric cyan accent and
restrained orange rim lighting on midnight blue. Three subtle visual objects
represent cost planning, backup storage and deployment readiness. Clear negative
space and readable typography. Exact headline: “VPS BUYING GUIDE”. Exact subtitle:
“Cost · Backups · Setup”. Small brand: “AIProFreelancer”. Generous safe margins;
readable at small card size. No provider logos, ratings, prices, speed claims or
fake service UI. Conceptual editorial illustration, not a provider screenshot.

Generated 2026-10-02 using built-in imagegen. Reviewed text and composition; output
1672×941. Published asset: /images/ultahost-vps-cover-v2.webp.
