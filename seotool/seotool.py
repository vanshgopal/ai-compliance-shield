"""
AI Compliance Shield — Organic SEO Automation Tool
--------------------------------------------------
Automates the legitimate INPUTS that help a site rank in organic (unpaid)
search results. It does NOT and CANNOT guarantee page 1 — no tool can.
Google ranks pages on years of authority + backlinks + indexation that no
script can fabricate overnight.

What the tool DOES automate:
  1. keyword   - loads/manages the target keyword list
  2. articles  - generates keyword-optimized blog posts with an internal
                 link network between pages
  3. sitemap   - generates sitemap.xml + robots.txt from the page inventory
  4. links     - emits backlink/directory submission files (copy-paste ready)
  5. track     - checks which position each keyword ranks at (needs a search API key)

Runs on the Python STANDARD LIBRARY only (no pip installs needed).

Usage:
    python seotool.py keyword-list
    python seotool.py articles
    python seotool.py sitemap
    python seotool.py links
    python seotool.py track --api YOUR_KEY
    python seotool.py all
"""

import argparse
import json
import os
import re
import sys
import urllib.parse
from collections import OrderedDict

# --------------------------------------------------------------------------- #
#  Config
# --------------------------------------------------------------------------- #
TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(TOOL_DIR, ".."))
TEMPLATES_DIR = os.path.join(PROJECT_ROOT, "frontend", "templates")
BLOG_DIR = os.path.join(TEMPLATES_DIR, "blog")
STATIC_DIR = os.path.join(PROJECT_ROOT, "frontend", "static")
OUTPUT_DIR = os.path.join(TOOL_DIR, "output")
DATA_DIR = os.path.join(TOOL_DIR, "data")

BASE_URL = "https://vgsr.pythonanywhere.com"
SITE_NAME = "AI Compliance Shield"

# --------------------------------------------------------------------------- #
#  Keyword database
# --------------------------------------------------------------------------- #
# keyword      -> (approx monthly searches, difficulty, intent)
KEYWORDS = OrderedDict([
    ("eu ai act compliance",       (2400, "Medium", "transactional/info")),
    ("eu ai act checklist",        (1800, "Medium", "information")),
    ("ai compliance tool",         (1200, "Low",    "commercial")),
    ("ai compliance check",        (600,  "Low",    "commercial")),
    ("eu ai act scanner",          (800,  "Low",    "commercial")),
    ("ai audit tool",              (1000, "Low",    "commercial")),
    ("eu ai act compliance for startups", (900, "Low", "information")),
    ("eu ai act requirements",     (1300, "Medium", "information")),
    ("article 50 eu ai act",       (500,  "Low",    "information")),
    ("eu ai act fines",            (1100, "Low",    "information")),
    ("eu ai act deadlines 2026",   (700,  "Low",    "information")),
    ("eu ai act transparency",     (600,  "Low",    "information")),
    ("ai act for small business",  (500,  "Low",    "information")),
    ("how to comply with eu ai act", (800, "Medium", "information")),
    ("eu ai act generative ai",    (500,  "Low",    "information")),
])


def keyword_list():
    """Pretty-print the keyword database as a table + CSV."""
    rows = [("keyword", "monthly_searches", "difficulty", "intent", "slug")]
    for kw, (searches, diff, intent) in KEYWORDS.items():
        rows.append((kw, str(searches), diff, intent, slugify(kw)))
    print_table(rows)
    return iterative_make_dirs(DATA_DIR) and write_csv(
        os.path.join(DATA_DIR, "keywords.csv"),
        [",".join(r) for r in rows])


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text.strip("-")


# --------------------------------------------------------------------------- #
#  Utils
# --------------------------------------------------------------------------- #
def iterative_make_dirs(path):
    os.makedirs(path, exist_ok=True)
    return True


def write_text(path, content):
    iterative_make_dirs(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def write_csv(path, lines):
    iterative_make_dirs(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return path


def print_table(rows):
    if not rows:
        return
    widths = [max(len(str(r[i])) for r in rows) for i in range(len(rows[0]))]
    sep = "  ".join("-" * w for w in widths)
    print(sep)
    for r in rows:
        print("  ".join(str(c).ljust(w) for c, w in zip(r, widths)))
    print(sep)


def slug(value):
    return slugify(value)


# --------------------------------------------------------------------------- #
#  Page inventory (used by sitemap + internal linking)
# --------------------------------------------------------------------------- #
def page_inventory(generated_articles):
    """Return a list of (path, lastmod, changefreq, priority, title)."""
    pages = [
        ("/",                             "2026-08-31", "weekly",  "1.0", "Home"),
        ("/pricing",                      "2026-08-31", "monthly", "0.9", "Pricing"),
        ("/features",                     "2026-08-31", "monthly", "0.8", "Features"),
        ("/how-it-works",                 "2026-08-31", "monthly", "0.8", "How It Works"),
        ("/get-started",                  "2026-08-31", "weekly",  "0.8", "Get Started"),
        ("/resources",                    "2026-08-31", "weekly",  "0.8", "Free Resources"),
        ("/privacy-policy",               "2026-08-31", "yearly",  "0.3", "Privacy Policy"),
        ("/terms",                        "2026-08-31", "yearly",  "0.3", "Terms"),
        ("/refund-policy",                "2026-08-31", "yearly",  "0.3", "Refund Policy"),
        ("/contact",                      "2026-08-31", "yearly",  "0.3", "Contact"),
        ("/about",                        "2026-08-31", "yearly",  "0.3", "About"),
    ]
    # static/manual blogs
    manual_blogs = [
        ("/blog/eu-ai-act-requirements-checklist-2026", "EU AI Act Requirements Checklist (2026)"),
        ("/blog/eu-ai-act-fines-2026",                  "EU AI Act Fines in 2026"),
        ("/blog/eu-ai-act-compliance-indian-saas-2026", "EU AI Act for Indian SaaS"),
        ("/blog/eu-ai-act-compliance-for-startups-2026","EU AI Act Compliance for Startups 2026"),
    ]
    for path, title in manual_blogs:
        pages.append((path, "2026-08-31", "monthly", "0.7", title))
    for a in generated_articles:
        pages.append((a["path"], "2026-08-31", "monthly", "0.7", a["title"]))
    return pages


# --------------------------------------------------------------------------- #
#  1. Article generator
# --------------------------------------------------------------------------- #
ARTICLE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | AI Compliance Shield</title>
  <meta name="description" content="{meta_desc}">
  <meta name="keywords" content="{keywords}">
  <link rel="canonical" href="{BASE}/blog/{slug}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{meta_desc}">
  <style>
    body {{ font-family: -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
           line-height: 1.7; color: #111; max-width: 800px; margin: 0 auto;
           padding: 24px; }}
    h1,h2,h3 {{ line-height: 1.3; }}
    a {{ color: #2563EB; }}
    nav, footer {{ border-top: 1px solid #eee; margin-top: 28px; padding-top: 14px;
                   font-size: 14px; }}
    nav a, footer a {{ margin-right: 14px; }}
    .cta {{ background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px;
           padding: 16px; margin: 24px 0; }}
  </style>
</head>
<body>
  <nav>
    <a href="/">AI Compliance Shield</a>
    <a href="/features">Features</a>
    <a href="/how-it-works">How It Works</a>
    <a href="/pricing">Pricing</a>
    <a href="/resources">Free Guides</a>
  </nav>

  <h1>{h1}</h1>
  <p><em>Updated for 2026 • {BASE}/blog/{slug}</em></p>

  <p>{intro}</p>

  <div class="cta">
    <strong>Scan your code now — it's free.</strong> Get your EU AI Act compliance
    score in about 5 minutes. <a href="/">Run the free scanner →</a>
  </div>

  <h2>{section1_h}</h2>
  <p>{section1_p1}</p>
  <p>{section1_p2}</p>

  <h2>{section2_h}</h2>
  <p>{section2_p1}</p>
  <p>{section2_p2}</p>

  <h2>Frequently asked questions</h2>
  <p><strong>Q: {faq_q1}</strong></p>
  <p>A: {faq_a1}</p>
  <p><strong>Q: {faq_q2}</strong></p>
  <p>A: {faq_a2}</p>

  <div class="cta">
    <strong>Don't guess — check.</strong> Run our free EU AI Act compliance scan
    and get a 0–100%% score plus a prioritized fix list. <a href="/">Start now →</a>
  </div>

  <h3>Related EU AI Act guides</h3>
  <p>{related_links}</p>

  <footer>
    <a href="/">Home</a>
    <a href="/pricing">Pricing</a>
    <a href="/features">Features</a>
    <a href="/how-it-works">How It Works</a>
    <a href="/resources">Free Guides</a>
    <a href="/privacy-policy">Privacy</a>
    <a href="/terms">Terms</a>
    <a href="/contact">Contact</a>
    <p>Disclaimer: AI Compliance Shield provides an automated technical check. It is
       not legal advice and does not guarantee EU AI Act compliance.</p>
  </footer>
</body>
</html>
"""


def _related_links(chain):
    """Build internal link block from other pages (the internal-link network)."""
    links = []
    slugs = [slugify(kw) for kw in ["eu ai act compliance", "eu ai act checklist",
                                    "eu ai act fines", "eu ai act requirements",
                                    "eu ai act deadlines 2026"]]
    for s in slugs:
        word = s.replace("-", " ")
        links.append('<a href="/blog/%s">%s</a>' % (s, word.title()))
    for other in chain:
        links.append('<a href="/blog/%s">%s</a>' % (other["slug"], other["title"]))
    # de-dup preserving order
    seen, out = set(), []
    for l in links:
        if l not in seen:
            seen.add(l)
            out.append(l)
    return " • ".join(out[:7])


def generate_articles():
    """Generate a keyword-optimized blog post for each target keyword."""
    iterative_make_dirs(BLOG_DIR)
    generated = []
    # manual slugs we already have (avoid clobbering)
    existing = {"eu-ai-act-requirements-checklist-2026",
                "eu-ai-act-fines-2026",
                "eu-ai-act-compliance-indian-saas-2026",
                "eu-ai-act-compliance-for-startups-2026"}
    for kw, (searches, diff, intent) in KEYWORDS.items():
        slug = slugify(kw)
        if slug in existing:
            continue
        title = kw.title()
        h1 = "%s — a practical 2026 guide" % kw.title()
        meta_desc = ("Learn about %s for the EU AI Act. Run our free scanner to get "
                     "your compliance score and a prioritized fix list in minutes." % kw)
        content = ARTICLE_TEMPLATE.format(
            BASE=BASE_URL,
            title=title,
            slug=slug,
            meta_desc=meta_desc,
            keywords=", ".join(list(KEYWORDS.keys())[:8]),
            h1=h1,
            intro=("The EU AI Act's main obligations are in force as of August 2, 2026. "
                   "Small teams often assume it only applies to big tech. This guide covers "
                   "%s and how to check where you stand." % kw),
            section1_h="Why %s matters now" % kw,
            section1_p1=("Under the EU AI Act, roughly %s monthly searches come from "
                         "people exactly like you — founders and engineers trying to "
                         "figure out their obligations. The good news is the first step "
                         "is free and takes minutes." % ("{:,}".format(searches))),
            section1_p2=("The main transparency obligations (Article 50) are already "
                         "enforceable. A quick code scan tells you whether you're "
                         "producing detectable AI output, handling data governance, "
                         "and keeping the audit trail regulators expect."),
            section2_h="How to check %s for your project" % kw,
            section2_p1=("Upload your code or point the scanner at your repo. In about "
                         "five minutes you get a 0–100%% compliance score, the specific "
                         "rules you're missing, and a prioritized remediation plan."),
            section2_p2=("Repeat the scan as you make changes to track your progress. "
                         "Compliance is a process, not a one-time checkbox."),
            faq_q1=("Does %s apply to my small company?" % kw),
            faq_a1="If you build, deploy, or use AI systems whose output reaches EU users, the Act's transparency and (where relevant) high-risk duties can apply regardless of company size.",
            faq_q2="Do I need to hire a consultant?",
            faq_a2="Start with a free automated scan to see your gaps. Many teams fix basic transparency issues themselves and only escalate genuinely high-risk use cases to a qualified EU AI Act lawyer.",
            related_links=_related_links([]),
        )
        path = os.path.join(BLOG_DIR, slug + ".html")
        write_text(path, content)
        generated.append({"slug": slug, "title": title,
                          "path": "/blog/" + slug, "file": path})
        print("  wrote %s" % path)
    print("Generated %d new keyword articles." % len(generated))
    return generated


# --------------------------------------------------------------------------- #
#  2. Sitemap + robots generator
# --------------------------------------------------------------------------- #
def generate_sitemap(generated_articles=None):
    generated_articles = generated_articles or []
    pages = page_inventory(generated_articles)
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, lastmod, freq, prio, _title in pages:
        lines.append("  <url>")
        lines.append("    <loc>%s%s</loc>" % (BASE_URL, path))
        lines.append("    <lastmod>%s</lastmod>" % lastmod)
        lines.append("    <changefreq>%s</changefreq>" % freq)
        lines.append("    <priority>%s</priority>" % prio)
        lines.append("  </url>")
    lines.append("</urlset>")
    sitemap = "\n".join(lines)
    robots = ("User-agent: *\n"
              "Allow: /\n"
              "Sitemap: %s/sitemap.xml\n" % BASE_URL)
    s1 = write_text(os.path.join(STATIC_DIR, "sitemap.xml"), sitemap)
    s2 = write_text(os.path.join(PROJECT_ROOT, "robots.txt"), robots)
    print("  wrote %s" % s1)
    print("  wrote %s (project root — deploy to site root)" % s2)
    return sitemap


# --------------------------------------------------------------------------- #
#  3. Backlink / directory submission files
# --------------------------------------------------------------------------- #
DIRECTORIES = [
    ("Product Hunt",        "https://www.producthunt.com/posts/new", "Launch page"),
    ("SaaSHub",             "https://www.saashub.com/submit",        "Free listing"),
    ("AlternativeTo",       "https://alternativeto.net/submit-a-tool/", "Free listing"),
    ("G2",                  "https://www.g2.com/products/new",       "Free listing"),
    ("Futurepedia",         "https://www.futurepedia.io/submit-a-tool", "AI tools galore"),
    ("There's An AI For That", "https://theresanaiforthat.com/submit-tool/", "AI tools galore"),
    ("AI Tool Hunt",        "https://www.ai-toolhunt.com/submit",    "Free listing"),
]


def generate_links_files():
    iterative_make_dirs(OUTPUT_DIR)
    # directory list
    dl = ["# Directory & community submission targets (organic backlinks)", ""]
    for name, url, note in DIRECTORIES:
        dl.append("- [%s](%s) — %s" % (name, url, note))
    dl.append("")
    dl.append("## Universal listing boilerplate")
    dl.append("")
    dl.append("- **Name:** " + SITE_NAME)
    dl.append("- **Tagline:** Automated EU AI Act compliance scanner for SMEs & SaaS")
    dl.append("- **One-liner:** Scan your code against the EU AI Act in ~5 minutes, get a 0-100% compliance score, the specific violations, and a prioritized remediation plan.")
    dl.append("- **Website:** " + BASE_URL)
    dl.append("- **Pricing:** Free scan; paid plans from Rs 24,999/month")
    dl.append("- **Contact:** (use your monitoring inbox)")
    p1 = write_text(os.path.join(OUTPUT_DIR, "directories.md"), "\n".join(dl))
    print("  wrote %s" % p1)

    # reddit post draft
    rd = [
        "# Reddit / community draft (adapt to each subreddit's rules)",
        "",
        "**Title:** I built a free EU AI Act compliance scanner for small SaaS teams",
        "",
        "**Body:**",
        "The EU AI Act's main transparency obligations went live Aug 2, 2026, and small "
        "companies are exposed to fines up to EUR 35M/7% of global revenue. Most teams "
        "aren't sure which rules apply to them.",
        "",
        "I built a free tool that scans a codebase in ~5 minutes and returns a 0-100% "
        "compliance score, the specific obligations you're missing, and what to fix. "
        "No signup needed for a scan.",
        "",
        "Would love feedback from anyone shipping AI or ML features: " + BASE_URL,
    ]
    p2 = write_text(os.path.join(OUTPUT_DIR, "reddit-draft.md"), "\n".join(rd))
    print("  wrote %s" % p2)
    print("  Directory kit: %s" % p1)
    print("  Community draft: %s" % p2)


# --------------------------------------------------------------------------- #
#  4. Ranking position tracker
# --------------------------------------------------------------------------- #
def track_rankings(api_key=None, num_results=20):
    """
    Reports which position each keyword ranks at.

    NOTE: This requires a keyword-ranking search API. With a standard-lib-only
    CSV dump of your last known positions, it reads/updates a local CSV so you
    can track movement over time. Live SERP scraping needs an API key (e.g.
    SerpApi, which is paid once you exceed free credits).

    Without an API key, this prints instructions and a starter CSV you can fill in
    after checking Google yourself (or after connecting a SerpApi account).
    """
    iterative_make_dirs(DATA_DIR)
    csv_path = os.path.join(DATA_DIR, "rankings.csv")
    header = "keyword,position,url,checked_at"
    lines = [header]
    if os.path.exists(csv_path):
        with open(csv_path, encoding="utf-8") as f:
            lines = [ln.rstrip("\n") for ln in f if ln.strip()]
    seen = {ln.split(",")[0] for ln in lines[1:]}
    for kw in KEYWORDS:
        if kw not in seen:
            lines.append("%s,,," % kw)
    write_csv(csv_path, lines)
    print("Rankings CSV ready: %s" % csv_path)
    print("")
    if api_key:
        print("[track] Live SERP lookups need a search API. Wire your provider's "
              "endpoint here. Until then, fill the `position` column after "
              "checking Google, or connect a SerpApi key to automate it.")
        print("        (KEY PROVIDED but refactor `_lookup_serp` in this file to call your provider.)")
    else:
        print("[track] No --api provided.")
        print("        Options:")
        print("          1) Check each keyword on Google, paste the position into %s" % csv_path)
        print("          2) Connect a search API (e.g. SerpApi) and edit `_lookup_serp()` "
              "to fill positions automatically.")
    return csv_path


def _lookup_serp(keyword, api_key, num_results):
    """Stub: replace with your search API call to automate live position checks."""
    raise NotImplementedError(
        "\nTrack live requires a search API. Implement `_lookup_serp()` with your "
        "provider (e.g. SerpApi). Example payload:\n"
        "  GET https://serpapi.com/search.json?engine=google&q=%(kw)s&num=%(n)s"
        % {"kw": urllib.parse.quote(keyword), "n": num_results}
    )


# --------------------------------------------------------------------------- #
#  CLI
# --------------------------------------------------------------------------- #
def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Organic SEO automation for AI Compliance Shield (stdlib-only).")
    parser.add_argument("command", nargs="?", default="all",
                        choices=["all", "keyword-list", "articles", "sitemap",
                                 "links", "track"],
                        help="What to run. Default: all")
    parser.add_argument("--api", dest="api_key", default=None,
                        help="Search API key for live ranking lookup (optional).")
    args = parser.parse_args(argv)
    iterative_make_dirs(DATA_DIR)
    iterative_make_dirs(OUTPUT_DIR)

    if args.command in ("all", "keyword-list"):
        print("== Keywords ==")
        keyword_list()
    if args.command in ("all", "articles"):
        print("\n== Generating keyword articles ==")
        generated = generate_articles()
    else:
        generated = []
    if args.command in ("all", "sitemap"):
        print("\n== Generating sitemap + robots ==")
        generate_sitemap(generated)
    if args.command in ("all", "links"):
        print("\n== Generating backlink/directory kit ==")
        generate_links_files()
    if args.command in ("all", "track"):
        print("\n== Ranking position tracker ==")
        track_rankings(args.api_key)

    print("\nDone. Outputs written under seotool/output and seotool/data, plus")
    print("frontend/static/sitemap.xml and blog/ pages (ready to deploy).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
