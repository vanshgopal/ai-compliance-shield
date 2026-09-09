"""Programmatic SEO page generator for AI Compliance Shield.

Generates long-tail keyword pages targeting low-competition searches.
Each page describes the EU AI Act rules for a specific industry or use case
and links back to the compliance scanner.
"""

import html
import json
from datetime import datetime

BASE_URL = "https://aicomplianceshield.site"

INDUSTRIES = {
    "healthcare": {
        "title": "Healthcare",
        "risk": "high-risk",
        "rules": "Clinical decision-support systems that help diagnose or treat patients are treated as high-risk under the EU AI Act. Companies must keep technical documentation, ensure human oversight, and log every assisted decision. Even wellness chatbots that only give general health tips usually stay outside the high-risk rules.",
    },
    "fintech": {
        "title": "FinTech & Banking",
        "risk": "high-risk",
        "rules": "AI that scores credit, prices insurance, or detects fraud is treated as high-risk. Providers need risk-management systems, data-governance controls, and audit logs. If an AI system decides who gets a loan, a human must be able to review and override the decision.",
    },
    "hr-recruiting": {
        "title": "HR & Recruiting",
        "risk": "high-risk",
        "rules": "AI used to screen CVs, rank candidates, or recommend hiring decisions is high-risk. Resume-screening tools must be tested for bias, documented, and give human reviewers the final call. Chatbots that answer candidate questions generally stay lower-risk.",
    },
    "ecommerce": {
        "title": "E-Commerce",
        "risk": "limited-risk",
        "rules": "Recommendation engines and dynamic-pricing AI are limited-risk. They mostly need transparency — telling users when they are interacting with AI and how their data shapes results. They do not need the heavy documentation that high-risk systems do.",
    },
    "education": {
        "title": "Education",
        "risk": "high-risk",
        "rules": "AI that scores exams, admits students, or evaluates learning outcomes is high-risk. AI-based proctoring that monitors test-takers is also tightly restricted because it can use biometric data. Developers need bias testing, documentation, and human oversight.",
    },
    "edtech-tutoring": {
        "title": "EdTech & Tutoring",
        "risk": "limited-risk",
        "rules": "Intelligent tutoring systems that adapt lessons to students are usually limited-risk. They carry transparency duties but mostly avoid the heaviest obligations. The picture changes the moment the AI makes an official assessment or decides a grade.",
    },
    "legaltech": {
        "title": "LegalTech",
        "risk": "limited-risk",
        "rules": "AI that drafts contracts or summarises case law is limited-risk today, but it must be transparent and accurate. Systems that rank legal outcomes or make case-priority decisions risk being classified as high-risk and need far more documentation.",
    },
    "insurtech": {
        "title": "InsurTech",
        "risk": "high-risk",
        "rules": "AI used to price premiums, assess risk, or process claims can be high-risk, especially when it affects access to insurance. Providers must document the model, audit for discrimination, and leave a human in the loop for significant decisions.",
    },
    "real-estate": {
        "title": "Real Estate & Proptech",
        "risk": "limited-risk",
        "rules": "AI that values properties or matches buyers to homes is limited-risk if it only recommends. It becomes high-risk if it decides who can access essential housing services. Transparency about how AI shapes recommendations is the first obligation.",
    },
    "marketing": {
        "title": "Marketing & AdTech",
        "risk": "limited-risk",
        "rules": "Ad-targeting and content-personalisation AI are limited-risk. The main duties are transparency and honest labelling, especially for AI-generated content. Deepfakes and social-scoring systems are banned outright, so adtech must stay well clear of those.",
    },
    "customer-support": {
        "title": "Customer Support Chatbots",
        "risk": "limited-risk",
        "rules": "Chatbots that answer customer questions must clearly disclose they are AI. Article 50 transparency is already live. If a chatbot makes decisions that significantly affect a person — like refunds or account bans — the risk tier climbs.",
    },
    "manufacturing": {
        "title": "Manufacturing & IIoT",
        "risk": "limited-risk",
        "rules": "Predictive-maintenance and quality-control AI are usually limited or minimal risk. Safety-related components that protect workers can become high-risk. Documentation and incident reporting requirements have been rolling in since 2025.",
    },
    "recruitment-agencies": {
        "title": "Recruitment Agencies",
        "risk": "high-risk",
        "rules": "Recruitment platforms that screen, rank, or filter talent are high-risk under Annex III. They need bias audits, technical documentation, and human oversight. The August 2, 2026 deadline put most of these obligations into force.",
    },
    "prototyping": {
        "title": "Prototyping & MVP",
        "risk": "minimal-risk",
        "rules": "Testing and prototyping AI is the moment to build compliance in cheaply. Features you ship to EU users trigger obligations, while internal prototypes — especially pre-market — carry lighter rules. Starting documentation early saves months later.",
    },
    "freelance-development": {
        "title": "Freelance & Development Agencies",
        "risk": "limited-risk",
        "rules": "Agencies that ship AI features for clients inherit parts of the provider obligations. Even if you build the model for a customer, you carry duties like technical documentation and transparency. Your deliverables should include compliance artefacts.",
    },
    "sme-saas": {
        "title": "SME SaaS",
        "risk": "limited-risk",
        "rules": "Most SME SaaS products that add AI features start in the limited-risk tier. The cheapest win is Article 50 transparency — disclose that users interact with AI. Review your risk tier before the heavier 2027 deadlines arrive.",
    },
    "startups": {
        "title": "Startups",
        "risk": "limited-risk",
        "rules": "Startups shipping AI to EU markets should map their risk tier immediately. The EU AI Act gives SMEs lower compliance fees and sandbox access, but only if you know which obligations apply. A free scan of your codebase is the fastest starting point.",
    },
    "nlp": {
        "title": "NLP & Text AI",
        "risk": "limited-risk",
        "rules": "Text-generation and summarisation AI carry transparency duties and, for large models, GPAI obligations. If your NLP tool generates deepfake-style synthetic content, disclosure rules tighten. Keep an audit trail of model versions and prompts.",
    },
    "computer-vision": {
        "title": "Computer Vision",
        "risk": "high-risk",
        "rules": "Real-time biometric identification in public spaces is banned except for narrow law-enforcement cases. Emotion-recognition in workplaces and schools is banned. Other computer-vision uses are fine but can be high-risk, so document early.",
    },
    "generative-ai": {
        "title": "Generative AI",
        "risk": "limited-risk",
        "rules": "Generative models fall under GPAI transparency rules and must label AI-generated content. Training-data summaries are required for large models. If you build or fine-tune foundation models, register your system in the EU database.",
    },
    "voice-assistants": {
        "title": "Voice Assistants",
        "risk": "limited-risk",
        "rules": "Voice assistants must disclose they are AI and can be used as generative models. Voice-cloning and synthetic-voice tools face deepfake disclosure rules. Sensitive biometric authentication raises the risk tier considerably.",
    },
    "automotive": {
        "title": "Automotive",
        "risk": "high-risk",
        "rules": "Autonomous-driving and driver-monitoring AI hits the highest-risk tier because it touches safety. Expect substantial technical documentation and conformity assessments. Suppliers and integrators share obligations across the supply chain.",
    },
    "supply-chain": {
        "title": "Supply Chain",
        "risk": "limited-risk",
        "rules": "Demand forecasting and logistics optimisation AI are limited-risk. They mostly need transparency and good data governance. The tier rises only when AI makes decisions that significantly affect people, like shutting off essential services.",
    },
    "cybersecurity": {
        "title": "Cybersecurity",
        "risk": "limited-risk",
        "rules": "Threat-detection and anomaly-detection AI are limited-risk and typically exempt from the heaviest rules. Providers still must be transparent and document model behaviour. Incident reporting is the key operational obligation.",
    },
    "enterprise-b2b": {
        "title": "Enterprise B2B",
        "risk": "limited-risk",
        "rules": "B2B AI tools start limited-risk but EU enterprise buyers already ask for AI Act documentation in procurement. Being able to show a compliance report is becoming a deal-breaker. Demand for vendor AI-compliance evidence is growing fast.",
    },
    "property-management": {
        "title": "Property Management",
        "risk": "limited-risk",
        "rules": "AI that screens tenants or sets rental terms edges toward high-risk if it controls access to housing. Landlords and proptech firms must document bias checks and keep humans in the loop on lease decisions.",
    },
    "dating-apps": {
        "title": "Dating & Social Apps",
        "risk": "limited-risk",
        "rules": "Recommendation AI in social and dating apps is limited-risk. Matching and engagement algorithms need transparency rules. Synthetic profiles or AI-generated faces must be labelled under deepfake disclosure requirements.",
    },
    "fitness-health": {
        "title": "Fitness & Wellness",
        "risk": "limited-risk",
        "rules": "Fitness trackers and wellness apps are minimal or limited risk. Symptom-checking AI that edges toward diagnosis can become high-risk medical software. Transparency about AI-generated advice is the safest first step.",
    },
    "gaming": {
        "title": "Gaming",
        "risk": "minimal-risk",
        "rules": "Most gaming AI is minimal-risk — the lightest tier with no mandatory obligations. AI NPCs and procedural generation are fine. The moment AI moderates chat or welfare systems, transparency rules appear.",
    },
    "gambling-betting": {
        "title": "Gambling & Betting",
        "risk": "limited-risk",
        "rules": "AI that personalises odds or recommends bets is limited-risk. Responsible-gambling AI that intervenes on player behaviour is scrutinised heavily. Self-exclusion enforcement by AI carries high-risk exposure.",
    },
    "espionage-surveillance": {
        "title": "Surveillance & Security",
        "risk": "high-risk",
        "rules": "AI-powered surveillance, biometric identification, and social scoring face the strictest rules. Real-time biometric ID in public is banned outside narrow law-enforcement exceptions. Any commercial product here needs a full conformity assessment.",
    },
    "ai-recruitment": {
        "title": "AI Recruitment Tools",
        "risk": "high-risk",
        "rules": "Automated hiring systems are high-risk since AI influences employment decisions. Providers must run bias testing, keep technical documentation, and give candidates the right to human review. Translated into plain language: document everything.",
    },
    "real-time-bidding": {
        "title": "Real-Time Ad Bidding",
        "risk": "limited-risk",
        "rules": "RTB and ad-auction AI are limited-risk. The transparency obligations matter most — users should know when content is AI-generated or personalised by AI. Avoid any subliminal manipulation, which is banned outright by Article 5.",
    },
    "web-apps": {
        "title": "Web Apps & SaaS",
        "risk": "limited-risk",
        "rules": "Web apps that embed AI features are limited-risk by default. The cheapest obligation is disclosing AI use to users. Upload your code to a free scanner to confirm your tier and get your first compliance score.",
    },
    "mobile-apps": {
        "title": "Mobile Apps",
        "risk": "limited-risk",
        "rules": "Mobile apps with AI features carry the same obligations as any other software. In-app transparency labels are required and AI-generated content needs labelling. Camera and microphone features can trigger biometric rules.",
    },
    "crypto-defi": {
        "title": "Crypto & DeFi",
        "risk": "limited-risk",
        "rules": "Trading-bot and portfolio AI is limited-risk. AI that makes investment decisions for users, gives regulated financial advice, or scores users can become high-risk. MiCA and the AI Act overlap, so compliance teams need both.",
    },
    "travel-tourism": {
        "title": "Travel & Tourism",
        "risk": "minimal-risk",
        "rules": "Price-comparison and booking-recommendation AI is limited to minimal risk. Making customers believe dynamic pricing is a human choice is a transparency violation. Dynamic pricing will face new EU rules in 2026.",
    },
    "food-delivery": {
        "title": "Food Delivery",
        "risk": "limited-risk",
        "rules": "Delivery-routing and demand-forecasting AI is limited-risk. Algorithmic worker-management systems that monitor or rate couriers face heavier scrutiny in Europe and are already regulated in several member states.",
    },
    "ride-hailing": {
        "title": "Ride Hailing & Mobility",
        "risk": "limited-risk",
        "rules": "Dispatch and pricing algorithms for ride-hailing are limited-risk. Worker monitoring and algorithmic deactivation decisions are the riskiest parts. Transparency around surge pricing and driver ratings is essential.",
    },
    "logistics": {
        "title": "Logistics & Freight",
        "risk": "limited-risk",
        "rules": "Route-planning and warehouse AI is limited-risk. Warehouse-automation systems interacting with workers can become high-risk. Robotics integrators carry documentation duties across the supply chain.",
    },
    "agriculture": {
        "title": "Agriculture & Agritech",
        "risk": "minimal-risk",
        "rules": "Crop-monitoring, drone, and precision-agriculture AI is minimal risk. Anything that controls safety-critical farm machinery rises in tier. Yield-prediction models are fine — document and stay transparent.",
    },
    "pharma": {
        "title": "Pharma & Biotech",
        "risk": "high-risk",
        "rules": "Drug-discovery and AI-assisted diagnostics are high-risk when they affect medical outcomes and safety. Documentation, validation, and traceability are legally required, not just good practice.",
    },
    "construction": {
        "title": "Construction",
        "risk": "limited-risk",
        "rules": "Site-monitoring and safety AI is limited-risk. Anything that controls machinery or makes safety decisions becomes high-risk. BIM and scheduling AI on its own is usually minimal risk.",
    },
    "government-services": {
        "title": "Government & Public Services",
        "risk": "high-risk",
        "rules": "Government AI for benefits, immigration, and law enforcement is heavily regulated. Real-time biometric surveillance is banned outside the narrow carve-outs. Public-sector AI needs conformity assessment and human review.",
    },
    "hr-analytics": {
        "title": "HR Analytics",
        "risk": "high-risk",
        "rules": "AI that predicts performance, attrition, or promotion potential can be high-risk because it influences employment decisions. Needs bias audits, documentation, and human oversight. Treat any employee-scoring AI with the highest care.",
    },
    "biometric": {
        "title": "Biometric Systems",
        "risk": "high-risk",
        "rules": "Biometric identification, categorisation, and emotion recognition carry the strictest rules. Several uses are banned outright — emotion recognition at work or school, social scoring, and real-time public surveillance outside law enforcement.",
    },
    "ecommerce-recs": {
        "title": "Recommendation Engines",
        "risk": "minimal-risk",
        "rules": "Recommendation engines are minimal risk unless they manipulate behaviour. Dark patterns and manipulative nudging violate the EU AI Act Article 5 and the Digital Services Act. Transparent, non-manipulative recs are safest.",
    },
    "deepfake": {
        "title": "Deepfakes",
        "risk": "limited-risk",
        "rules": "Deepfakes face strict disclosure rules. AI-generated or manipulated content that resembles real people must be labelled. Failure to label is directly punishable. Synthetic content at scale also triggers GPAI transparency obligations.",
    },
    "chatbots": {
        "title": "Chatbots",
        "risk": "limited-risk",
        "rules": "Chatbots must disclose they are AI (Article 50, already live). Emotional-manipulation tricks and subliminal techniques are banned. Any chatbot making consequential decisions needs human oversight — and a compliance scan.",
    },
    "agentic-ai": {
        "title": "Agentic AI",
        "risk": "limited-risk",
        "rules": "Autonomous agents that take actions carry emerging obligations. They must log decisions, handle failure safely, and disclose autonomy. As agentic systems touch more decisions, they trend toward high-risk classification.",
    },
    "small-business": {
        "title": "Small Businesses",
        "risk": "limited-risk",
        "rules": "SMEs using off-the-shelf AI are usually deployers, meaning fewer obligations than providers. But you still must use AI per the provider's instructions, disclose AI use, and log high-risk activity. The EU AI Act also gives SMEs priority access to sandboxes.",
    },
    "consulting-services": {
        "title": "Consulting Services",
        "risk": "limited-risk",
        "rules": "Consultancies that build AI for clients become providers and inherit technical-documentation duties. Your deliverables should include compliance artefacts from day one. Recommending compliant architecture is itself a selling point.",
    },
    "fashion-retail": {
        "title": "Fashion & Retail",
        "risk": "minimal-risk",
        "rules": "Trend-forecasting and inventory AI is minimal risk. Virtual-try-on tools using body data raise biometric and privacy concerns. Personalised-advertising AI only needs transparency obligations.",
    },
    "restaurants": {
        "title": "Restaurants & Hospitality",
        "risk": "minimal-risk",
        "rules": "Demand-forecasting, staffing, and kitchen AI is minimal risk. Guest-survey sentiment analysis needs transparency. AI that prices or manages staff schedules must be fair to employees under labour-law overlap.",
    },
    "media-news": {
        "title": "Media & News",
        "risk": "limited-risk",
        "rules": "AI-generated news content must be labelled as synthetic. Recommendation systems that amplify content face transparency and manipulation rules. Public-interest media has special editorial-responsibility carve-outs.",
    },
    "telecom": {
        "title": "Telecom",
        "risk": "limited-risk",
        "rules": "Network-optimisation and customer-experience AI is limited-risk. Call-centre sentiment analysis uses speech data — combining AI Act and GDPR duties. Anything touching biometrics (voice ID) raises the tier.",
    },
    "energy-utilities": {
        "title": "Energy & Utilities",
        "risk": "high-risk",
        "rules": "Grid-management and safety AI in critical infrastructure is high-risk. Demand-forecasting alone is limited-risk. Providers of safety-critical controls must complete impact assessments and documentation.",
    },
}

SECTIONS = [
    {
        "heading": "Do you come under the EU AI Act?",
        "body": (
            "The EU AI Act reaches any company whose AI output is used in the European Union — "
            "regardless of where the company is based. If your product has EU users or clients, "
            "the rules apply to you. The first question is always the same: which risk tier does "
            "your system fall into, and what duties come with that tier?"
        ),
    },
    {
        "heading": "Which risk tier applies to you?",
        "body": (
            "The Act sorts AI into four tiers: prohibited (banned outright), high-risk (heavy "
            "duties), limited-risk (transparency only), and minimal-risk (no mandatory duties). "
            "Most software starts in limited or minimal risk. The expensive surprises live in "
            "high-risk and prohibited — which is exactly why scanning early matters."
        ),
    },
    {
        "heading": "Ready to see your compliance score?",
        "body": (
            "Free scan. No signup. No code stored. Works for teams worldwide — because the "
            "EU AI Act applies to anyone selling to the EU."
        ),
        "cta": True,
    },
]

RELATED_BLOGS = [
    ("EU AI Act Requirements Checklist 2026", "/blog/eu-ai-act-requirements-checklist-2026"),
    ("What EU AI Act Non-Compliance Costs in 2026", "/blog/eu-ai-act-fines-2026"),
    ("EU AI Act Compliance for Indian SaaS Companies", "/blog/eu-ai-act-compliance-indian-saas-2026"),
    ("EU AI Act Compliance for Startups", "/blog/eu-ai-act-compliance-for-startups-2026"),
]

OTHER_PAGES = [
    ("Home", "/"),
    ("Features", "/features"),
    ("Pricing", "/pricing"),
    ("How It Works", "/how-it-works"),
    ("Free Resources", "/resources"),
    ("About", "/about"),
    ("Contact", "/contact"),
]


def _keyword_slug(key: str) -> str:
    return f"eu-ai-act-compliance-{key}"


def _title_for(key, data):
    return f"{data['title']} & the EU AI Act: Tier, Rules & a Free Compliance Scan"


def _description_for(key, data):
    return (
        f"EU AI Act compliance for {data['title'].lower()}. "
        f"Compute your {data['risk']} tier, the obligations that come with it, and scan your "
        f"codebase free in 2 minutes. No signup, no code stored."
    )


def _jsonld(key, data):
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": _title_for(key, data),
        "description": _description_for(key, data),
        "datePublished": "2026-09-05",
        "dateModified": "2026-09-05",
        "publisher": {"@type": "Organization", "name": "AI Compliance Shield"},
        "mainEntityOfPage": f"{BASE_URL}/{_keyword_slug(key)}",
    }


def _internal_links(key):
    out = []
    for label, url in OTHER_PAGES:
        out.append(f'<p class="art-link"><a href="{url}">{label}</a></p>')
    return "\n".join(out)


def build_page(key: str) -> str:
    data = INDUSTRIES[key]
    slug = _keyword_slug(key)
    url = f"{BASE_URL}/{slug}"
    title = _title_for(key, data)
    description = _description_for(key, data)
    h1 = f"{data['title']} under the EU AI Act: Your Compliance Guide"
    jsonld = json.dumps(_jsonld(key, data), ensure_ascii=False, indent=2)

    sections_html = ""
    for idx, sec in enumerate(SECTIONS):
        if sec.get("cta"):
            sections_html += f"""
            <div class="cta-box">
                <h3>Free EU AI Act Compliance Scan</h3>
                <p>See your score in 2 minutes. No signup, no code stored.</p>
                <a class="btn-white" href="/">Scan Your Codebase Now</a>
            </div>"""
        else:
            sections_html += f"""
            <h2>{sec['heading']}</h2>
            <p>{sec['body']}</p>"""

    related_links = "\n".join(
        f'<p class="art-link"><a href="{u}">{label}</a></p>' for label, u in RELATED_BLOGS
    )
    related_links += "\n" + _internal_links(key)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>
    <meta name="description" content="{html.escape(description)}">
    <meta name="keywords" content="{html.escape(key.replace('-', ' '))}, EU AI Act {data['title'].lower()}, AI Act compliance {data['title'].lower()}, {data['risk']} AI">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{url}">
    <link rel="icon" type="image/svg+xml" href="/static/favicon.svg">
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="{html.escape(title)}">
    <meta name="twitter:description" content="{html.escape(description)}">
    <meta property="og:title" content="{html.escape(title)}">
    <meta property="og:description" content="{html.escape(description)}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="{url}">
    <link rel="stylesheet" href="/static/style.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-QNZ5VNJ73M"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'G-QNZ5VNJ73M');
    </script>
    <script type="application/ld+json">
    {jsonld}
    </script>
    <style>
        .article {{ max-width: 820px; margin: 0 auto; padding: 48px 20px 0; }}
        .article-head {{ margin-bottom: 32px; }}
        .article-meta {{ color: #6B7280; font-size: 14px; margin-top: 16px; }}
        .article h1 {{ font-size: 40px; line-height: 1.15; color: #111827; margin: 12px 0 12px; }}
        .article h2 {{ font-size: 26px; color: #111827; margin: 44px 0 14px; border-bottom: 2px solid #E5E7EB; padding-bottom: 10px; }}
        .article p, .article li {{ color: #374151; line-height: 1.75; font-size: 16px; }}
        .article strong {{ color: #111827; }}
        .tag {{ display: inline-block; background: #EFF6FF; color: #1D4ED8; font-size: 13px; font-weight: 600; padding: 4px 10px; border-radius: 6px; }}
        .risk-box {{ background: #EFF6FF; border-left: 4px solid #2563EB; border-radius: 8px; padding: 16px 20px; margin: 20px 0; }}
        .cta-box {{ background: linear-gradient(135deg, #1D4ED8, #2563EB); color: white; border-radius: 16px; padding: 32px; text-align: center; margin: 40px 0; }}
        .cta-box h3 {{ color: white; font-size: 24px; margin-top: 0; }}
        .cta-box p {{ color: #DBEAFE; }}
        .btn-white {{ display: inline-block; background: white; color: #1D4ED8; font-weight: 700; padding: 14px 28px; border-radius: 10px; text-decoration: none; margin-top: 8px; }}
        .btn-white:hover {{ background: #F3F4F6; }}
        .more-guides {{ background: #F9FAFB; border: 1px solid #E5E7EB; border-radius: 12px; padding: 20px 24px; margin: 32px 0; }}
        .art-link a {{ color: #2563EB; text-decoration: none; }}
        .art-link a:hover {{ text-decoration: underline; }}
        @media (max-width: 640px) {{ .article h1 {{ font-size: 30px; }} .article h2 {{ font-size: 22px; }} }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="logo">
                <div class="logo-icon">
                    <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
                        <rect width="40" height="40" rx="10" fill="#2563EB"/>
                        <path d="M20 8L10 14V22C10 27.5 14.3 32.7 20 34C25.7 32.7 30 27.5 30 22V14L20 8Z" fill="white"/>
                        <path d="M17 20L19 22L23 18" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                <span class="logo-text">AI Compliance Shield</span>
            </div>
            <nav>
                <a href="/" class="nav-link">Home</a>
                <a href="/features" class="nav-link">Features</a>
                <a href="/pricing" class="nav-link">Pricing</a>
            </nav>
        </header>

        <div class="article">
            <div class="article-head">
                <span class="tag">EU AI Act · {html.escape(data['risk'])} tier</span>
                <h1>{html.escape(h1)}</h1>
                <p class="article-meta">Updated September 2026 · EU AI Act (Regulation (EU) 2024/1689)</p>
            </div>

            <p><strong>{html.escape(data['rules'])}</strong></p>

            <div class="risk-box">
                <strong>Typical risk tier: {html.escape(data['risk'])}</strong>
                <br>
                Your actual tier depends on exactly how your system is built and used. A free scan of your codebase is the fastest way to confirm it.
            </div>

            {sections_html}

            <div class="more-guides">
                <h3>Related guides</h3>
                {related_links}
            </div>
        </div>

        <footer>
            <div class="footer-content">
                <div class="footer-brand">
                    <div class="logo">
                        <div class="logo-icon">
                            <svg width="32" height="32" viewBox="0 0 40 40" fill="none">
                                <rect width="40" height="40" rx="10" fill="#2563EB"/>
                                <path d="M20 8L10 14V22C10 27.5 14.3 32.7 20 34C25.7 32.7 30 27.5 30 22V14L20 8Z" fill="white"/>
                            </svg>
                        </div>
                        <span class="logo-text">AI Compliance Shield</span>
                    </div>
                    <p>Protecting companies from EU AI Act fines since 2026.</p>
                </div>
                <div class="footer-links">
                    <a href="/">Home</a>
                    <a href="/features">Features</a>
                    <a href="/how-it-works">How It Works</a>
                    <a href="/pricing">Pricing</a>
                    <a href="/resources">Free Guides</a>
                    <a href="/about">About</a>
                    <a href="/contact">Contact</a>
                    <a href="/privacy-policy">Privacy Policy</a>
                    <a href="/terms">Terms</a>
                    <a href="/refund-policy">Refund Policy</a>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2026 AI Compliance Shield. All rights reserved.</p>
            </div>
        </footer>
    </div>
</body>
</html>
"""


def all_slugs() -> list:
    return sorted(INDUSTRIES.keys())


def build_sitemap_xml() -> str:
    from datetime import date

    today = date.today().isoformat()
    entries = [
        {"loc": BASE_URL, "priority": "1.0", "freq": "weekly"},
        {"loc": f"{BASE_URL}/pricing", "priority": "0.9", "freq": "monthly"},
        {"loc": f"{BASE_URL}/features", "priority": "0.8", "freq": "monthly"},
        {"loc": f"{BASE_URL}/how-it-works", "priority": "0.8", "freq": "monthly"},
        {"loc": f"{BASE_URL}/resources", "priority": "0.8", "freq": "weekly"},
        {"loc": f"{BASE_URL}/about", "priority": "0.3", "freq": "yearly"},
        {"loc": f"{BASE_URL}/contact", "priority": "0.3", "freq": "yearly"},
        {"loc": f"{BASE_URL}/privacy-policy", "priority": "0.3", "freq": "yearly"},
        {"loc": f"{BASE_URL}/terms", "priority": "0.3", "freq": "yearly"},
        {"loc": f"{BASE_URL}/refund-policy", "priority": "0.3", "freq": "yearly"},
        {"loc": f"{BASE_URL}/blog/eu-ai-act-requirements-checklist-2026", "priority": "0.8", "freq": "monthly"},
        {"loc": f"{BASE_URL}/blog/eu-ai-act-fines-2026", "priority": "0.8", "freq": "monthly"},
        {"loc": f"{BASE_URL}/blog/eu-ai-act-compliance-indian-saas-2026", "priority": "0.8", "freq": "monthly"},
        {"loc": f"{BASE_URL}/blog/eu-ai-act-compliance-for-startups-2026", "priority": "0.8", "freq": "monthly"},
    ]
    for key in all_slugs():
        entries.append({
            "loc": f"{BASE_URL}/{_keyword_slug(key)}",
            "priority": "0.7",
            "freq": "monthly",
        })

    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for e in entries:
        lines.append("  <url>")
        lines.append(f"    <loc>{e['loc']}</loc>")
        lines.append(f"    <lastmod>{today}</lastmod>")
        lines.append(f"    <changefreq>{e['freq']}</changefreq>")
        lines.append(f"    <priority>{e['priority']}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines)