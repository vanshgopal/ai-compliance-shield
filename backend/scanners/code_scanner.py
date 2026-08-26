"""Code Scanner - Analyzes source code for AI/ML usage and compliance gaps."""

import os
import re
from pathlib import Path
from typing import Optional
from ..compliance.eu_ai_act import (
    AI_KEYWORDS, ComplianceStatus, Finding, RiskCategory,
    classify_risk_level, get_requirements_for_risk
)


class CodeScanner:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.supported_extensions = {
            ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".go",
            ".rs", ".cpp", ".c", ".cs", ".rb", ".php", ".r", ".scala"
        }
        self.scan_results = {
            "ai_files": [],
            "model_usage": [],
            "training_code": [],
            "inference_code": [],
            "data_processing": [],
            "api_calls": [],
            "findings": [],
        }

    def scan(self) -> dict:
        for root, dirs, files in os.walk(self.project_path):
            dirs[:] = [d for d in dirs if d not in {".git", "node_modules", "__pycache__", ".venv", "venv"}]
            for file in files:
                if Path(file).suffix in self.supported_extensions:
                    file_path = Path(root) / file
                    self._scan_file(file_path)
        self._analyze_findings()
        return self.scan_results

    def _scan_file(self, file_path: Path):
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            lines = content.splitlines()
            relative_path = str(file_path.relative_to(self.project_path))
            if self._contains_ai_keywords(content):
                self.scan_results["ai_files"].append(relative_path)
            for i, line in enumerate(lines, 1):
                self._check_line(line, relative_path, i, content)
        except Exception as e:
            pass

    def _contains_ai_keywords(self, content: str) -> bool:
        content_lower = content.lower()
        return any(kw in content_lower for kw in AI_KEYWORDS[:20])

    def _check_line(self, line: str, file_path: str, line_num: int, full_content: str):
        line_lower = line.lower().strip()
        if line_lower.startswith("#") or line_lower.startswith("//"):
            return
        self._check_model_imports(line, line_lower, file_path, line_num)
        self._check_training_code(line, line_lower, file_path, line_num)
        self._check_api_calls(line, line_lower, file_path, line_num)
        self._check_data_processing(line, line_lower, file_path, line_num)
        self._check_model_loading(line, line_lower, file_path, line_num)

    def _check_model_imports(self, line: str, line_lower: str, file_path: str, line_num: int):
        ml_imports = [
            "import torch", "import tensorflow", "from keras", "from sklearn",
            "import transformers", "from langchain", "import openai",
            "import anthropic", "from sentence_transformers", "import whisper",
            "import cv2", "import mediapipe", "from ultralytics",
        ]
        for imp in ml_imports:
            if imp in line_lower:
                self.scan_results["model_usage"].append({
                    "file": file_path, "line": line_num,
                    "type": "import", "content": line.strip()
                })
                break

    def _check_training_code(self, line: str, line_lower: str, file_path: str, line_num: int):
        training_patterns = [
            r"\.fit\(", r"\.train\(", r"train_on_batch",
            r"gradient", r"backprop", r"optimizer\.step",
            r"loss\.backward", r"model\.save", r"torch\.save",
            r"joblib\.dump", r"pickle\.dump", r"\.save_pretrained",
        ]
        for pattern in training_patterns:
            if re.search(pattern, line_lower):
                self.scan_results["training_code"].append({
                    "file": file_path, "line": line_num,
                    "content": line.strip()
                })
                break

    def _check_api_calls(self, line: str, line_lower: str, file_path: str, line_num: int):
        api_patterns = [
            r"openai\.", r"anthropic\.", r"cohere\.",
            r"requests\.post.*api", r"requests\.get.*model",
            r"/predict", r"/v1/chat", r"/v1/completions",
            r"ollama\.generate", r"ollama\.chat",
        ]
        for pattern in api_patterns:
            if re.search(pattern, line_lower):
                self.scan_results["api_calls"].append({
                    "file": file_path, "line": line_num,
                    "content": line.strip()
                })
                break

    def _check_data_processing(self, line: str, line_lower: str, file_path: str, line_num: int):
        data_patterns = [
            r"train_test_split", r"validation_split",
            r"preprocess", r"normalize", r"standardize",
            r"augment", r"label_encode", r"one_hot",
            r"data_loader", r"dataset", r"dataframe.*ai",
        ]
        for pattern in data_patterns:
            if re.search(pattern, line_lower):
                self.scan_results["data_processing"].append({
                    "file": file_path, "line": line_num,
                    "content": line.strip()
                })
                break

    def _check_model_loading(self, line: str, line_lower: str, file_path: str, line_num: int):
        load_patterns = [
            r"load_model", r"load_state_dict", r"from_pretrained",
            r"pickle\.load", r"joblib\.load", r"torch\.load",
            r"tf\.saved_model\.load", r"onnxruntime",
        ]
        for pattern in load_patterns:
            if re.search(pattern, line_lower):
                self.scan_results["model_usage"].append({
                    "file": file_path, "line": line_num,
                    "type": "loading", "content": line.strip()
                })
                break

    def _analyze_findings(self):
        has_ai = bool(self.scan_results["ai_files"])
        has_training = bool(self.scan_results["training_code"])
        has_inference = bool(self.scan_results["model_usage"])
        has_api = bool(self.scan_results["api_calls"])

        if not has_ai:
            self.scan_results["findings"].append(Finding(
                requirement_id="RA-005",
                status=ComplianceStatus.NOT_APPLICABLE,
                evidence="No AI/ML code detected in the scanned project.",
                risk_level="none",
                recommendation="No AI-specific compliance actions required."
            ))
            return

        if has_ai and not has_training and not has_api:
            self.scan_results["findings"].append(Finding(
                requirement_id="RA-005",
                status=ComplianceStatus.PARTIALLY_COMPLIANT,
                evidence="AI-related code detected but limited to utility functions.",
                risk_level="low",
                recommendation="Ensure AI system transparency requirements are met if deploying AI features."
            ))

        if has_training:
            self.scan_results["findings"].append(Finding(
                requirement_id="RA-002",
                status=ComplianceStatus.NON_COMPLIANT,
                evidence="Training code detected. Data governance requirements apply.",
                risk_level="high",
                recommendation="Implement data governance for training datasets. Document data sources, quality criteria, and bias mitigation."
            ))
            self.scan_results["findings"].append(Finding(
                requirement_id="RA-004",
                status=ComplianceStatus.NON_COMPLIANT,
                evidence="Training operations detected. Logging capabilities required.",
                risk_level="medium",
                recommendation="Implement automatic logging for all training runs, including parameters, metrics, and data versions."
            ))

        if has_inference or has_api:
            self.scan_results["findings"].append(Finding(
                requirement_id="RA-006",
                status=ComplianceStatus.PARTIALLY_COMPLIANT,
                evidence="AI inference/API calls detected. Human oversight mechanisms needed.",
                risk_level="high",
                recommendation="Implement human oversight mechanisms for AI decisions. Add approval workflows for high-risk decisions."
            ))
            self.scan_results["findings"].append(Finding(
                requirement_id="RA-005",
                status=ComplianceStatus.PARTIALLY_COMPLIANT,
                evidence="AI system detected. Transparency documentation required.",
                risk_level="medium",
                recommendation="Create documentation describing AI system capabilities, limitations, and intended use."
            ))

        if has_api:
            self.scan_results["findings"].append(Finding(
                requirement_id="RA-007",
                status=ComplianceStatus.PARTIALLY_COMPLIANT,
                evidence="External AI API calls detected. Robustness and security assessment needed.",
                risk_level="medium",
                recommendation="Implement API error handling, rate limiting, and input validation. Document third-party AI service dependencies."
            ))
