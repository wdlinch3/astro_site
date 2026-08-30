# Astro Lab site handoff

Last updated: 2026-08-30

## Current state

The first substantial implementation is on branch
`codex/build-project-archive` in open PR #2:

<https://github.com/wdlinch3/astro_site/pull/2>

At commit `1c160a5`, the branch contains:

- the landing page, Research, About, Partners, TJ Labs, and Contact;
- a 2025-26 archive with eight concise project records;
- retained paper, poster, and filtered tjSTAR links;
- the Astro at TJ family strip;
- a May 19, 2027 tjSTAR countdown;
- professional profile links for William D. Linch III;
- responsive layouts audited at 1280, 768, 390, and 320 px;
- the privacy rule that exposes HTML student credits only for explicitly marked
  external collaborations.

The branch is pushed but unmerged. Nothing from PR #2 has been pulled to
Director or anonymously verified on the live TJHSST site.

## Before the first deployment

1. Author-review the eight public scientific summaries and the V-SPARC credit
   disclosure.
2. Confirm with Tiger that Director's `public` directory should remain a Git
   checkout and that direct server-side edits are outside the normal workflow.
3. Review PR #2, merge only after approval, then use `git pull --ff-only` in the
   Director checkout.
4. Verify the live site anonymously, including the homepage, all primary pages,
   all eight project records, papers/posters, family links, and mobile behavior.

## Content and links still needed

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

- Replace the Astro Team placeholder when its officer supplies the current URL.
- The Classes link currently points to the 2026-27 sister site. Keep the class
  migration and any AA@TJ redesign in their own repository/workflow; do not mix
  their CSS or generated pages into this lab repository.
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

