# Astro Lab site instructions

These instructions govern work in this repository. The site is the public page
for the TJHSST Laboratory for Astronomy & Astrophysics Research:

<https://activities.tjhsst.edu/astro/>

## Purpose and audience

Build a useful working record of the lab for:

- current senior-research students;
- younger TJ students considering Astro Lab;
- families, educators, researchers, and organizations interested in the lab's
  existing work or a future collaboration.

The site should sound established, direct, and open: this is what the lab does
and what its students have produced; interested people are welcome to learn
more or make contact.

Do not write as though the site is selling a program, announcing an aspiration,
or asking the visitor to trust a new institution. Avoid slogans, generic claims
about excellence or innovation, and promotional boilerplate. Prefer factual
labels such as `Research archive`, `Partners`, `Contact`, and `2025-26 projects`.

## Visual character

Preserve the current dark, restrained institutional theme in `assets/site.css`.
The lab site defines the preferred visual direction; do not import older AA@TJ
CSS conventions into this repository.

- Useful content should begin high on the page.
- Do not introduce full-viewport or hero-first layouts that make the first
  routine action a scroll. The landing page may use a larger title, but it must
  still expose a useful action and current information promptly.
- Ordinary page titles should remain substantially smaller than the landing
  title. As of the current design, desktop landing/title/record scales are
  approximately 59/41/41 px, with ordinary phone titles around 30-32 px.
- Keep headings subordinate to content. Do not let one-line page titles occupy
  a large fraction of the viewport.
- Prefer compact, aligned grids and cards over large empty areas. Partners and
  Contact are reference pages for the intended density.
- Use color and emphasis sparingly. The muted red tjSTAR deadline treatment is
  intentional; it should feel quiet but consequential.

Any substantial typography, spacing, or navigation change requires rendered
comparison at 1280, 768, 390, and 320 CSS pixels. Confirm the actual
`window.innerWidth`; do not infer that a viewport override succeeded.

## Architecture and source of truth

This is a dependency-free generated static site intended to work from a raw Git
checkout in the Director `public` directory.

- `data/site.json` is authoritative for navigation, professional profiles,
  partners, TJ labs, years, project records, collaboration metadata, and
  artifact links.
- `scripts/build_site.py` is authoritative for page templates.
- `assets/site.css` and `assets/countdown.js` are the shared presentation layer.
- Generated HTML is committed for deployment, but should not be edited by hand.
- Retained papers and posters are public research artifacts. Do not alter,
  replace, redact, or remove them without explicit direction.

Prefer shared data and generation over manually duplicated navigation or page
lists. Preserve stable public URLs unless a redirect or compatibility plan is
part of the change.

## Content rules

### Research records

Project pages are concise public records, not reproductions of papers or
mini-posters. They should let a visitor understand the question, significance,
method, and supported result quickly, then link to retained artifacts.

- Ground scientific claims in the retained paper, poster, tjSTAR record, or
  another identified authoritative source.
- Distinguish demonstrated results from interpretation, limitations, and future
  work.
- Every `Paper`, `Poster`, and `tjSTAR record` label shown on a card must be a
  real direct link.
- Use the exact visible spelling `tjSTAR` throughout.

### Student identity

The HTML site intentionally deemphasizes student identities.

- Public project credits are permitted only when the project has
  `external_collaboration: true` and a public `collaboration` description.
- The checker must reject credits that do not satisfy that rule.
- Papers and posters retain their original authorship unless an administrator
  explicitly requires artifact redaction or replacement.
- Do not reintroduce student names elsewhere in cards, summaries, metadata, or
  navigation as a workaround.

### Partners and external institutions

- Use restrained, supportable descriptions of relationships. Do not imply a
  formal, current, or project-specific partnership beyond the available record.
- Link only to verified current institutional pages.
- Do not link stale legacy lab sites merely to make a card clickable.
- Do not hotlink logos. Official marks must be stored locally, come from an
  approved or clearly authoritative source, and be recorded with provenance.
- When a visible organization name accompanies a decorative logo, use empty alt
  text for the logo to avoid duplicate accessible names.

### Astro at TJ family

Keep the lab connected minimally to Classes, Astro Club, Astro Team, and related
TJ research pages without importing their implementations or CSS systems.
Non-clickable placeholders are acceptable only when deliberately requested and
must not be disguised as links.

## Accessibility and responsive behavior

Every generated page should have:

- one `h1` and a logical heading sequence;
- a working skip link and labelled navigation landmarks;
- visible keyboard focus;
- meaningful link text and no empty destinations;
- no unintended page-level horizontal overflow;
- keyboard order matching visual order;
- readable layouts at 1280, 768, 390, and 320 px.

The primary navigation should remain fully discoverable on phones. The Astro at
TJ family strip may scroll horizontally, but it needs a visible overflow cue.

## Audit and implementation workflow

For meaningful changes:

1. Audit the rendered pages, source data, links, and relevant authoritative
   external pages before editing.
2. State which requirements are clear enough to implement and which depend on
   missing URLs, source material, permissions, or an owner decision.
3. Edit the generator, data, or shared assets rather than generated HTML.
4. Regenerate all managed pages.
5. Run the complete validation suite.
6. Perform a final adversarial review of content claims, privacy, page hierarchy,
   links, accessibility, and responsive behavior.
7. Repair blockers before committing. Record genuine evidence-dependent gaps in
   `PROJECT_HANDOFF.md` or the pull request rather than fabricating a completion.

Required validation:

```sh
python3 scripts/build_site.py
python3 scripts/build_site.py --check
python3 scripts/check_site.py
python3 scripts/test_generation.py
node scripts/test_countdown.mjs
git diff --check
```

Visual review must use an HTTP preview, not `file://`.

## Git and deployment boundaries

- Work on a focused `codex/` branch unless the user directs otherwise.
- Keep commits narrow and describe intentionally deferred work in the PR.
- Do not merge a PR, pull in Director, or claim public deployment without
  explicit authorization.
- Report lifecycle state literally: implemented locally, tested, committed,
  pushed, under review, merged, pulled to Director, and anonymously verified are
  different states.
- After an authorized Director pull, verify the exact public routes and artifact
  links anonymously. A successful Git push is not a deployment.

The GitHub repository is the source authority. The TJHSST Director checkout is
the delivery path; server-side edits should not become a second source of truth.

