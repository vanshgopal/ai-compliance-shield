"""Config Scanner - Analyzes configuration files for AI/ML settings and compliance."""

import os
import json
import yaml
from pathlib import Path
from typing import Optional
from ..compliance.eu_ai_act import ComplianceStatus, Finding


class ConfigScanner:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.config_files = {
            "yaml": [".yaml", ".yml"],
            "json": [".json"],
            "toml": [".toml"],
            "ini": [".ini", ".cfg"],
            "env": [".env", ".env.example"],
        }
        self.findings = []

    def scan(self) -> dict:
        results = {
            "config_files": [],
            "ai_configs": [],
            "env_files": [],
            "model_configs": [],
            "security_issues": [],
            "findings": [],
        }

        for root, dirs, files in os.walk(self.project_path):
            dirs[:] = [d for d in dirs if d not in {".git", "node_modules", "__pycache__", ".venv"}]
            for file in files:
                file_path = Path(root) / file
                suffix = file_path.suffix.lower()
                if suffix in [".yaml", ".yml"]:
                    self._scan_yaml(file_path, results)
                elif suffix == ".json":
                    self._scan_json(file_path, results)
                elif suffix in [".env", ".env.example"]:
                    self._scan_env(file_path, results)
                elif suffix in [".toml", ".ini", ".cfg"]:
                    self._scan_toml(file_path, results)

        self._analyze_config_findings(results)
        return results

    def _scan_yaml(self, file_path: Path, results: dict):
        try:
            relative_path = str(file_path.relative_to(self.project_path))
            results["config_files"].append(relative_path)
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            if any(kw in content.lower() for kw in ["model", "training", "inference", "ai"]):
                results["ai_configs"].append(relative_path)
                results["model_configs"].append({
                    "file": relative_path,
                    "type": "yaml",
                    "has_model_config": True
                })
        except Exception:
            pass

    def _scan_json(self, file_path: Path, results: dict):
        try:
            relative_path = str(file_path.relative_to(self.project_path))
            results["config_files"].append(relative_path)
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            if any(kw in content.lower() for kw in ["model", "training", "inference", "pipeline"]):
                results["ai_configs"].append(relative_path)
                results["model_configs"].append({
                    "file": relative_path,
                    "type": "json",
                    "has_model_config": True
                })
        except Exception:
            pass

    def _scan_env(self, file_path: Path, results: dict):
        relative_path = str(file_path.relative_to(self.project_path))
        results["env_files"].append(relative_path)
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            ai_env_vars = [
                "OPENAI", "ANTHROPIC", "COHERE", "HUGGING", "MODEL",
                "TRAINING", "INFERENCE", "API_KEY", "SECRET",
            ]
            for line in content.splitlines():
                if line.strip() and not line.startswith("#"):
                    key = line.split("=")[0].strip().upper() if "=" in line else ""
                    if any(env_kw in key for env_kw in ai_env_vars):
                        results["security_issues"].append({
                            "file": relative_path,
                            "issue": "AI-related credential found in env file",
                            "severity": "high" if "SECRET" in key or "API_KEY" in key else "medium",
                            "recommendation": "Ensure .env files are in .gitignore and never committed to version control."
                        })
        except Exception:
            pass

    def _scan_toml(self, file_path: Path, results: dict):
        try:
            relative_path = str(file_path.relative_to(self.project_path))
            results["config_files"].append(relative_path)
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            if any(kw in content.lower() for kw in ["model", "training", "ai"]):
                results["ai_configs"].append(relative_path)
        except Exception:
            pass

    def _analyze_config_findings(self, results: dict):
        if results["ai_configs"]:
            results["findings"].append(Finding(
                requirement_id="RA-003",
                status=ComplianceStatus.PARTIALLY_COMPLIANT,
                evidence=f"Found {len(results['ai_configs'])} AI-related configuration files.",
                risk_level="medium",
                recommendation="Ensure technical documentation covers all AI configuration files, including model parameters and training settings."
            ))

        if results["security_issues"]:
            results["findings"].append(Finding(
                requirement_id="RA-007",
                status=ComplianceStatus.NON_COMPLIANT,
                evidence=f"Found {len(results['security_issues'])} security issues in configuration files.",
                risk_level="high",
                recommendation="Address security issues: ensure credentials are not committed to version control, implement secret management."
            ))

        if results["env_files"]:
            env_in_git = any(".gitignore" not in str(f) for f in results["env_files"])
            if env_in_git:
                results["findings"].append(Finding(
                    requirement_id="RA-007",
                    status=ComplianceStatus.PARTIALLY_COMPLIANT,
                    evidence="Environment files detected. Verify they are excluded from version control.",
                    risk_level="medium",
                    recommendation="Add .env files to .gitignore and use secret management solutions for production deployments."
                ))
