"""API Scanner - Analyzes API endpoints and dependencies for AI usage."""

import os
import re
from pathlib import Path
from typing import Optional
from ..compliance.eu_ai_act import ComplianceStatus, Finding


class APIScanner:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.findings = []

    def scan(self) -> dict:
        results = {
            "api_endpoints": [],
            "ai_dependencies": [],
            "external_services": [],
            "data_flow": [],
            "findings": [],
        }

        for root, dirs, files in os.walk(self.project_path):
            dirs[:] = [d for d in dirs if d not in {".git", "node_modules", "__pycache__", ".venv"}]
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix in [".py", ".js", ".ts", ".go", ".java"]:
                    self._scan_api_file(file_path, results)
                elif file_path.name in ["requirements.txt", "package.json", "pyproject.toml", "Pipfile"]:
                    self._scan_dependencies(file_path, results)

        self._analyze_api_findings(results)
        return results

    def _scan_api_file(self, file_path: Path, results: dict):
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            relative_path = str(file_path.relative_to(self.project_path))
            lines = content.splitlines()

            api_patterns = [
                (r"@app\.(get|post|put|delete|patch)\s*\(", "fastapi"),
                (r"@route\s*\(", "flask"),
                (r"app\.(get|post|put|delete)\s*\(", "express"),
                (r"router\.(get|post|put|delete)\s*\(", "express"),
                (r"func.*Handle.*\(w\s+\*http\.ResponseWriter", "go"),
            ]

            for i, line in enumerate(lines, 1):
                for pattern, framework in api_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        results["api_endpoints"].append({
                            "file": relative_path,
                            "line": i,
                            "framework": framework,
                            "endpoint": line.strip()
                        })

            ai_service_patterns = [
                r"openai\.(ChatCompletion|Completion|Embedding)",
                r"anthropic\.(Client|messages)",
                r"cohere\.(Client|generate)",
                r"huggingface_hub\.(InferenceClient|HfApi)",
                r"requests\.(post|get).*api\.openai",
                r"requests\.(post|get).*api\.anthropic",
            ]

            for i, line in enumerate(lines, 1):
                for pattern in ai_service_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        results["external_services"].append({
                            "file": relative_path,
                            "line": i,
                            "service": "external_ai",
                            "content": line.strip()
                        })
                        break

        except Exception:
            pass

    def _scan_dependencies(self, file_path: Path, results: dict):
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            relative_path = str(file_path.relative_to(self.project_path))

            ai_packages = [
                "torch", "tensorflow", "keras", "scikit-learn", "sklearn",
                "transformers", "langchain", "llamaindex", "openai",
                "anthropic", "cohere", "huggingface-hub", "sentence-transformers",
                "chromadb", "pinecone-client", "weaviate-client",
                "whisper", "opencv-python", "mediapipe", "ultralytics",
                "xgboost", "lightgbm", "catboost",
            ]

            for line in content.splitlines():
                pkg = line.strip().split("=")[0].split(">")[0].split("<")[0].strip().lower()
                if pkg in [p.lower() for p in ai_packages]:
                    results["ai_dependencies"].append({
                        "file": relative_path,
                        "package": pkg,
                        "requires_documentation": True
                    })
        except Exception:
            pass

    def _analyze_api_findings(self, results: dict):
        if results["ai_dependencies"]:
            results["findings"].append(Finding(
                requirement_id="RA-003",
                status=ComplianceStatus.NON_COMPLIANT,
                evidence=f"Found {len(results['ai_dependencies'])} AI/ML dependencies. Technical documentation required.",
                risk_level="high",
                recommendation="Document all AI/ML dependencies, their versions, and intended use in your technical documentation."
            ))

        if results["external_services"]:
            results["findings"].append(Finding(
                requirement_id="RA-007",
                status=ComplianceStatus.PARTIALLY_COMPLIANT,
                evidence=f"Found {len(results['external_services'])} external AI service integrations.",
                risk_level="medium",
                recommendation="Document third-party AI services, implement error handling, and ensure data processing agreements are in place."
            ))

        if results["api_endpoints"]:
            results["findings"].append(Finding(
                requirement_id="RA-005",
                status=ComplianceStatus.PARTIALLY_COMPLIANT,
                evidence=f"Found {len(results['api_endpoints'])} API endpoints. Transparency documentation needed.",
                risk_level="medium",
                recommendation="Ensure API documentation includes AI system information, capabilities, and limitations for deployers."
            ))
