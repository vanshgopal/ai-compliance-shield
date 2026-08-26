"""EU AI Act Compliance Rules Engine.

Defines risk categories, compliance requirements, and scoring rules
based on the EU AI Act (Regulation 2024/1689).
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class RiskCategory(Enum):
    """EU AI Act risk classification levels."""
    UNACCEPTABLE = "unacceptable"
    HIGH = "high"
    LIMITED = "limited"
    MINIMAL = "minimal"


class ComplianceStatus(Enum):
    COMPLIANT = "compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    NON_COMPLIANT = "non_compliant"
    NOT_APPLICABLE = "not_applicable"


@dataclass
class ComplianceRequirement:
    id: str
    title: str
    description: str
    risk_category: RiskCategory
    article: str
    deadline: str
    penalty_range: str
    weight: float = 1.0


@dataclass
class Finding:
    requirement_id: str
    status: ComplianceStatus
    evidence: str
    risk_level: str
    recommendation: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None


@dataclass
class ComplianceReport:
    company_name: str
    scan_date: str
    overall_score: float
    risk_category: RiskCategory
    findings: list[Finding]
    summary: str
    remediation_plan: list[dict]


EU_AI_ACT_REQUIREMENTS = [
    ComplianceRequirement(
        id="RA-001",
        title="Risk Management System",
        description="Establish, implement, and maintain a risk management system for high-risk AI systems.",
        risk_category=RiskCategory.HIGH,
        article="Article 9",
        deadline="Aug 2, 2026",
        penalty_range="Up to €15M or 3% global turnover",
        weight=1.5
    ),
    ComplianceRequirement(
        id="RA-002",
        title="Data Governance",
        description="Training, validation, and testing datasets must meet quality criteria.",
        risk_category=RiskCategory.HIGH,
        article="Article 10",
        deadline="Aug 2, 2026",
        penalty_range="Up to €15M or 3% global turnover",
        weight=1.3
    ),
    ComplianceRequirement(
        id="RA-003",
        title="Technical Documentation",
        description="Maintain technical documentation describing AI system design and development.",
        risk_category=RiskCategory.HIGH,
        article="Article 11",
        deadline="Aug 2, 2026",
        penalty_range="Up to €15M or 3% global turnover",
        weight=1.2
    ),
    ComplianceRequirement(
        id="RA-004",
        title="Record-Keeping / Logging",
        description="AI systems must have automatic logging capabilities for traceability.",
        risk_category=RiskCategory.HIGH,
        article="Article 12",
        deadline="Aug 2, 2026",
        penalty_range="Up to €15M or 3% global turnover",
        weight=1.0
    ),
    ComplianceRequirement(
        id="RA-005",
        title="Transparency & Information to Deployers",
        description="Provide deployers with clear information about AI system capabilities and limitations.",
        risk_category=RiskCategory.HIGH,
        article="Article 13",
        deadline="Aug 2, 2026",
        penalty_range="Up to €15M or 3% global turnover",
        weight=1.2
    ),
    ComplianceRequirement(
        id="RA-006",
        title="Human Oversight",
        description="Design AI systems to allow effective human oversight and intervention.",
        risk_category=RiskCategory.HIGH,
        article="Article 14",
        deadline="Aug 2, 2026",
        penalty_range="Up to €15M or 3% global turnover",
        weight=1.4
    ),
    ComplianceRequirement(
        id="RA-007",
        title="Accuracy, Robustness & Cybersecurity",
        description="AI systems must be accurate, robust, and secure throughout lifecycle.",
        risk_category=RiskCategory.HIGH,
        article="Article 15",
        deadline="Aug 2, 2026",
        penalty_range="Up to €15M or 3% global turnover",
        weight=1.3
    ),
    ComplianceRequirement(
        id="RA-008",
        title="Conformity Assessment",
        description="High-risk AI systems must undergo conformity assessment before market placement.",
        risk_category=RiskCategory.HIGH,
        article="Article 43",
        deadline="Aug 2, 2026",
        penalty_range="Up to €15M or 3% global turnover",
        weight=1.5
    ),
    ComplianceRequirement(
        id="RA-009",
        title="EU Database Registration",
        description="Register high-risk AI systems in the EU database before market placement.",
        risk_category=RiskCategory.HIGH,
        article="Article 49",
        deadline="Aug 2, 2026",
        penalty_range="Up to €15M or 3% global turnover",
        weight=1.0
    ),
    ComplianceRequirement(
        id="RA-010",
        title="Post-Market Monitoring",
        description="Establish post-market monitoring system for high-risk AI systems.",
        risk_category=RiskCategory.HIGH,
        article="Article 72",
        deadline="Aug 2, 2026",
        penalty_range="Up to €15M or 3% global turnover",
        weight=1.1
    ),
    ComplianceRequirement(
        id="RA-011",
        title="Incident Reporting",
        description="Report serious incidents to market surveillance authorities.",
        risk_category=RiskCategory.HIGH,
        article="Article 73",
        deadline="Aug 2, 2026",
        penalty_range="Up to €15M or 3% global turnover",
        weight=1.2
    ),
    ComplianceRequirement(
        id="RA-012",
        title="Transparency for Limited Risk AI",
        description="Inform users they are interacting with an AI system.",
        risk_category=RiskCategory.LIMITED,
        article="Article 50",
        deadline="Aug 2, 2025",
        penalty_range="Up to €7.5M or 1% global turnover",
        weight=1.0
    ),
    ComplianceRequirement(
        id="RA-013",
        title="Deepfake Disclosure",
        description="Disclose AI-generated content that resembles natural persons.",
        risk_category=RiskCategory.LIMITED,
        article="Article 50",
        deadline="Aug 2, 2025",
        penalty_range="Up to €7.5M or 1% global turnover",
        weight=1.0
    ),
    ComplianceRequirement(
        id="RA-014",
        title="Prohibited AI Practices",
        description="Ban on subliminal manipulation, social scoring, and real-time biometric identification.",
        risk_category=RiskCategory.UNACCEPTABLE,
        article="Article 5",
        deadline="Feb 2, 2025",
        penalty_range="Up to €35M or 7% global turnover",
        weight=2.0
    ),
    ComplianceRequirement(
        id="RA-015",
        title="Foundation Model Requirements",
        description="General-purpose AI models must comply with transparency and copyright obligations.",
        risk_category=RiskCategory.LIMITED,
        article="Articles 51-56",
        deadline="Aug 2, 2025",
        penalty_range="Up to €15M or 3% global turnover",
        weight=1.3
    ),
]

AI_KEYWORDS = [
    "model", "prediction", "classification", "regression", "neural",
    "deep learning", "machine learning", "ml", "ai", "artificial intelligence",
    "tensorflow", "pytorch", "keras", "sklearn", "scikit", "xgboost",
    "transformer", "bert", "gpt", "llm", "embedding", "fine-tune",
    "training", "inference", "dataset", "label", "annotation",
    "pipeline", "deploy", "endpoint", "api/model", "/predict",
    "openai", "anthropic", "cohere", "huggingface", "ollama",
    "langchain", "llamaindex", "chromadb", "pinecone", "weaviate",
    "opencv", "mediapipe", "yolo", "segmentation", "detection",
]

RISK_INDICATORS = {
    "high": [
        "biometric", "facial recognition", "credit scoring", "hiring",
        "recruitment", "law enforcement", "migration", "asylum",
        "education", "grading", "assessment", "medical", "diagnosis",
        "clinical", "safety", "critical infrastructure", "autonomous",
        "self-driving", "robot", "decision making", "automated decision",
    ],
    "limited": [
        "chatbot", "recommendation", "content generation", "translation",
        "spam filter", "weather", "gaming", "entertainment", "customer service",
    ],
    "minimal": [
        "spam filter", "game", "entertainment", "inventory", "weather forecast",
    ]
}


def classify_risk_level(text: str) -> RiskCategory:
    text_lower = text.lower()
    for keyword in RISK_INDICATORS["high"]:
        if keyword in text_lower:
            return RiskCategory.HIGH
    for keyword in RISK_INDICATORS["limited"]:
        if keyword in text_lower:
            return RiskCategory.LIMITED
    for keyword in RISK_INDICATORS["minimal"]:
        if keyword in text_lower:
            return RiskCategory.MINIMAL
    return RiskCategory.MINIMAL


def get_requirements_for_risk(risk: RiskCategory) -> list[ComplianceRequirement]:
    if risk == RiskCategory.UNACCEPTABLE:
        return [r for r in EU_AI_ACT_REQUIREMENTS if r.risk_category == RiskCategory.UNACCEPTABLE]
    elif risk == RiskCategory.HIGH:
        return EU_AI_ACT_REQUIREMENTS
    elif risk == RiskCategory.LIMITED:
        return [r for r in EU_AI_ACT_REQUIREMENTS
                if r.risk_category in (RiskCategory.LIMITED, RiskCategory.MINIMAL)]
    return [r for r in EU_AI_ACT_REQUIREMENTS if r.risk_category == RiskCategory.MINIMAL]


def calculate_compliance_score(findings: list[Finding]) -> float:
    if not findings:
        return 100.0
    total_weight = 0.0
    weighted_score = 0.0
    for finding in findings:
        req = next((r for r in EU_AI_ACT_REQUIREMENTS if r.id == finding.requirement_id), None)
        weight = req.weight if req else 1.0
        total_weight += weight
        if finding.status == ComplianceStatus.COMPLIANT:
            weighted_score += weight * 100
        elif finding.status == ComplianceStatus.PARTIALLY_COMPLIANT:
            weighted_score += weight * 50
        elif finding.status == ComplianceStatus.NON_COMPLIANT:
            weighted_score += weight * 0
    return round(weighted_score / total_weight, 1) if total_weight > 0 else 100.0


def generate_remediation_plan(findings: list[Finding]) -> list[dict]:
    plan = []
    priority_order = {
        ComplianceStatus.NON_COMPLIANT: 1,
        ComplianceStatus.PARTIALLY_COMPLIANT: 2,
        ComplianceStatus.COMPLIANT: 3,
        ComplianceStatus.NOT_APPLICABLE: 4,
    }
    sorted_findings = sorted(findings, key=lambda f: priority_order.get(f.status, 5))
    for i, finding in enumerate(sorted_findings):
        req = next((r for r in EU_AI_ACT_REQUIREMENTS if r.id == finding.requirement_id), None)
        if req and finding.status != ComplianceStatus.COMPLIANT:
            plan.append({
                "step": i + 1,
                "requirement_id": finding.requirement_id,
                "title": req.title,
                "status": finding.status.value,
                "recommendation": finding.recommendation,
                "deadline": req.deadline,
                "priority": "HIGH" if finding.status == ComplianceStatus.NON_COMPLIANT else "MEDIUM",
                "estimated_effort": _estimate_effort(finding),
            })
    return plan


def _estimate_effort(finding: Finding) -> str:
    if finding.status == ComplianceStatus.NON_COMPLIANT:
        return "2-4 weeks"
    elif finding.status == ComplianceStatus.PARTIALLY_COMPLIANT:
        return "1-2 weeks"
    return "1-3 days"
