# Astro Lab site handoff

Last updated: 2026-08-30

## Current state

The first substantial implementation was merged through PR #2:

<https://github.com/wdlinch3/astro_site/pull/2>

Through implementation commit `1c160a5`, the site contains:

- the landing page, Research, About, Partners, TJ Labs, and Contact;
- a 2025-26 archive with eight concise project records;
- retained paper, poster, and filtered tjSTAR links;
- the Astro at TJ family strip;
- a May 19, 2027 tjSTAR countdown;
- professional profile links for William D. Linch III;
- responsive layouts audited at 1280, 768, 390, and 320 px;
- the privacy rule that exposes HTML student credits only for explicitly marked
  external collaborations.

The documentation in `AGENTS.md` and this handoff was merged through PR #3:

<https://github.com/wdlinch3/astro_site/pull/3>

On 2026-08-30, an anonymous verification found the generated site live at
<https://activities.tjhsst.edu/astro/>. All 15 generated HTML pages, both shared
CSS/JavaScript assets, and all 12 retained papers/posters were retrievable and
byte-identical to `origin/main` at merge commit `5b090cd`. The required 1280,
768, 390, and 320 CSS-pixel reviews confirmed the actual `window.innerWidth`,
fully discoverable primary navigation, and no page-level horizontal overflow.
Each filtered tjSTAR link returned exactly one matching presentation. The other
external links resolved to their intended current targets; NRL's homepage was
browser-verified after its automated HTTP check returned a bot-protection 403.

This evidence confirms the public result, but not the delivery mechanism. It
does not establish whether Director's `public` directory was updated with
`git pull --ff-only` or by another action.

## Current review and deployment gates

1. An independent source audit of the eight public scientific summaries and the
   V-SPARC credit disclosure was completed on 2026-08-30 against the retained
   papers/posters. The summaries remained appropriately concise and cautious;
   one primordial-feedback sentence was clarified to describe the initialized
   central black-hole mass and the explicitly omitted direct radiative feedback.
   Author approval is still required.
2. Confirm with Tiger that Director's `public` directory should remain a Git
   checkout and that direct server-side edits are outside the normal workflow.
3. Before the next deployment, confirm the intended revision on `main`, then use
   `git pull --ff-only` in the Director checkout after authorization.
4. After every deployment, repeat anonymous verification of the homepage,
   primary pages, project records, artifacts, family links, and mobile behavior.

## Content and links still needed

### Retained artifact review

- The V-SPARC HTML credit uses the four students named on the retained poster
  and the live tjSTAR record. The retained paper's title page names only Aarushi
  Kanigicherla and Sarah Trainer. Keep the four-name disclosure pending explicit
  author confirmation; do not infer that the shorter paper byline supersedes the
  poster and tjSTAR record.
- The retained SPINNI poster contains visibly unfinished authoring text in its
  Discussion & Conclusions section. The public HTML record already limits its
  result to what the artifact supports. Do not edit or replace the poster without
  an approved final artifact and explicit direction.

### 2026-27 work

- Add the 2026-27 year when participants and project directions are known.
- Decide what minimum current-project information can be published before final
  papers and posters exist.
- Keep the annual structure data-driven so the latest year changes without
  breaking the 2025-26 URLs.

### Student and project intake

- Consider a lab-membership/project-intake form for names, project titles,
  mentors, external institutions, research area, and publication permissions.
- Define which fields are internal working records and which may enter the
  public repository. The present repository contains public material only.
- Record external collaboration explicitly so the student-credit rule can be
  applied deliberately rather than reconstructed later.
- For student-suggested literature, begin with a restricted Google Form and a
  private response sheet. Publish only teacher-approved fields; do not expose
  submitter identity, raw responses, or an unmoderated feed on the public site.
- Automate an approved-only export only after the manual moderation fields and
  public/private boundary have been tested in normal class use.

### Peer TJ labs

- Q Lab is the only peer lab with a verified current standalone site.
- Obtain current URLs for Biotechnology and Life Sciences, Chemical Analysis and
  Nanochemistry, Computer Systems, Combined Engineering Research, Mobile and Web
  Application Development, Neuroscience, and Oceanography and Geophysical
  Systems.
- Until then, retain non-clickable cards and the current official TJHSST Senior
  Research Labs overview. Do not substitute the stale 2015-17 pages.

### Partners

- Decide whether the current text-mark treatment is sufficient or whether the
  page should use official organization logos.
- If logos are adopted, obtain approved official assets for NRL, Johns Hopkins
  APL, George Mason University, Georgetown University, and the Thomas Jefferson
  Partnership Fund; store them locally and record source/provenance.
- Clarify whether the page represents current relationships only or also
  historically important support.
- Audit future project records for qualifying external collaborations rather
  than inferring project-level relationships from the general Partners page.

### Astro at TJ family

- The Astro Team link points to its live Director site at
  <https://activities.tjhsst.edu/astroteam/>.
- The family strip links directly to the current AA:SS 2026-27 sister page and
  the lab-owned Astronomy Research 2026-27 page. A Classes landing page remains
  optional and is not required for these stable year-specific routes.
- Keep AA:SS content, CSS, and generated pages in their existing source and
  deployment repositories. The Astronomy Research class page uses this lab
  repository's data, generator, and shared theme.
- Revisit the Club and family links periodically so a functioning top-level
  connection does not become a stale directory.

## Design decisions still open

- Whether the compact tjSTAR countdown should also appear in the header of every
  primary page. It is currently prominent on Home and present on Research.
- Whether additional durable pages are useful, such as lab resources,
  facilities, expectations, or a project-submission guide. Add them only when
  there is real content and a clear recurring audience; do not create empty
  architecture.
- Whether older annual archives can be reconstructed from authoritative papers,
  posters, or tjSTAR records.

## External maintenance outside this repository

- The ORCID record's personal-website field has previously pointed to an obsolete
  TAMU URL; updating the ORCID profile is separate from this site.
- The 2026-27 Classes site migration and its Director/Git workflow are separate
  tasks.

## Working principle for the next task

Extend the site from evidence and actual recurring needs. Preserve the compact,
matter-of-fact tone: show what the lab is doing, make the useful paths obvious,
and invite contact without promotional language.
