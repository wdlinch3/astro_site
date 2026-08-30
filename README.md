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
