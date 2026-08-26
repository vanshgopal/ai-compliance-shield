# AI Compliance Shield

## 🛡️ EU AI Act Compliance Audit Tool for SMEs

An automated compliance scanning, reporting, and remediation planning tool designed to help Small and Medium Enterprises (SMEs) comply with the EU AI Act (Regulation 2024/1689).

### ⚠️ Important Deadline

**EU AI Act Enforcement: August 2, 2026**

Penalties for non-compliance:
- Up to **€35 million** or **7% of global annual turnover** for prohibited AI practices
- Up to **€15 million** or **3% of global annual turnover** for high-risk AI violations

### 🚀 Features

- **Code Scanning**: Detects AI/ML libraries, model training code, and inference pipelines
- **Configuration Auditing**: Reviews configuration files for AI settings and security issues
- **API & Dependency Analysis**: Identifies AI service integrations and ML package dependencies
- **Compliance Scoring**: Calculates overall compliance score based on EU AI Act requirements
- **PDF Reports**: Generates professional compliance reports with detailed findings
- **Interactive Dashboard**: Visualizes compliance status with charts and metrics
- **Remediation Planning**: Creates prioritized action plans for achieving compliance

### 📋 What We Scan

| Category | Detection |
|----------|-----------|
| Code | Python, JavaScript, TypeScript, Java, Go, Rust, C++, C#, Ruby, PHP, R, Scala |
| Config | YAML, JSON, TOML, INI, .env files |
| Dependencies | requirements.txt, package.json, pyproject.toml, Pipfile |
| AI Services | OpenAI, Anthropic, Cohere, Hugging Face, Ollama |
| ML Libraries | TensorFlow, PyTorch, scikit-learn, XGBoost, LightGBM |

### 🏗️ Project Structure

```
ai-compliance-shield/
├── backend/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── compliance/
│   │   ├── __init__.py
│   │   └── eu_ai_act.py     # EU AI Act rules engine
│   ├── scanners/
│   │   ├── __init__.py
│   │   ├── code_scanner.py  # Source code analysis
│   │   ├── config_scanner.py # Configuration file analysis
│   │   └── api_scanner.py   # API and dependency analysis
│   └── reports/
│       ├── __init__.py
│       └── pdf_generator.py # PDF report generation
├── frontend/
│   ├── static/
│   │   ├── style.css        # Dashboard styling
│   │   └── app.js           # Frontend JavaScript
│   └── templates/
│       ├── index.html       # Landing page
│       └── dashboard.html   # Results dashboard
├── data/
│   ├── uploads/             # Uploaded project files
│   └── reports/             # Generated PDF reports
├── requirements.txt         # Python dependencies
├── run.py                   # Server entry point
└── README.md                # This file
```

### 🛠️ Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 🚀 Running the Application

```bash
# Start the server
python run.py

# Or using uvicorn directly
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Open your browser and navigate to: **http://localhost:8000**

### 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Landing page |
| `/api/scan/upload` | POST | Scan uploaded files |
| `/api/scan/path` | POST | Scan local directory |
| `/api/report/{scan_id}/pdf` | GET | Download PDF report |
| `/api/report/{scan_id}/json` | GET | Get report as JSON |
| `/api/requirements` | GET | List EU AI Act requirements |
| `/api/scans` | GET | List all scans |
| `/dashboard/{scan_id}` | GET | View results dashboard |

### 💰 Pricing Model

| Plan | Price | Features |
|------|-------|----------|
| Starter | $500/month | Up to 3 scans/month, basic report |
| Professional | $1,200/month | Unlimited scans, full dashboard, remediation |
| Enterprise | $2,000/month | Custom rules, API access, dedicated support |

### 🎯 Target Market

- **25+ million SMEs** in the European Union
- Fewer than 5 funded competitors in the SME segment
- Most existing tools target enterprises only

### 📝 EU AI Act Requirements Covered

| ID | Requirement | Article | Risk Level |
|----|-------------|---------|------------|
| RA-001 | Risk Management System | Article 9 | High |
| RA-002 | Data Governance | Article 10 | High |
| RA-003 | Technical Documentation | Article 11 | High |
| RA-004 | Record-Keeping / Logging | Article 12 | High |
| RA-005 | Transparency & Information | Article 13 | High |
| RA-006 | Human Oversight | Article 14 | High |
| RA-007 | Accuracy, Robustness & Security | Article 15 | High |
| RA-008 | Conformity Assessment | Article 43 | High |
| RA-009 | EU Database Registration | Article 49 | High |
| RA-010 | Post-Market Monitoring | Article 72 | High |
| RA-011 | Incident Reporting | Article 73 | High |
| RA-012 | Transparency for Limited Risk | Article 50 | Limited |
| RA-013 | Deepfake Disclosure | Article 50 | Limited |
| RA-014 | Prohibited AI Practices | Article 5 | Unacceptable |
| RA-015 | Foundation Model Requirements | Articles 51-56 | Limited |

### 📄 License

Proprietary - All rights reserved.

### 🤝 Support

For questions or support, contact: support@ai-compliance-shield.com
