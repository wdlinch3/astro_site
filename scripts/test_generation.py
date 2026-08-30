#!/usr/bin/env python3
"""Regression test for coexisting annual research archives."""

from __future__ import annotations

import copy

import build_site


def main() -> int:
    data = copy.deepcopy(build_site.load_data())
    future_year = {"slug": "2026-27", "label": "2026-27"}
    future_project = copy.deepcopy(data["projects"][0])
    future_project.update(
        {
            "year": future_year["slug"],
            "slug": "future-fixture",
            "title": "Future Archive Fixture",
            "credits": [],
        }
    )
    data["years"].append(future_year)
    data["projects"].append(future_project)
    data["site"]["latest_year"] = future_year["slug"]

    rendered = build_site.render_all(data)
    assert "2025-26/exomoon-wobble/index.html" in rendered
    assert "2025-26/index.html" in rendered
    assert "2026-27/future-fixture/index.html" in rendered
    assert "2026-27/index.html" in rendered
    assert "Explore 2026-27 projects" in rendered["index.html"]
    assert "1 project record" in rendered["index.html"]
    assert "1 project spanning exoplanets." in rendered["research/index.html"]
    assert "1 projects" not in rendered["research/index.html"]
    assert "2025-26" in rendered["research/index.html"]
    assert "2026-27" in rendered["research/index.html"]
    assert '<span class="site-name" aria-current="page">Astronomy &amp; Astrophysics Research</span>' in rendered["index.html"]
    assert '<a class="site-name" href="../index.html">Astronomy &amp; Astrophysics Research</a>' in rendered["about/index.html"]
    assert '<a class="site-mark-kicker" href="https://tjhsst.fcps.edu/">TJHSST</a>' in rendered["index.html"]
    assert '<span class="family-placeholder">Astro Team</span>' in rendered["index.html"]
    assert "Astro at TJ" in rendered["index.html"]
    assert ">Classes</a>" in rendered["index.html"]

    print("Generation tests passed: 2025-26 URLs remain stable when 2026-27 is added.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
