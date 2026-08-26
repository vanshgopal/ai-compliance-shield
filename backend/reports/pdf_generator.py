"""PDF Report Generator - Creates compliance reports in PDF format."""

from pathlib import Path
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from ..compliance.eu_ai_act import (
    ComplianceReport, Finding, ComplianceStatus, RiskCategory,
    EU_AI_ACT_REQUIREMENTS
)


class PDFReportGenerator:
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor('#1a1a2e'),
        ))
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.HexColor('#16213e'),
        ))
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=8,
            leading=14,
        ))
        self.styles.add(ParagraphStyle(
            name='StatusCompliant',
            parent=self.styles['Normal'],
            textColor=colors.HexColor('#27ae60'),
            fontSize=11,
            fontWeight='bold',
        ))
        self.styles.add(ParagraphStyle(
            name='StatusPartial',
            parent=self.styles['Normal'],
            textColor=colors.HexColor('#f39c12'),
            fontSize=11,
            fontWeight='bold',
        ))
        self.styles.add(ParagraphStyle(
            name='StatusNonCompliant',
            parent=self.styles['Normal'],
            textColor=colors.HexColor('#e74c3c'),
            fontSize=11,
            fontWeight='bold',
        ))

    def generate(self, report: ComplianceReport) -> str:
        filename = f"compliance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = self.output_dir / filename

        doc = SimpleDocTemplate(
            str(filepath),
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72,
        )

        elements = []
        elements.extend(self._build_cover_page(report))
        elements.append(PageBreak())
        elements.extend(self._build_executive_summary(report))
        elements.append(PageBreak())
        elements.extend(self._build_detailed_findings(report))
        elements.append(PageBreak())
        elements.extend(self._build_remediation_plan(report))
        elements.append(PageBreak())
        elements.extend(self._build_requirements_matrix(report))

        doc.build(elements)
        return str(filepath)

    def _build_cover_page(self, report: ComplianceReport) -> list:
        elements = []
        elements.append(Spacer(1, 2 * inch))
        elements.append(Paragraph("EU AI Act", self.styles['CustomTitle']))
        elements.append(Paragraph("Compliance Report", self.styles['CustomTitle']))
        elements.append(Spacer(1, 0.5 * inch))
        elements.append(HRFlowable(width="80%", thickness=2, color=colors.HexColor('#3498db')))
        elements.append(Spacer(1, 0.5 * inch))
        elements.append(Paragraph(f"<b>Company:</b> {report.company_name}", self.styles['CustomBody']))
        elements.append(Paragraph(f"<b>Scan Date:</b> {report.scan_date}", self.styles['CustomBody']))
        elements.append(Paragraph(f"<b>Overall Score:</b> {report.overall_score}%", self.styles['CustomBody']))
        elements.append(Paragraph(f"<b>Risk Category:</b> {report.risk_category.value.upper()}", self.styles['CustomBody']))
        elements.append(Spacer(1, 1 * inch))
        elements.append(Paragraph(
            "This report provides an assessment of your organization's compliance "
            "with the European Union Artificial Intelligence Act (Regulation 2024/1689).",
            self.styles['CustomBody']
        ))
        elements.append(Spacer(1, 0.5 * inch))
        elements.append(Paragraph(
            "<b>CONFIDENTIAL</b> - This document contains proprietary compliance assessment data.",
            self.styles['CustomBody']
        ))
        return elements

    def _build_executive_summary(self, report: ComplianceReport) -> list:
        elements = []
        elements.append(Paragraph("Executive Summary", self.styles['CustomHeading']))
        elements.append(Spacer(1, 0.2 * inch))

        score_color = self._get_score_color(report.overall_score)
        elements.append(Paragraph(
            f"<b>Overall Compliance Score: <font color='{score_color}'>{report.overall_score}%</font></b>",
            self.styles['CustomBody']
        ))
        elements.append(Spacer(1, 0.2 * inch))

        elements.append(Paragraph("<b>Key Findings:</b>", self.styles['CustomBody']))
        compliant = sum(1 for f in report.findings if f.status == ComplianceStatus.COMPLIANT)
        partial = sum(1 for f in report.findings if f.status == ComplianceStatus.PARTIALLY_COMPLIANT)
        non_compliant = sum(1 for f in report.findings if f.status == ComplianceStatus.NON_COMPLIANT)

        summary_data = [
            ['Status', 'Count', 'Percentage'],
            ['Compliant', str(compliant), f"{compliant/len(report.findings)*100:.1f}%"],
            ['Partially Compliant', str(partial), f"{partial/len(report.findings)*100:.1f}%"],
            ['Non-Compliant', str(non_compliant), f"{non_compliant/len(report.findings)*100:.1f}%"],
            ['Total', str(len(report.findings)), '100%'],
        ]

        summary_table = Table(summary_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#27ae60')),
            ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#f39c12')),
            ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#e74c3c')),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 0.3 * inch))

        elements.append(Paragraph("<b>Risk Assessment:</b>", self.styles['CustomBody']))
        elements.append(Paragraph(
            f"The AI systems detected in your codebase are classified as <b>{report.risk_category.value}</b> risk "
            f"under the EU AI Act. This classification determines the applicable compliance requirements "
            f"and potential penalties for non-compliance.",
            self.styles['CustomBody']
        ))

        return elements

    def _build_detailed_findings(self, report: ComplianceReport) -> list:
        elements = []
        elements.append(Paragraph("Detailed Findings", self.styles['CustomHeading']))
        elements.append(Spacer(1, 0.2 * inch))

        for i, finding in enumerate(report.findings, 1):
            status_style = self._get_status_style(finding.status)
            elements.append(Paragraph(f"<b>Finding {i}: {finding.requirement_id}</b>", self.styles['CustomBody']))
            elements.append(Paragraph(f"Status: {finding.status.value.upper()}", status_style))
            elements.append(Paragraph(f"<b>Evidence:</b> {finding.evidence}", self.styles['CustomBody']))
            elements.append(Paragraph(f"<b>Risk Level:</b> {finding.risk_level}", self.styles['CustomBody']))
            elements.append(Paragraph(f"<b>Recommendation:</b> {finding.recommendation}", self.styles['CustomBody']))
            if finding.file_path:
                elements.append(Paragraph(f"<b>Location:</b> {finding.file_path}:{finding.line_number}", self.styles['CustomBody']))
            elements.append(Spacer(1, 0.2 * inch))
            elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#bdc3c7')))
            elements.append(Spacer(1, 0.1 * inch))

        return elements

    def _build_remediation_plan(self, report: ComplianceReport) -> list:
        elements = []
        elements.append(Paragraph("Remediation Plan", self.styles['CustomHeading']))
        elements.append(Spacer(1, 0.2 * inch))

        if not report.remediation_plan:
            elements.append(Paragraph("No remediation actions required. Your organization is fully compliant.", self.styles['CustomBody']))
            return elements

        plan_data = [['Step', 'Requirement', 'Priority', 'Deadline', 'Effort']]
        for item in report.remediation_plan:
            plan_data.append([
                str(item['step']),
                item['title'][:30] + "..." if len(item['title']) > 30 else item['title'],
                item['priority'],
                item['deadline'],
                item['estimated_effort'],
            ])

        plan_table = Table(plan_data, colWidths=[0.5*inch, 2.5*inch, 0.8*inch, 1.2*inch, 1*inch])
        plan_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')]),
        ]))
        elements.append(plan_table)
        elements.append(Spacer(1, 0.3 * inch))

        elements.append(Paragraph("<b>Estimated Timeline:</b>", self.styles['CustomBody']))
        high_priority = sum(1 for item in report.remediation_plan if item['priority'] == 'HIGH')
        med_priority = sum(1 for item in report.remediation_plan if item['priority'] == 'MEDIUM')
        elements.append(Paragraph(
            f"• High Priority Items: {high_priority} (Est. 2-4 weeks each)<br/>"
            f"• Medium Priority Items: {med_priority} (Est. 1-2 weeks each)<br/>"
            f"<b>Total Estimated Compliance Timeline: {2 + high_priority * 2}-{4 + med_priority * 2} weeks</b>",
            self.styles['CustomBody']
        ))

        return elements

    def _build_requirements_matrix(self, report: ComplianceReport) -> list:
        elements = []
        elements.append(Paragraph("EU AI Act Requirements Matrix", self.styles['CustomHeading']))
        elements.append(Spacer(1, 0.2 * inch))

        matrix_data = [['ID', 'Requirement', 'Article', 'Risk Level', 'Status']]
        for req in EU_AI_ACT_REQUIREMENTS:
            finding = next((f for f in report.findings if f.requirement_id == req.id), None)
            status = finding.status.value if finding else 'N/A'
            matrix_data.append([
                req.id,
                req.title[:25] + "..." if len(req.title) > 25 else req.title,
                req.article,
                req.risk_category.value,
                status,
            ])

        matrix_table = Table(matrix_data, colWidths=[0.6*inch, 2*inch, 0.8*inch, 1*inch, 1.2*inch])
        matrix_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')]),
        ]))
        elements.append(matrix_table)

        return elements

    def _get_score_color(self, score: float) -> str:
        if score >= 80:
            return '#27ae60'
        elif score >= 60:
            return '#f39c12'
        return '#e74c3c'

    def _get_status_style(self, status: ComplianceStatus):
        if status == ComplianceStatus.COMPLIANT:
            return self.styles['StatusCompliant']
        elif status == ComplianceStatus.PARTIALLY_COMPLIANT:
            return self.styles['StatusPartial']
        return self.styles['StatusNonCompliant']
