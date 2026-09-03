"""AI Compliance Shield - FastAPI Backend.

Automated EU AI Act compliance audit tool for SMEs.
"""

import os
import json
import shutil
import time
from pathlib import Path
from datetime import datetime
from typing import Optional
from collections import defaultdict

from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel

from .compliance.eu_ai_act import (
    ComplianceReport, Finding, ComplianceStatus, RiskCategory,
    classify_risk_level, get_requirements_for_risk,
    calculate_compliance_score, generate_remediation_plan,
    EU_AI_ACT_REQUIREMENTS
)
from .scanners.code_scanner import CodeScanner
from .scanners.config_scanner import ConfigScanner
from .scanners.api_scanner import APIScanner
from .reports.pdf_generator import PDFReportGenerator

app = FastAPI(
    title="AI Compliance Shield",
    description="EU AI Act Compliance Audit Tool for SMEs",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://aicomplianceshield.site", "https://www.aicomplianceshield.site"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
    allow_credentials=True,
)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://checkout.razorpay.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self' https://www.google-analytics.com https://api.razorpay.com;"
        return response


app.add_middleware(SecurityHeadersMiddleware)


rate_limit_store = defaultdict(list)
RATE_LIMIT_REQUESTS = 60
RATE_LIMIT_WINDOW = 60


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        USER_AGENT = request.headers.get("user-agent", "").lower()
        ALLOWED_BOTS = ["googlebot", "bingbot", "yandex", "duckduckbot", "baiduspider", "slurp"]
        if any(bot in USER_AGENT for bot in ALLOWED_BOTS):
            return await call_next(request)
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        rate_limit_store[client_ip] = [
            t for t in rate_limit_store[client_ip] if now - t < RATE_LIMIT_WINDOW
        ]
        if len(rate_limit_store[client_ip]) >= RATE_LIMIT_REQUESTS:
            return JSONResponse(
                status_code=429,
                content={"error": "Too many requests. Please try again later."},
            )
        rate_limit_store[client_ip].append(now)
        return await call_next(request)


app.add_middleware(RateLimitMiddleware)

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = DATA_DIR / "uploads"
REPORTS_DIR = DATA_DIR / "reports"

UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

STATIC_DIR = FRONTEND_DIR / "static"
TEMPLATES_DIR = FRONTEND_DIR / "templates"

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


def _find_template(name: str) -> Path:
    flat = TEMPLATES_DIR / name
    if flat.exists():
        return flat
    return TEMPLATES_DIR / name


class ScanRequest(BaseModel):
    company_name: str
    project_path: Optional[str] = None


class ScanResponse(BaseModel):
    scan_id: str
    company_name: str
    scan_date: str
    overall_score: float
    risk_category: str
    findings_count: int
    report_url: str
    dashboard_url: str


scan_history = {}


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return HTMLResponse(content=_find_template("index.html").read_text(encoding="utf-8"))


@app.get("/get-started", response_class=HTMLResponse)
async def get_started(request: Request):
    return HTMLResponse(content=_find_template("index.html").read_text(encoding="utf-8"))


@app.get("/resources", response_class=HTMLResponse)
async def resources_page(request: Request):
    return HTMLResponse(content=_find_template("resources.html").read_text(encoding="utf-8"))


@app.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    return HTMLResponse(content=_find_template("about.html").read_text(encoding="utf-8"))


@app.get("/contact", response_class=HTMLResponse)
async def contact_page(request: Request):
    return HTMLResponse(content=_find_template("contact.html").read_text(encoding="utf-8"))


@app.get("/features", response_class=HTMLResponse)
async def features_page(request: Request):
    return HTMLResponse(content=_find_template("features.html").read_text(encoding="utf-8"))


@app.get("/how-it-works", response_class=HTMLResponse)
async def how_it_works_page(request: Request):
    return HTMLResponse(content=_find_template("how-it-works.html").read_text(encoding="utf-8"))


@app.get("/privacy-policy", response_class=HTMLResponse)
async def privacy_policy_page(request: Request):
    return HTMLResponse(content=_find_template("privacy-policy.html").read_text(encoding="utf-8"))


@app.get("/terms", response_class=HTMLResponse)
async def terms_page(request: Request):
    return HTMLResponse(content=_find_template("terms.html").read_text(encoding="utf-8"))


@app.get("/refund-policy", response_class=HTMLResponse)
async def refund_policy_page(request: Request):
    return HTMLResponse(content=_find_template("refund-policy.html").read_text(encoding="utf-8"))


@app.get("/blog/{slug}", response_class=HTMLResponse)
async def blog_page(request: Request, slug: str):
    flat = BASE_DIR / "blog" / f"{slug}.html"
    nested = TEMPLATES_DIR / "blog" / f"{slug}.html"
    path = flat if flat.exists() else nested
    if path.exists():
        return HTMLResponse(content=path.read_text(encoding="utf-8"))
    return HTMLResponse(content=_find_template("index.html").read_text(encoding="utf-8"))


@app.post("/api/scan/upload")
async def scan_upload(
    company_name: str = "Unknown Company",
    files: list[UploadFile] = File(...),
):
    total_size = 0
    MAX_UPLOAD_SIZE = 10 * 1024 * 1024
    for file in files:
        content = await file.read()
        total_size += len(content)
        if total_size > MAX_UPLOAD_SIZE:
            raise HTTPException(status_code=413, detail="Total upload size exceeds 10MB limit")
        file.file.seek(0)

    scan_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    scan_dir = UPLOADS_DIR / scan_id
    scan_dir.mkdir(parents=True, exist_ok=True)

    for file in files:
        safe_name = Path(file.filename).name
        file_path = scan_dir / safe_name
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

    report = _run_scan(company_name, str(scan_dir))
    scan_history[scan_id] = report

    return ScanResponse(
        scan_id=scan_id,
        company_name=company_name,
        scan_date=report.scan_date,
        overall_score=report.overall_score,
        risk_category=report.risk_category.value,
        findings_count=len(report.findings),
        report_url=f"/api/report/{scan_id}/pdf",
        dashboard_url=f"/dashboard/{scan_id}",
    )


@app.post("/api/scan/path")
async def scan_path(request: ScanRequest):
    scan_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    project_path = Path(request.project_path)

    if not project_path.exists():
        raise HTTPException(status_code=400, detail="Project path does not exist")

    report = _run_scan(request.company_name, str(project_path))
    scan_history[scan_id] = report

    return ScanResponse(
        scan_id=scan_id,
        company_name=request.company_name,
        scan_date=report.scan_date,
        overall_score=report.overall_score,
        risk_category=report.risk_category.value,
        findings_count=len(report.findings),
        report_url=f"/api/report/{scan_id}/pdf",
        dashboard_url=f"/dashboard/{scan_id}",
    )


@app.get("/api/report/{scan_id}/pdf")
async def download_pdf(scan_id: str):
    if scan_id not in scan_history:
        raise HTTPException(status_code=404, detail="Scan not found")

    report = scan_history[scan_id]
    generator = PDFReportGenerator(str(REPORTS_DIR))
    pdf_path = generator.generate(report)

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=f"compliance_report_{scan_id}.pdf",
    )


@app.get("/api/report/{scan_id}/json")
async def get_report_json(scan_id: str):
    if scan_id not in scan_history:
        raise HTTPException(status_code=404, detail="Scan not found")

    report = scan_history[scan_id]
    return {
        "scan_id": scan_id,
        "company_name": report.company_name,
        "scan_date": report.scan_date,
        "overall_score": report.overall_score,
        "risk_category": report.risk_category.value,
        "findings": [
            {
                "requirement_id": f.requirement_id,
                "status": f.status.value,
                "evidence": f.evidence,
                "risk_level": f.risk_level,
                "recommendation": f.recommendation,
                "file_path": f.file_path,
                "line_number": f.line_number,
            }
            for f in report.findings
        ],
        "remediation_plan": report.remediation_plan,
    }


@app.get("/dashboard/{scan_id}", response_class=HTMLResponse)
async def dashboard(request: Request, scan_id: str):
    if scan_id not in scan_history:
        return HTMLResponse(content=_find_template("index.html").read_text(encoding="utf-8"))

    report = scan_history[scan_id]
    import jinja2
    tmpl_dir = str(TEMPLATES_DIR if TEMPLATES_DIR.exists() else BASE_DIR)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(tmpl_dir))
    tmpl = env.get_template("dashboard.html")
    html = tmpl.render(scan_id=scan_id, report=report)
    return HTMLResponse(content=html)


@app.get("/api/requirements")
async def get_requirements():
    return [
        {
            "id": r.id,
            "title": r.title,
            "description": r.description,
            "risk_category": r.risk_category.value,
            "article": r.article,
            "deadline": r.deadline,
            "penalty_range": r.penalty_range,
        }
        for r in EU_AI_ACT_REQUIREMENTS
    ]


@app.get("/api/scans")
async def list_scans():
    return [
        {
            "scan_id": sid,
            "company_name": r.company_name,
            "scan_date": r.scan_date,
            "overall_score": r.overall_score,
            "risk_category": r.risk_category.value,
        }
        for sid, r in scan_history.items()
    ]


@app.get("/pricing", response_class=HTMLResponse)
async def pricing_page(request: Request):
    return HTMLResponse(content=_find_template("pricing.html").read_text(encoding="utf-8"))


@app.get("/payment-success", response_class=HTMLResponse)
async def payment_success(request: Request):
    return HTMLResponse(content="""
    <html>
    <head><title>Payment Successful</title></head>
    <body style="font-family: Inter, sans-serif; text-align: center; padding: 100px;">
        <h1>Payment Successful!</h1>
        <p>Thank you for your purchase.</p>
        <a href="/" style="color: #2563EB;">Go to Dashboard</a>
    </body>
    </html>
    """)


@app.get("/api/payment/config")
async def payment_config():
    return {"key_id": os.getenv("RAZORPAY_KEY_ID", "")}


@app.post("/api/payment/create-order")
async def create_order(request: Request):
    try:
        import razorpay
        body = await request.json()
        plan = body.get("plan", "starter")
        company = body.get("company", "")
        email = body.get("email", "")

        PRICES = {"starter": 2499900, "professional": 5999900, "enterprise": 9999900}
        amount = PRICES.get(plan, 2499900)

        client = razorpay.Client(auth=(
            os.getenv("RAZORPAY_KEY_ID", ""),
            os.getenv("RAZORPAY_KEY_SECRET", ""),
        ))

        order = client.order.create({
            "amount": amount,
            "currency": "INR",
            "receipt": f"{plan}_{company}",
            "notes": {"plan": plan, "company": company, "email": email},
        })

        return {
            "order_id": order["id"],
            "amount": order["amount"],
            "currency": order["currency"],
            "key_id": os.getenv("RAZORPAY_KEY_ID", ""),
        }
    except Exception as e:
        return {"error": str(e)}


@app.post("/api/payment/verify")
async def verify_payment(request: Request):
    try:
        import razorpay
        body = await request.json()

        client = razorpay.Client(auth=(
            os.getenv("RAZORPAY_KEY_ID", ""),
            os.getenv("RAZORPAY_KEY_SECRET", ""),
        ))

        client.utility.verify_payment_signature({
            "razorpay_order_id": body.get("razorpay_order_id"),
            "razorpay_payment_id": body.get("razorpay_payment_id"),
            "razorpay_signature": body.get("razorpay_signature"),
        })

        return {"success": True}
    except Exception:
        return {"success": False}


@app.post("/api/leads")
async def create_lead(request: Request):
    try:
        body = await request.json()
        leads_file = DATA_DIR / "leads.json"
        leads = []
        if leads_file.exists():
            leads = json.loads(leads_file.read_text(encoding="utf-8"))
        leads.append({
            "name": body.get("name"),
            "email": body.get("email"),
            "company": body.get("company"),
            "status": body.get("status", "new"),
            "notes": body.get("notes", ""),
            "date": datetime.now().isoformat(),
        })
        leads_file.write_text(json.dumps(leads, indent=2), encoding="utf-8")
        return {"success": True}
    except Exception:
        return {"success": False}


@app.get("/sitemap.xml", response_class=Response)
async def sitemap():
    path = STATIC_DIR / "sitemap.xml"
    if path.exists():
        return Response(
            content=path.read_text(encoding="utf-8"),
            media_type="application/xml",
            headers={"Content-Type": "application/xml; charset=utf-8"},
        )
    return Response(content="Not found", status_code=404)


@app.get("/robots.txt", response_class=Response)
async def robots():
    path = STATIC_DIR / "robots.txt"
    if path.exists():
        return Response(
            content=path.read_text(encoding="utf-8"),
            media_type="text/plain",
            headers={"Content-Type": "text/plain; charset=utf-8"},
        )
    return Response(content="User-agent: *\nAllow: /", media_type="text/plain")


@app.post("/api/contact")
async def contact_form(request: Request):
    try:
        body = await request.json()
        name = body.get("name", "")
        email = body.get("email", "")
        company = body.get("company", "")
        message = body.get("message", "")
        if not name or not email or not message:
            return {"success": False, "error": "Name, email, and message are required"}
        leads_file = DATA_DIR / "contacts.json"
        contacts = []
        if leads_file.exists():
            contacts = json.loads(leads_file.read_text(encoding="utf-8"))
        contacts.append({
            "name": name, "email": email, "company": company,
            "message": message, "date": datetime.now().isoformat(),
        })
        leads_file.write_text(json.dumps(contacts, indent=2), encoding="utf-8")
        return {"success": True}
    except Exception:
        return {"success": False, "error": "Failed to send message"}


@app.post("/api/referral/track")
async def track_referral(request: Request):
    try:
        body = await request.json()
        referrals_file = DATA_DIR / "referrals.json"
        referrals = []
        if referrals_file.exists():
            referrals = json.loads(referrals_file.read_text(encoding="utf-8"))
        referrals.append({
            "code": body.get("referral_code"),
            "page": body.get("page"),
            "date": datetime.now().isoformat(),
        })
        referrals_file.write_text(json.dumps(referrals, indent=2), encoding="utf-8")
        return {"success": True}
    except Exception:
        return {"success": False}


@app.post("/api/newsletter/subscribe")
async def subscribe_newsletter(request: Request):
    try:
        body = await request.json()
        email = body.get("email", "")
        if not email or not "@" in email:
            return {"success": False, "error": "Valid email required"}
        subs_file = DATA_DIR / "subscribers.json"
        subs = []
        if subs_file.exists():
            subs = json.loads(subs_file.read_text(encoding="utf-8"))
        if any(s.get("email") == email for s in subs):
            return {"success": True, "message": "Already subscribed"}
        subs.append({
            "email": email,
            "subscribed": datetime.now().isoformat(),
            "source": body.get("source", "website"),
        })
        subs_file.write_text(json.dumps(subs, indent=2), encoding="utf-8")
        return {"success": True}
    except Exception:
        return {"success": False}


def _read_html(name: str) -> str:
    for d in [TEMPLATES_DIR, BASE_DIR]:
        p = d / name
        if p.exists():
            return p.read_text(encoding="utf-8")
    return "<h1>Page not found</h1><p><a href='/'>Go home</a></p>"


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return HTMLResponse(content=_read_html("404.html"), status_code=404)


def _run_scan(company_name: str, project_path: str) -> ComplianceReport:
    code_scanner = CodeScanner(project_path)
    config_scanner = ConfigScanner(project_path)
    api_scanner = APIScanner(project_path)

    code_results = code_scanner.scan()
    config_results = config_scanner.scan()
    api_results = api_scanner.scan()

    all_findings = []
    all_findings.extend(code_results.get("findings", []))
    all_findings.extend(config_results.get("findings", []))
    all_findings.extend(api_results.get("findings", []))

    if not all_findings:
        all_findings.append(Finding(
            requirement_id="RA-005",
            status=ComplianceStatus.COMPLIANT,
            evidence="No AI/ML systems detected in the scanned project.",
            risk_level="none",
            recommendation="Continue monitoring for AI/ML usage. Consider implementing AI governance policies proactively."
        ))

    overall_score = calculate_compliance_score(all_findings)

    has_high_risk = any(
        kw in str(code_results).lower()
        for kw in ["biometric", "hiring", "credit", "medical", "law enforcement"]
    )
    risk_category = RiskCategory.HIGH if has_high_risk else RiskCategory.LIMITED

    remediation_plan = generate_remediation_plan(all_findings)

    summary_parts = []
    if code_results.get("ai_files"):
        summary_parts.append(f"AI code detected in {len(code_results['ai_files'])} files")
    if code_results.get("training_code"):
        summary_parts.append(f"Training operations in {len(code_results['training_code'])} locations")
    if api_results.get("ai_dependencies"):
        summary_parts.append(f"{len(api_results['ai_dependencies'])} AI dependencies found")
    if config_results.get("security_issues"):
        summary_parts.append(f"{len(config_results['security_issues'])} security issues")

    summary = ". ".join(summary_parts) if summary_parts else "No significant AI usage detected."

    return ComplianceReport(
        company_name=company_name,
        scan_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        overall_score=overall_score,
        risk_category=risk_category,
        findings=all_findings,
        summary=summary,
        remediation_plan=remediation_plan,
    )
