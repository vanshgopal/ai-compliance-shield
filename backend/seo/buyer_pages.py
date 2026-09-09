"""Buyer-intent programmatic SEO pages.

These target purchase-intent queries ("checker", "tool", "software", "audit",
"checklist", "risk assessment") rather than industry queries. They live on the
``/eu-ai-act-compliance-*`` slug space alongside industry pages.
"""

import json
import html

from .pages import _shell, _faq_html, BASE_URL, RELATED_BLOGS, OTHER_PAGES

PAGES = {
    "checklist": {
        "name": "EU AI Act compliance checklist",
        "h1": "EU AI Act Compliance Checklist — 15 Requirements, Scanned Automatically",
        "intro": (
            "The EU AI Act asks for a lot of groundwork: risk-management systems, data "
            "governance, technical documentation, record-keeping, human oversight, accuracy "
            "and cybersecurity. Walking a team through all 15 requirement areas manually "
            "takes weeks. A scanner checks your actual code and configuration against them "
            "and tells you exactly which items pass and which are missing."
        ),
        "sections": [
            ("What is on the compliance checklist",
             "The high-risk package covers: a risk-management system (Article 9); data-governance "
             "controls for training, validation and test data (Article 10); technical documentation "
             "(Article 11); automatic log-recording (Article 12); transparency and instructions "
             "(Article 13); human oversight, including a human who can override the system "
             "(Article 14); and accuracy, robustness and cybersecurity (Article 15). Providers also "
             "owe a quality-management system, an EU declaration of conformity and CE marking "
             "before market placement."),
            ("How an automated checklist is different",
             "A manual spreadsheet becomes stale the moment your code changes. An automated scan "
             "re-runs the checklist against your codebase, config files and model definitions every "
             "time, so the evidence matches reality. The result is a scorecard per requirement — "
             "with the specific files and lines that satisfy each item, and the gaps that need work."),
            ("Getting from checklist to compliant",
             "The checklist is step one. Fix gaps in priority order (high-risk gaps first), "
             "document each requirement with evidence, and re-scan so the report shows a closed "
             "loop. Regulators and auditors increasingly accept machine-generated evidence trails "
             "over hand-written claims."),
        ],
        "faqs": [
            ("Is the checklist free?",
             "The first scan is free and takes about 2 minutes. Paid plans cover recurring scans, "
             "full dashboards and remediation planning."),
            ("Does it reflect the omnibus deferrals?",
             "Yes. The rules engine reflects the current timelines under Regulation (EU) "
             "2026/1744, including the December 2027 high-risk date."),
            ("What if we are not high-risk?",
             "The scan still surfaces transparency duties such as chatbot disclosure and deepfake "
             "labelling, so limited-risk teams can close those cheap wins too."),
        ],
    },
    "audit": {
        "name": "EU AI Act audit",
        "h1": "EU AI Act Audit — An Automated Technical Compliance Audit in Minutes",
        "intro": (
            "A real EU AI Act audit checks your system against the Act's technical requirements, "
            "not just your paperwork. Doing that manually means code reviews, documentation hunts "
            "and a consultant's invoice. An automated audit scans the same surface — code, "
            "configuration, dependencies, APIs — in minutes and produces an evidence-based report "
            "you can hand to an auditor."
        ),
        "sections": [
            ("What a technical audit actually checks",
             "A useful audit verifies: how the system manages risk and logs decisions, whether "
             "training data has governance and provenance, whether technical documentation exists "
             "for each model, whether outputs are traceable and auditable, whether a human can "
             "override the system, and whether accuracy, robustness and cybersecurity measures are "
             "present in the code. Each check should resolve to evidence, not opinions."),
            ("Manual vs automated audit",
             "Manual audits are thorough but slow, expensive and snapshot-based — they test one "
             "point in time. Automated audits are fast, repeatable and continuous, and can be "
             "re-run after every deploy. The best setup is an automated first pass that flags "
             "deviations, then a human auditor signs off on the evidence."),
            ("What the report should contain",
             "Your audit report should list each requirement, the evidence found (files, config, "
             "dependencies), the pass/fail verdict, and a prioritized remediation plan. That is "
             "exactly the format the scanner produces — a board-ready summary plus a deep "
             "technical annex."),
        ],
        "faqs": [
            ("Does this replace a human auditor?",
             "No. The scan does the technical evidence-gathering. A qualified professional signs "
             "off on legal conformity and, where needed, the formal conformity assessment."),
            ("How long does an audit take?",
             "The automated scan runs in about 2 minutes. Recurring plans keep the evidence "
             "current automatically."),
            ("What is the cost?",
             "A free scan gives you a first-pass audit report. Paid plans add full dashboards, "
             "remediation planning and recurring audits."),
        ],
    },
    "software": {
        "name": "EU AI Act compliance software",
        "h1": "EU AI Act Compliance Software — Features, Pricing & Comparison (2026)",
        "intro": (
            "Choosing EU AI Act compliance software means choosing between document-heavy tools, "
            "consulting retainer wheels, and automated code scanners. This page explains what "
            "compliance software should actually do, what it should cost, and how AI Compliance "
            "Shield compares."
        ),
        "sections": [
            ("The four jobs compliance software must do",
             "Good AI Act software: (1) classifies your systems into risk tiers, (2) checks your "
             "actual code and configuration against the requirements, (3) produces an evidence-"
             "based report and remediation plan, and (4) keeps that evidence current as your code "
             "changes. Anything less is a checkbox tool, not a compliance system."),
            ("Where the industry overcharges",
             "Most AI compliance products are policy templates or consulting slidedecks. They "
             "charge five figures for PDFs that cannot see your code. An automated scanner checks "
             "the deployable reality — which is what regulators actually inspect — at a fraction "
             "of the cost."),
            ("What AI Compliance Shield offers",
             "Free first scan, 57+ industry-specific compliance guides, automated requirement "
             "matching against your codebase, a 0-100 compliance score, prioritized remediation, "
             "team dashboards, and plans from EUR 299/month without a multi-year contract."),
        ],
        "faqs": [
            ("Is it really a code scanner?",
             "Yes. Point it at your repo and it checks code, configuration and model definitions "
             "against the EU AI Act requirement engine."),
            ("Is my code safe?",
             "Scanning runs against your files; your source only leaves your machine if you "
             "explicitly upload it, and it is never stored or shared."),
            ("Can we try before paying?",
             "Yes — the first scan is free, no signup required."),
        ],
    },
    "tool": {
        "name": "EU AI Act compliance tool",
        "h1": "Free EU AI Act Compliance Tool — Check Your AI in 2 Minutes",
        "intro": (
            "A compliance tool should give you an answer quickly. The EU AI Act obligations are "
            "complex, but finding out where you stand does not have to be. This free tool scans "
            "your AI codebase and returns an EU AI Act compliance score in about two minutes — "
            "no signup, no code stored."
        ),
        "sections": [
            ("What the tool checks",
             "It matches your code, configuration and dependencies against the Act's requirement "
             "areas: risk management, data governance, technical documentation, record-keeping, "
             "transparency, human oversight, and accuracy, robustness and cybersecurity. The "
             "output is a coverage score per requirement."),
            ("How to use it",
             "Upload your project or point the scanner at a local path. The scan runs, the report "
             "renders, and you get a prioritized list of gaps to fix. Teams that sell into the EU "
             "from anywhere can use it — the Act applies to non-EU providers too."),
            ("What the score means",
             "The 0-100 score measures how much of the requirement engine your system already "
             "satisfies. It is not legal advice and does not replace a formal conformity "
             "assessment — it is the fastest evidence-based starting point available."),
        ],
        "faqs": [
            ("Is the tool really free?",
             "The first scan is free and unlimited in scope. Recurring scans and dashboards are "
             "part of paid plans."),
            ("Does it need EU access?",
             "No. Use it from anywhere; the tool checks against EU rules regardless of your "
             "location."),
            ("How accurate is the score?",
             "It reflects technical code patterns against the requirement list. Use it to find "
             "and fix gaps, then have a professional confirm legal conformity."),
        ],
    },
    "risk-assessment": {
        "name": "EU AI Act risk assessment",
        "h1": "EU AI Act Risk Assessment — Is Your AI System High-Risk?",
        "intro": (
            "Everything in the EU AI Act flows from one question: which risk tier is your AI "
            "system in? Prohibited, high-risk, limited-risk, or minimal-risk. Getting the "
            "classification wrong — especially under-calling high-risk — is the most expensive "
            "mistake you can make. Here is how to assess your tier, and how to verify it with "
            "a scan."
        ),
        "sections": [
            ("The four tiers at a glance",
             "Prohibited: practices banned outright — social scoring, manipulative deception, "
             "real-time public biometric identification, and the 2026 additions for non-consensual "
             "intimate imagery and CSAM. High-risk: AI in critical infrastructure, education, "
             "employment, essential services, law enforcement, migration and other Annex III "
             "areas, or AI that is a safety component of regulated products. Limited-risk: "
             "transparency duties only, e.g. chatbots and deepfakes. Minimal-risk: the rest — "
             "no mandatory obligations."),
            ("How to tell if you are high-risk",
             "Ask two questions. First: does your system fall under Annex I (a safety component "
             "of, or itself, a regulated product)? Second: does it fall under Annex III (a listed "
             "sensitive use, e.g. credit scoring, CV screening, biometric identification, "
             "education scoring)? If either is yes, you are high-risk unless an exception applies "
             "— and the burden of proving an exception sits with you."),
            ("Verify your tier with evidence",
             "A spreadsheet guess is not evidence. Scan the codebase so the classification is "
             "backed by the actual system: what risk-management hooks exist, what data feeds the "
             "model, what automated decisions it makes, and how outputs are logged and overridden."),
        ],
        "faqs": [
            ("Can a tool classify my tier?",
             "A scanner gives you an evidence-backed initial classification based on your code, "
             "config and use-case patterns. Final classification for regulated products still "
             "needs professional sign-off."),
            ("Is limited-risk really safe?",
             "Limited-risk means transparency duties — and chatbot disclosure and deepfake "
             "labelling are enforceable now, so 'not high-risk' is not 'no obligations'."),
            ("When do high-risk rules apply?",
             "Under the 2026 omnibus, Annex III high-risk systems face obligations from December "
             "2027 (Annex I products from August 2028). That gap is your runway to comply."),
        ],
    },
    "technical-documentation": {
        "name": "EU AI Act technical documentation",
        "h1": "EU AI Act Technical Documentation — Generate Your Dossier Automatically",
        "intro": (
            "Article 11 requires a technical documentation file for high-risk systems before "
            "market placement. It must cover the system's intended purpose, architecture, data, "
            "risk-management measures and verification results. Writing it by hand is slow; "
            "generating it from your actual codebase is fast and far harder to challenge."
        ),
        "sections": [
            ("What must be in your technical file",
             "The dossier includes: a general description (intended purpose, input/output, "
             "deployers), a detailed architecture and development process description, training/"
             "validation/test data descriptions and governance, monitoring and logging design, "
             "accuracy and robustness evidence, risk-management measures, and instructions for "
             "use. Providers must keep it up to date and available to authorities."),
            ("Why the documentation must match the code",
             "Auditors cross-check the dossier against the shipped system. A documentation file "
             "that describes features your code does not implement is worse than no file at all — "
             "it looks like an attempt to mislead. Evidence generated from the actual codebase "
             "survives that check."),
            ("Automating the generation",
             "An automated pipeline reads the repo and drafts each dossier section directly from "
             "code, config and metadata: architecture from the module graph, model definitions "
             "from config, data handling from the data layer, and logging from the observability "
             "hooks. You review and sign, instead of writing from scratch."),
        ],
        "faqs": [
            ("Do we still need a lawyer?",
             "Yes — for the legal conformity assessment and declaration of conformity. The "
             "generator handles the technical evidence layer."),
            ("Is the dossier graded?",
             "The scan scores each required documentation element so you know which sections are "
             "missing before an inspector does."),
            ("Can it stay current?",
             "Recurring plans regenerate the dossier on every scan, so the file matches the "
             "latest deployed code."),
        ],
    },
}


def buyer_slugs() -> list:
    return sorted(PAGES.keys())


def build_page(key: str):
    import html as _h
    data = PAGES[key]
    slug = f"eu-ai-act-compliance-{key}"
    url = f"{BASE_URL}/{slug}"
    meta_title = f"{data['h1']} | AI Compliance Shield"
    description = data["intro"][:150].replace("\n", " ").strip() + " Free scan, no signup."

    jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": data["h1"],
        "description": description,
        "datePublished": "2026-09-08",
        "dateModified": "2026-09-08",
        "publisher": {"@type": "Organization", "name": "AI Compliance Shield"},
        "mainEntityOfPage": url,
    }, ensure_ascii=False, indent=2)

    intro_html = f"<p><strong>{_h.escape(data['intro'])}</strong></p>"
    sections_html = "".join(
        f"<h2>{_h.escape(head)}</h2><p>{_h.escape(body)}</p>" for head, body in data["sections"]
    )

    related_links = "\n".join(
        f'<p class="art-link"><a href="{u}">{label}</a></p>' for label, u in RELATED_BLOGS
    )
    related_links += "\n" + "\n".join(
        f'<p class="art-link"><a href="{url}">{label}</a></p>'
        for label, url in OTHER_PAGES
    )

    return _shell(
        meta_title=meta_title,
        description=description,
        keywords=f"EU AI Act {data['name']}, {data['name']} free, AI Act compliance scanner",
        canonical_url=url,
        jsonld=jsonld,
        tag_line="EU AI Act · Compliance tooling",
        h1=data["h1"],
        intro_html=intro_html,
        sections_html=sections_html,
        faq_html=_faq_html(data.get("faqs", [])),
        related_html=related_links,
    )