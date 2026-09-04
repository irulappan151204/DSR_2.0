"""
Alias module for report routes, pointing to routes.reports.
"""
from routes.reports import report_bp, generate_report

__all__ = ['report_bp', 'generate_report']
