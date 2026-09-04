"""
Legacy wrapper for report routes.
Delegates to routes.reports and services.report_service.
"""
from routes.reports import report_bp, generate_report
from services.report_service import generate_pdf_report

__all__ = ['report_bp', 'generate_report', 'generate_pdf_report']