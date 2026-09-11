#!/usr/bin/env python3
"""Detect, cluster, and prioritize issues in Screaming Frog crawl exports."""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

SEVERITY_WEIGHT = {"critical": 100, "high": 40, "medium": 12, "low": 3}
TITLE_MAX_CHARS = 60
TITLE_MIN_CHARS = 30
TITLE_MAX_PX = 600
META_MAX_CHARS = 155
META_MIN_CHARS = 70
META_MAX_PX = 985
H1_MAX_CHARS = 70
THIN_WORDS = 200
DEEP_DEPTH = 4
SLOW_SECONDS = 1.0
LONG_URL_CHARS = 115
HIGH_INLINKS_NOINDEX = 20
MONEY_TOKENS = (
    "service",
    "services",
    "product",
    "products",
    "location",
    "locations",
    "contact",
    "pricing",
    "quote",
    "estimate",
    "shop",
    "collection",
)

COLUMN_ALIASES = {
    "address": ["address", "url", "uri"],
    "content_type": ["content type"],
    "status_code": ["status code"],
    "status": ["status"],
    "indexability": ["indexability"],
    "indexability_status": ["indexability status"],
    "title": ["title 1", "title"],
    "title_length": ["title 1 length", "title length"],
    "title_px": ["title 1 pixel width", "title pixel width"],
    "meta": ["meta description 1", "meta description"],
    "meta_length": ["meta description 1 length", "meta description length"],
    "meta_px": ["meta description 1 pixel width", "meta description pixel width"],
    "h1": ["h1-1", "h1 1", "h1"],
    "h1_length": ["h1-1 length", "h1 1 length", "h1 length"],
    "h1_2": ["h1-2", "h1 2"],
    "canonical": ["canonical link element 1", "canonical link element", "canonical 1"],
    "word_count": ["word count"],
    "inlinks": ["unique inlinks", "inlinks"],
    "crawl_depth": ["crawl depth"],
    "response_time": ["response time"],
    "redirect_url": ["redirect url", "redirect uri"],
    "meta_robots": ["meta robots 1", "meta robots"],
    "alt_text": ["alt text", "alt"],
    "loop": ["loop"],
    "hops": ["number of hops", "hops", "redirects"],
    "from_url": ["from", "source"],
    "to_url": ["to", "destination", "destination url"],
}


@dataclass
class Finding:
    issue_id: str
    title: str
    severity: str
    url: str
    detail: str
    inlinks: int
    indexable: bool
    status: int
    template: str
    directory: str
    page_type: str


@dataclass
class Cluster:
    issue_id: str
    title: str
    severity: str
    template: str
    path_templates: list[str]
    count: int
    indexable_count: int
    total_inlinks: int
    score: float
    examples: list[dict[str, Any]] = field(default_factory=list)
    sample_details: list[str] = field(default_factory=list)


def norm_header(value: str) -> str:
    value = value.replace("\ufeff", "").strip().lower()
    value = value.replace("–", "-").replace("—", "-")
    value = re.sub(r"[_\s]+", " ", value)
    return value


def map_columns(headers: list[str]) -> dict[str, str]:
    lookup = {norm_header(h): h for h in headers}
    mapped: dict[str, str] = {}
    for key, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            if alias in lookup:
                mapped[key] = lookup[alias]
                break
    return mapped


def to_int(value: Any, default: int = 0) -> int:
    if value is None:
        return default
    text = str(value).strip()
    if text == "":
        return default
    try:
        return int(float(text))
    except ValueError:
        return default


def to_float(value: Any, default: float = 0.0) -> float:
    if value is None:
        return default
    text = str(value).strip().replace("s", "")
    if text == "":
        return default
    try:
        return float(text)
    except ValueError:
        return default


def is_blank(value: Any) -> bool:
    return value is None or str(value).strip() == ""


def is_html(content_type: str) -> bool:
    if not content_type:
        return True
    return "html" in content_type.lower()


def is_indexable(value: str) -> bool:
    return value.strip().lower() == "indexable"


def is_homepage(url: str) -> bool:
    path = urlparse(url).path or "/"
    return path in {"/", "/index", "/index.html", "/index.php", "/home"}


def first_directory(url: str) -> str:
    parts = [p for p in urlparse(url).path.split("/") if p]
    if not parts:
        return "/"
    return f"/{parts[0]}/"


def page_type(url: str) -> str:
    if is_homepage(url):
        return "homepage"
    path = urlparse(url).path.lower()
    for token in MONEY_TOKENS:
        if re.search(rf"[/-]{token}s?([/-]|$)", path):
            return "money"
    if "/blog/" in path or "/news/" in path or "/article" in path:
        return "blog"
    if "search" in path or urlparse(url).query:
        return "utility"
    return "other"


def templatize(url: str) -> str:
    parsed = urlparse(url)
    parts: list[str] = []
    for part in parsed.path.split("/"):
        if part == "":
            continue
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", part):
            parts.append("{date}")
        elif re.fullmatch(r"\d{4}", part):
            parts.append("{year}")
        elif re.fullmatch(r"\d+", part):
            parts.append("{id}")
        elif re.fullmatch(r"[0-9a-f]{8}-[0-9a-f-]{27,}", part, re.I):
            parts.append("{id}")
        elif re.fullmatch(r"[0-9a-f]{32,}", part, re.I):
            parts.append("{id}")
        else:
            parts.append(part)
    path = "/" + "/".join(parts)
    if parsed.path.endswith("/") and path != "/":
        path += "/"
    if parsed.query:
        keys = []
        for chunk in parsed.query.split("&"):
            if not chunk:
                continue
            keys.append(chunk.split("=", 1)[0])
        if keys:
            path += "?{" + ",".join(sorted(set(keys))) + "}"
    return path or "/"


def money_boost(template: str, types: list[str]) -> float:
    if "homepage" in types or template in {"/", "/index", "/index.html"}:
        return 2.5
    lowered = template.lower()
    if any(token in lowered for token in MONEY_TOKENS) or "money" in types:
        return 1.5
    return 1.0


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    for encoding in ("utf-8-sig", "utf-8", "cp1252"):
        try:
            with path.open(newline="", encoding=encoding) as handle:
                sample = handle.read(4096)
                handle.seek(0)
                header = sample.splitlines()[0] if sample else ""
                # Screaming Frog is comma-separated. Sniffer will misread
                # "text/html; charset=utf-8" as a semicolon delimiter.
                if "\t" in header and "," not in header:
                    dialect = csv.excel_tab
                else:
                    dialect = csv.excel
                reader = csv.DictReader(handle, dialect=dialect)
                rows = [{k: (v or "") for k, v in row.items() if k is not None} for row in reader]
                return reader.fieldnames or [], rows
        except UnicodeDecodeError:
            continue
    raise RuntimeError(f"Could not decode {path}")


def collect_files(inputs: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw in inputs:
        path = Path(raw).expanduser()
        if path.is_dir():
            files.extend(sorted(path.glob("*.csv")))
        elif path.is_file():
            files.append(path)
        else:
            raise FileNotFoundError(raw)
    if not files:
        raise FileNotFoundError("No CSV files found")
    return files


def classify_export(headers: list[str], mapped: dict[str, str]) -> str:
    names = {norm_header(h) for h in headers}
    if "alt text" in names or mapped.get("alt_text"):
        return "images"
    if mapped.get("loop") or "number of hops" in names:
        return "redirect_chains"
    if mapped.get("from_url") and mapped.get("to_url"):
        return "inlinks"
    if mapped.get("address") and mapped.get("status_code"):
        return "internal"
    return "unknown"


def row_value(row: dict[str, str], mapped: dict[str, str], key: str) -> str:
    header = mapped.get(key)
    if not header:
        return ""
    return (row.get(header) or "").strip()


def analyze_internal(rows: list[dict[str, str]], mapped: dict[str, str]) -> list[Finding]:
    findings: list[Finding] = []
    html_rows = []
    for row in rows:
        url = row_value(row, mapped, "address")
        if not url:
            continue
        content_type = row_value(row, mapped, "content_type")
        if not is_html(content_type):
            continue
        html_rows.append(row)

    title_groups: dict[str, list[str]] = defaultdict(list)
    meta_groups: dict[str, list[str]] = defaultdict(list)
    h1_groups: dict[str, list[str]] = defaultdict(list)
    parsed_rows: list[dict[str, Any]] = []

    https_html = 0
    http_html = 0

    for row in html_rows:
        url = row_value(row, mapped, "address")
        status = to_int(row_value(row, mapped, "status_code"))
        indexable = is_indexable(row_value(row, mapped, "indexability"))
        title = row_value(row, mapped, "title")
        meta = row_value(row, mapped, "meta")
        h1 = row_value(row, mapped, "h1")
        inlinks = to_int(row_value(row, mapped, "inlinks"))
        item = {
            "url": url,
            "status": status,
            "indexable": indexable,
            "indexability_status": row_value(row, mapped, "indexability_status"),
            "title": title,
            "title_length": to_int(row_value(row, mapped, "title_length"), default=-1),
            "title_px": to_int(row_value(row, mapped, "title_px"), default=-1),
            "meta": meta,
            "meta_length": to_int(row_value(row, mapped, "meta_length"), default=-1),
            "meta_px": to_int(row_value(row, mapped, "meta_px"), default=-1),
            "h1": h1,
            "h1_length": to_int(row_value(row, mapped, "h1_length"), default=-1),
            "h1_2": row_value(row, mapped, "h1_2"),
            "canonical": row_value(row, mapped, "canonical"),
            "word_count": to_int(row_value(row, mapped, "word_count"), default=-1),
            "inlinks": inlinks,
            "crawl_depth": to_int(row_value(row, mapped, "crawl_depth"), default=-1),
            "response_time": to_float(row_value(row, mapped, "response_time")),
            "redirect_url": row_value(row, mapped, "redirect_url"),
            "meta_robots": row_value(row, mapped, "meta_robots").lower(),
            "template": templatize(url),
            "page_type": page_type(url),
        }
        if item["title_length"] < 0:
            item["title_length"] = len(title)
        if item["meta_length"] < 0:
            item["meta_length"] = len(meta)
        if item["h1_length"] < 0:
            item["h1_length"] = len(h1)
        parsed_rows.append(item)
        if url.lower().startswith("https://"):
            https_html += 1
        elif url.lower().startswith("http://"):
            http_html += 1
        if status == 200 and indexable:
            if title:
                title_groups[title].append(url)
            if meta:
                meta_groups[meta].append(url)
            if h1:
                h1_groups[h1].append(url)

    duplicate_titles = {k for k, urls in title_groups.items() if len(set(urls)) > 1}
    duplicate_meta = {k for k, urls in meta_groups.items() if len(set(urls)) > 1}
    duplicate_h1 = {k for k, urls in h1_groups.items() if len(set(urls)) > 1}
    site_is_https = https_html >= http_html and https_html > 0

    def add(issue_id: str, title: str, severity: str, item: dict[str, Any], detail: str) -> None:
        findings.append(
            Finding(
                issue_id=issue_id,
                title=title,
                severity=severity,
                url=item["url"],
                detail=detail,
                inlinks=item["inlinks"],
                indexable=item["indexable"],
                status=item["status"],
                template=item["template"],
                directory=first_directory(item["url"]),
                page_type=item["page_type"],
            )
        )

    for item in parsed_rows:
        url = item["url"]
        status = item["status"]
        if 500 <= status <= 599:
            add("server_error", "Server error (5xx)", "critical", item, f"Status {status}")
        elif 400 <= status <= 499:
            add("client_error", "Client error (4xx)", "high", item, f"Status {status}, {item['inlinks']} unique inlinks")
        if is_homepage(url) and not item["indexable"] and status == 200:
            add(
                "homepage_non_indexable",
                "Homepage is non-indexable",
                "critical",
                item,
                item["indexability_status"] or "Non-Indexable",
            )

        unintended = (
            not item["indexable"]
            and status == 200
            and (
                item["page_type"] in {"homepage", "money"}
                or item["inlinks"] >= HIGH_INLINKS_NOINDEX
            )
        )
        if unintended and not is_homepage(url):
            add(
                "unintended_noindex",
                "Likely unintended non-indexable page",
                "high",
                item,
                item["indexability_status"] or item["meta_robots"] or "Non-Indexable",
            )

        if site_is_https and url.lower().startswith("http://"):
            add("http_urls", "HTTP URL on an HTTPS site", "high", item, "Internal page still on http://")

        if status != 200 or not item["indexable"]:
            continue

        if is_blank(item["title"]):
            add("missing_title", "Missing title", "high", item, "Empty Title 1")
        else:
            if item["title"] in duplicate_titles:
                add(
                    "duplicate_title",
                    "Duplicate title",
                    "high",
                    item,
                    f'"{item["title"]}" used on {len(title_groups[item["title"]])} URLs',
                )
            if item["title_length"] > TITLE_MAX_CHARS or item["title_px"] > TITLE_MAX_PX:
                add(
                    "title_too_long",
                    "Title too long",
                    "low",
                    item,
                    f"{item['title_length']} chars, {item['title_px']} px" if item["title_px"] > 0 else f"{item['title_length']} chars",
                )
            if 0 < item["title_length"] < TITLE_MIN_CHARS:
                add("title_too_short", "Title too short", "low", item, f"{item['title_length']} chars")
            if item["title"] and item["h1"] and item["title"] == item["h1"]:
                add("title_same_as_h1", "Title same as H1", "low", item, item["title"])

        if is_blank(item["meta"]):
            add("missing_meta_description", "Missing meta description", "medium", item, "Empty Meta Description 1")
        else:
            if item["meta"] in duplicate_meta:
                add(
                    "duplicate_meta_description",
                    "Duplicate meta description",
                    "medium",
                    item,
                    f"Same description on {len(meta_groups[item['meta']])} URLs",
                )
            if item["meta_length"] > META_MAX_CHARS or item["meta_px"] > META_MAX_PX:
                add(
                    "meta_too_long",
                    "Meta description too long",
                    "low",
                    item,
                    f"{item['meta_length']} chars",
                )
            if 0 < item["meta_length"] < META_MIN_CHARS:
                add("meta_too_short", "Meta description too short", "low", item, f"{item['meta_length']} chars")

        if is_blank(item["h1"]):
            add("missing_h1", "Missing H1", "medium", item, "Empty H1-1")
        else:
            if item["h1"] in duplicate_h1:
                add(
                    "duplicate_h1",
                    "Duplicate H1",
                    "medium",
                    item,
                    f'"{item["h1"]}" used on {len(h1_groups[item["h1"]])} URLs',
                )
            if item["h1_length"] > H1_MAX_CHARS:
                add("h1_too_long", "H1 too long", "low", item, f"{item['h1_length']} chars")
        if not is_blank(item["h1_2"]):
            add("multiple_h1", "Multiple H1s", "medium", item, f'H1-2: "{item["h1_2"]}"')

        if item["word_count"] >= 0 and item["word_count"] < THIN_WORDS and item["page_type"] != "utility":
            add("thin_content", "Thin content", "medium", item, f"{item['word_count']} words")
        if item["inlinks"] == 0 and mapped.get("inlinks") and item["page_type"] != "utility":
            add("orphan_page", "Orphan page (0 unique inlinks)", "medium", item, "No unique inlinks in crawl")
        if item["crawl_depth"] > DEEP_DEPTH and item["inlinks"] < 5:
            add("deep_page", "Deep in site architecture", "low", item, f"Depth {item['crawl_depth']}")
        if item["response_time"] > SLOW_SECONDS:
            add("slow_response", "Slow response time", "low", item, f"{item['response_time']:.2f}s")
        path = urlparse(url).path
        if len(url) > LONG_URL_CHARS:
            add("long_url", "Long URL", "low", item, f"{len(url)} chars")
        if "_" in path:
            add("underscore_url", "Underscore in URL", "low", item, path)
        if re.search(r"[A-Z]", path):
            add("uppercase_url", "Uppercase characters in URL", "low", item, path)
        if urlparse(url).query:
            add("parameter_url_indexable", "Indexable parameterized URL", "low", item, urlparse(url).query)

    return findings


def analyze_images(rows: list[dict[str, str]], mapped: dict[str, str]) -> list[Finding]:
    findings: list[Finding] = []
    for row in rows:
        url = row_value(row, mapped, "address")
        if not url:
            continue
        alt = row_value(row, mapped, "alt_text")
        if is_blank(alt):
            item_url = url
            findings.append(
                Finding(
                    issue_id="missing_image_alt",
                    title="Missing image alt text",
                    severity="medium",
                    url=item_url,
                    detail="Empty alt text",
                    inlinks=0,
                    indexable=True,
                    status=200,
                    template=templatize(item_url),
                    directory=first_directory(item_url),
                    page_type="asset",
                )
            )
    return findings


def analyze_redirect_chains(rows: list[dict[str, str]], mapped: dict[str, str]) -> list[Finding]:
    findings: list[Finding] = []
    for row in rows:
        url = row_value(row, mapped, "address") or row_value(row, mapped, "from_url")
        if not url:
            continue
        hops = to_int(row_value(row, mapped, "hops"), default=1)
        loop = row_value(row, mapped, "loop").lower() in {"true", "yes", "1"}
        template = templatize(url)
        if loop:
            findings.append(
                Finding(
                    issue_id="redirect_loop",
                    title="Redirect loop",
                    severity="critical",
                    url=url,
                    detail="Loop=True in redirect chain export",
                    inlinks=0,
                    indexable=False,
                    status=0,
                    template=template,
                    directory=first_directory(url),
                    page_type=page_type(url),
                )
            )
        elif hops >= 3:
            findings.append(
                Finding(
                    issue_id="redirect_chain",
                    title="Redirect chain (3+ hops)",
                    severity="high",
                    url=url,
                    detail=f"{hops} hops",
                    inlinks=0,
                    indexable=False,
                    status=0,
                    template=template,
                    directory=first_directory(url),
                    page_type=page_type(url),
                )
            )
    return findings


def cluster_findings(findings: list[Finding], max_examples: int) -> list[Cluster]:
    buckets: dict[tuple[str, str], list[Finding]] = defaultdict(list)
    for finding in findings:
        buckets[(finding.issue_id, finding.directory)].append(finding)

    clusters: list[Cluster] = []
    for (issue_id, directory), items in buckets.items():
        first = items[0]
        count = len(items)
        indexable_count = sum(1 for item in items if item.indexable)
        total_inlinks = sum(item.inlinks for item in items)
        volume = min(count, 100) + 10 * math.log10(count + 1)
        inlink_boost = 1 + min(total_inlinks, 500) / 50
        indexable_boost = 1 + (indexable_count / count if count else 0)
        boost = money_boost(directory, [item.page_type for item in items])
        score = SEVERITY_WEIGHT[first.severity] * volume * inlink_boost * indexable_boost * boost
        examples = []
        for item in sorted(items, key=lambda f: (-f.inlinks, f.url))[:max_examples]:
            examples.append({"url": item.url, "inlinks": item.inlinks, "detail": item.detail})
        path_templates = sorted({item.template for item in items})
        clusters.append(
            Cluster(
                issue_id=issue_id,
                title=first.title,
                severity=first.severity,
                template=directory,
                path_templates=path_templates[:8],
                count=count,
                indexable_count=indexable_count,
                total_inlinks=total_inlinks,
                score=round(score, 1),
                examples=examples,
                sample_details=list(dict.fromkeys(item.detail for item in items))[:5],
            )
        )
    clusters.sort(key=lambda c: (-c.score, c.severity, -c.count))
    return clusters


def crawl_stats(internal_rows: list[dict[str, str]], mapped: dict[str, str]) -> dict[str, Any]:
    html = []
    for row in internal_rows:
        if is_html(row_value(row, mapped, "content_type")) and row_value(row, mapped, "address"):
            html.append(row)
    indexable_200 = 0
    status_counts: dict[str, int] = defaultdict(int)
    for row in html:
        status = to_int(row_value(row, mapped, "status_code"))
        bucket = f"{status // 100}xx" if status else "unknown"
        status_counts[bucket] += 1
        if status == 200 and is_indexable(row_value(row, mapped, "indexability")):
            indexable_200 += 1
    return {
        "html_urls": len(html),
        "indexable_200": indexable_200,
        "status_families": dict(status_counts),
    }


def roadmap(clusters: list[Cluster]) -> dict[str, list[str]]:
    now: list[str] = []
    sprint: list[str] = []
    backlog: list[str] = []
    for cluster in clusters:
        label = f"{cluster.title} on `{cluster.template}` ({cluster.count})"
        if cluster.severity == "critical" or (cluster.severity == "high" and cluster.score >= 200):
            now.append(label)
        elif cluster.severity in {"high", "medium"}:
            sprint.append(label)
        else:
            backlog.append(label)
    return {"do_now": now[:12], "this_sprint": sprint[:15], "backlog": backlog[:15]}


def render_markdown(
    files: list[str],
    export_types: dict[str, str],
    stats: dict[str, Any],
    clusters: list[Cluster],
    gaps: list[str],
) -> str:
    lines = ["# Screaming Frog crawl analysis", ""]
    lines.append("## Executive summary")
    critical = sum(c.count for c in clusters if c.severity == "critical")
    high = sum(c.count for c in clusters if c.severity == "high")
    medium = sum(c.count for c in clusters if c.severity == "medium")
    low = sum(c.count for c in clusters if c.severity == "low")
    lines.append(
        f"- **{len(clusters)} issue clusters** across {stats.get('html_urls', 0)} HTML URLs "
        f"({stats.get('indexable_200', 0)} indexable 200s)."
    )
    lines.append(f"- Findings by severity: Critical {critical}, High {high}, Medium {medium}, Low {low}.")
    if clusters:
        top = clusters[0]
        lines.append(
            f"- Highest-leverage cluster: **{top.title}** on `{top.template}` "
            f"({top.count} URLs, score {top.score})."
        )
    lines.append("")
    lines.append("## Crawl snapshot")
    lines.append("")
    lines.append("| Export | Type |")
    lines.append("| --- | --- |")
    for name, kind in export_types.items():
        lines.append(f"| `{name}` | {kind} |")
    lines.append("")
    families = stats.get("status_families", {})
    if families:
        lines.append("Status families: " + ", ".join(f"{k}={v}" for k, v in sorted(families.items())))
        lines.append("")
    plan = roadmap(clusters)
    lines.append("## Fix roadmap")
    lines.append("")
    for heading, key in (("Do now", "do_now"), ("This sprint", "this_sprint"), ("Backlog", "backlog")):
        lines.append(f"### {heading}")
        items = plan[key]
        if not items:
            lines.append("- None")
        else:
            for item in items:
                lines.append(f"- {item}")
        lines.append("")
    lines.append("## Prioritized clusters")
    lines.append("")
    lines.append("| Rank | Score | Severity | Issue | Template | URLs | Indexable | Inlinks |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for index, cluster in enumerate(clusters, start=1):
        lines.append(
            f"| {index} | {cluster.score} | {cluster.severity} | {cluster.title} | `{cluster.template}` | "
            f"{cluster.count} | {cluster.indexable_count} | {cluster.total_inlinks} |"
        )
    lines.append("")
    lines.append("## Cluster details")
    lines.append("")
    for index, cluster in enumerate(clusters, start=1):
        lines.append(f"### {index}. {cluster.title} — `{cluster.template}`")
        lines.append("")
        lines.append(
            f"{cluster.severity.title()} · {cluster.count} URLs · "
            f"{cluster.indexable_count} indexable · {cluster.total_inlinks} unique inlinks · score {cluster.score}"
        )
        if cluster.sample_details:
            lines.append("")
            lines.append("Notes: " + "; ".join(cluster.sample_details))
        if cluster.path_templates:
            lines.append("")
            lines.append("Path patterns: " + ", ".join(f"`{item}`" for item in cluster.path_templates))
        lines.append("")
        lines.append("| URL | Inlinks | Detail |")
        lines.append("| --- | --- | --- |")
        for example in cluster.examples:
            detail = example["detail"].replace("|", "/")
            lines.append(f"| {example['url']} | {example['inlinks']} | {detail} |")
        lines.append("")
    if gaps:
        lines.append("## Data gaps")
        lines.append("")
        for gap in gaps:
            lines.append(f"- {gap}")
        lines.append("")
    lines.append("## Files analyzed")
    lines.append("")
    for name in files:
        lines.append(f"- `{name}`")
    lines.append("")
    return "\n".join(lines)


def infer_gaps(export_types: set[str]) -> list[str]:
    gaps = []
    if "redirect_chains" not in export_types:
        gaps.append("No redirect-chain export: hop counts and loops were not fully checked.")
    if "inlinks" not in export_types:
        gaps.append("No All Inlinks export: broken-link sources were not listed.")
    if "images" not in export_types:
        gaps.append("No Images export: missing alt text was not checked.")
    return gaps


def analyze_paths(paths: list[Path], max_examples: int) -> dict[str, Any]:
    findings: list[Finding] = []
    export_types: dict[str, str] = {}
    stats: dict[str, Any] = {"html_urls": 0, "indexable_200": 0, "status_families": {}}
    for path in paths:
        headers, rows = read_csv(path)
        mapped = map_columns(headers)
        kind = classify_export(headers, mapped)
        export_types[path.name] = kind
        if kind == "internal":
            findings.extend(analyze_internal(rows, mapped))
            stats = crawl_stats(rows, mapped)
        elif kind == "images":
            findings.extend(analyze_images(rows, mapped))
        elif kind == "redirect_chains":
            findings.extend(analyze_redirect_chains(rows, mapped))
        elif kind == "inlinks":
            export_types[path.name] = "inlinks (context only)"
        else:
            export_types[path.name] = f"unrecognized ({', '.join(headers[:6])})"
    clusters = cluster_findings(findings, max_examples=max_examples)
    payload = {
        "files": [str(path) for path in paths],
        "export_types": export_types,
        "stats": stats,
        "gaps": infer_gaps(set(export_types.values())),
        "finding_count": len(findings),
        "clusters": [asdict(cluster) for cluster in clusters],
        "roadmap": roadmap(clusters),
    }
    payload["markdown"] = render_markdown(
        payload["files"],
        export_types,
        stats,
        clusters,
        payload["gaps"],
    )
    return payload


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze Screaming Frog CSV exports and prioritize clustered SEO fixes."
    )
    parser.add_argument("inputs", nargs="+", help="CSV files or a directory of CSVs")
    parser.add_argument("--json", action="store_true", help="Write machine-readable JSON instead of Markdown")
    parser.add_argument("--out", help="Write the report to this file as well as stdout")
    parser.add_argument("--max-examples", type=int, default=8, help="Example URLs per cluster")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    paths = collect_files(args.inputs)
    payload = analyze_paths(paths, max_examples=args.max_examples)
    output = json.dumps(payload, indent=2) if args.json else payload["markdown"]
    sys.stdout.write(output)
    if not output.endswith("\n"):
        sys.stdout.write("\n")
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover - CLI surface
        sys.stderr.write(f"error: {exc}\n")
        raise SystemExit(1)
