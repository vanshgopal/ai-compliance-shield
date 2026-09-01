# seotool — Organic SEO Automation

Automates the **legitimate inputs** that help a website rank in organic (unpaid)
Google search results. Runs on the **Python standard library only** (no pip
installs needed).

> ## ⚠️ Honest expectation setting — read this first
> **No tool can guarantee page-1 ranking.** Google ranks pages on years of
> accumulated authority: indexation history, backlinks, domain age. Your site
> (`vgsr.pythonanywhere.com`) is currently **not indexed by Google at all**.
> Every competitor on page 1 (aiactstack.com, complipilot.dev, aiactgap.com,
> the official EU checker, etc.) is there because it's **indexed** and has
> **backlinks**.
>
> This tool automates the work that *builds toward* page 1:
> keyword content, internal links, sitemaps, backlink outreach files, and a
> position tracker. It will not instantly leapfrog established domains. Anyone
> who promises guaranteed page 1 is selling something false.

---

## What it actually automate

| Command | What it does | Files it writes |
|---------|--------------|-----------------|
| `python seotool.py keyword-list` | Shows the target keyword DB + CSV | `data/keywords.csv` |
| `python seotool.py articles` | Generates a keyword-optimized blog post per keyword, with internal links | `frontend/templates/blog/*.html` |
| `python seotool.py sitemap` | Generates `sitemap.xml` + `robots.txt` covering every page | `frontend/static/sitemap.xml`, `robots.txt` |
| `python seotool.py links` | Emits backlink/directory submission files (copy-paste ready) | `output/directories.md`, `output/reddit-draft.md` |
| `python seotool.py track` | Position tracker (CSV you fill in, or wire a search API) | `data/rankings.csv` |
| `python seotool.py all` | Runs everything above | — |

Run any single command, e.g.:

```bash
cd C:\Users\pc\Desktop\ai-compliance-shield\seotool
python seotool.py articles
python seotool.py sitemap
python seotool.py all
```

---

## The order that matters (do these BEFORE the tool can help you rank)

1. **Get indexed (required, currently missing).**
   - Add your site to Google Search Console, verify it, submit `sitemap.xml`,
     then request indexing. Without this, Google doesn't crawl you at all.
   - Add GA4 so you can see traffic.
2. **Deploy the generated content.**
   - The tool writes files locally. They must be uploaded to PythonAnywhere +
     the web app reloaded before they're live. (The site is currently missing
     even the already-built `/resources` page — deploy that block too.)
3. **Backlinks (drives authority).**
   - Use `output/directories.md` to submit to free directories (Product Hunt,
     SaaSHub, AlternativeTo, G2, Futurepedia). Each is a real external link.
4. **Monitor with `track`.**
   - Record each keyword's position over weeks. Movement is the signal that
     the work is compounding.

---

## The `track` command — honest notes

`track` builds a rankings CSV. Filling the `position` column automatically
requires a **search API** (SerpApi etc.), which is a paid service after free
credits. The stub `_lookup_serp()` shows where to wire it. Until then, check
each keyword in Google yourself and type the position into
`data/rankings.csv` — that's free and accurate.

---

## The real checklist (the boring part that actually works)

- [ ] Google Search Console: verify + submit sitemap + request indexing
- [ ] GA4 installed
- [ ] Deploy `/resources`, blog pages, updated sitemap
- [ ] Submit to 5+ free directories (`output/directories.md`)
- [ ] Post the community draft (`output/reddit-draft.md`) where rules allow
- [ ] Run `articles` monthly to add fresh keyword content
- [ ] Track positions weekly in `data/rankings.csv`

No shortcut replaces the indexed + backlinks foundation. This tool makes doing
that work fast and repeatable — it doesn't fake it.
