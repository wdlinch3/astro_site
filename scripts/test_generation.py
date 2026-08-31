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
    assert "Explore 2026-27 projects" not in rendered["index.html"]
    assert "How the lab works" in rendered["index.html"]
    assert "1 project record" in rendered["index.html"]
    assert "1 project spanning exoplanets." in rendered["research/index.html"]
    assert "1 projects" not in rendered["research/index.html"]
    assert "2025-26" in rendered["research/index.html"]
    assert "2026-27" in rendered["research/index.html"]
    assert '<span class="site-name" aria-current="page">Astronomy &amp; Astrophysics Research</span>' in rendered["index.html"]
    assert '<a class="site-name" href="../index.html">Astronomy &amp; Astrophysics Research</a>' in rendered["about/index.html"]
    assert '<a class="site-mark-kicker" href="https://tjhsst.fcps.edu/">TJHSST</a>' in rendered["index.html"]
    assert '<a href="https://activities.tjhsst.edu/astroteam/">Astro Team</a>' in rendered["index.html"]
    assert "Astro at TJ" in rendered["index.html"]
    assert ">Elective Class</a>" in rendered["index.html"]
    assert ">Research Class</a>" in rendered["index.html"]
    class_path = "classes/astronomy-research/2026-2027/index.html"
    assert class_path in rendered
    assert "<h1>Astronomy Research</h1>" in rendered[class_path]
    assert "A gas-enshrouded and gas-reddened black hole at cosmic dawn" in rendered[class_path]
    assert "NASA ADS" in rendered[class_path]
    assert "arXiv astrophysics" in rendered[class_path]
    assert '<span class="family-current" aria-current="page">Research Class</span>' in rendered[class_path]
    assert '<span class="family-current" aria-current="page">Research Lab</span>' not in rendered[class_path]
    assert 'href="../../../index.html"' in rendered[class_path]
    assert "View the current AA:SS class" in rendered["about/index.html"]
    assert "partners/index.html" in rendered
    assert "labs/index.html" in rendered
    assert ">Partners</a>" in rendered["index.html"]
    assert ">TJ Labs</a>" in rendered["index.html"]
    assert "0000-0003-2631-4465" in rendered["contact/index.html"]
    assert "Research Practicum Program" in rendered["partners/index.html"]
    assert "Research Practicum Program" in rendered["labs/index.html"]
    assert "Project credits" not in rendered["2025-26/exomoon-wobble/index.html"]
    assert "Project credits" in rendered["2025-26/v-sparc/index.html"]
    assert 'href="Final_paper/exomoon.pdf">Paper</a>' in rendered["2025-26/index.html"]
    assert "Next tjSTAR" in rendered["index.html"]
    assert "A year built around evidence" not in rendered["index.html"]
    assert 'aria-current="page">Partners</a>' in rendered["partners/index.html"]
    assert 'aria-current="page">TJ Labs</a>' in rendered["labs/index.html"]
    assert "<h1>Research archive</h1>" in rendered["research/index.html"]
    assert "<h1>Senior research in Astro Lab</h1>" in rendered["about/index.html"]
    assert "<h1>Partners</h1>" in rendered["partners/index.html"]
    assert "<h1>Contact</h1>" in rendered["contact/index.html"]

    retired_copy = (
        "Browse the lab's work",
        "From learning astronomy to doing astronomy",
        "Partners and collaborators",
        "Connect with the lab",
        "Questions across the astronomical sciences",
        "Interested in collaborating?",
    )
    for page_html in rendered.values():
        assert not any(phrase in page_html for phrase in retired_copy)

    for project in data["projects"]:
        year_html = rendered[f"{project['year']}/index.html"]
        for artifact in project["artifacts"]:
            expected = build_site.href(f"{project['year']}/index.html", artifact["path"])
            assert f'href="{expected}">{artifact["label"]}</a>' in year_html
        assert f'href="{project["tjstar_url"].replace("&", "&amp;")}">tjSTAR record</a>' in year_html

    for page_html in rendered.values():
        assert "TJSTAR" not in page_html
        assert "TJStar" not in page_html

    print("Generation tests passed: 2025-26 URLs remain stable when 2026-27 is added.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
