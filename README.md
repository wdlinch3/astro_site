# TJHSST Astronomy & Astrophysics Research Lab

This repository is the public source for the static site served at
<https://activities.tjhsst.edu/astro/>.

## Site structure

- `AGENTS.md` records the project's durable design, content, audit, and release conventions.
- `PROJECT_HANDOFF.md` records current status, unresolved decisions, and next work.
- `data/site.json` is the authority for navigation, professional profiles, partners, TJ labs, annual project content, credits, and artifact links.
- `scripts/build_site.py` generates ordinary static HTML with no server-side dependencies.
- `assets/site.css` contains the shared visual system.
- `assets/countdown.js` progressively enhances the static tjSTAR date.
- `2025-26/Final_paper/` and `2025-26/Final_poster/` contain public research artifacts.

## Regenerate and check

Run from the repository root:

```sh
python3 scripts/build_site.py
python3 scripts/build_site.py --check
python3 scripts/check_site.py
python3 scripts/test_generation.py
node scripts/test_countdown.mjs
```

The check command regenerates every managed HTML page in memory and fails if a committed page is stale or missing.
The site check crawls local links case-sensitively, validates basic document structure, and confirms the public artifact manifest.

Project credits are public only when a project records `external_collaboration: true` and supplies a public `collaboration` description. The checker enforces both conditions. To remove all HTML credit disclosures, delete every `credits` array from `data/site.json`, set `show_project_credits` to `false`, regenerate, and run the checks. Papers and posters remain unredacted unless an administrative request also requires removing or replacing those artifacts.

## Publication workflow

1. Review the generated site locally, including the project summaries and links.
2. Merge an approved pull request into `main` on GitHub.
3. In the Director terminal, enter the public Git checkout and run `git pull --ff-only`.
4. Verify the TJ-hosted URL anonymously after the pull.

GitHub is the source repository. The TJHSST Director site is the public delivery path.

### Minicourses

The catalog is generated from `data/site.json`. All eight Read online and PDF
links use the school-hosted student editions at `astro2627.sites.tjhsst.edu`.
Their build and packet styling are managed by the `astro2627` deployment builder,
using the exact recorded personal-site source commit. The earlier local reader
experiment is retained outside this deployment in the survey record.

## Public mirror export

`scripts/export_public.py` prepares an independent public mirror from exact Git
revisions. It reads committed blobs, so dirty or stale working trees cannot
silently change the exported edition. It does not publish or alter either host.
Use a new or empty output directory; the command refuses to overwrite an
existing export.

```sh
python3 scripts/export_public.py \
  --ref <reviewed-lab-commit> \
  --school-source ../astro2627 \
  --school-ref <reviewed-school-deployment-commit> \
  --personal-course-base https://wdlinch3.github.io/aa/ \
  --output /tmp/lab_mirror/astro
python3 scripts/test_export_public.py
```

The result can be installed at `/astro/` in the personal Jekyll repository.
`--public-base` overrides its default canonical base,
`https://wdlinch3.github.io/astro/`. The lab's generated pages seed the export;
only their referenced, committed public assets and artifacts are included.
The optional school snapshot supplies its explicit minicourse file allowlist
and shared packet stylesheet. These files go under `school/` inside the
mirror. Reading/PDF/catalog links are rewritten together so the mirror does
not send minicourse readers back to a school-hosted catalog. Scientific text
and binary artifacts are preserved; only HTML URL attributes and CSS URL
references change.

`--personal-course-base` rewrites only the school AA homepage and
`ss/2026-2027/` navigation to the corresponding personal-site routes. These
are dependencies on the personal site's existing AA deployment, not files
included in this export. Verify both destination routes and their assignment
links in the personal site's Jekyll build before publication. Other school
URLs are deliberately retained and reported rather than guessed.

`MIRROR_MANIFEST.json` records exact source commits, original/exported file
hashes, course-link mappings, and remaining external links/runtime
requirements. Missing linked files, untracked files, symlinks, private-source
file types, and unresolved local HTML fragments stop the export before output
is written. An unrelated untracked archive cannot enter the mirror.

This is a public delivery copy, not a replacement for the local/GitHub source
repositories. External research references, Schoology/Google Docs links, and
CDN scripts remain external. JavaScript-created network requests are not
inferred, so the export is not an offline edition. A comparison with the live
school site is still needed to discover any Director-only changes; a Git
export cannot discover those. Preserve private instructor sources separately
in their existing private local/GitHub workflow.

For acceptance: run the full lab checks and exporter tests, build the personal
site with Jekyll, and preview through HTTP at `/astro/`. Confirm local research
artifacts, minicourse readings/PDFs, and personal AA/assignment routes work
without requests to school hosts for those materials. Review the manifest's
remaining external dependencies explicitly. Merge and Director deployment
remain separately authorized actions.
