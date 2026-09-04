"""Legacy wrapper for statistics routes to preserve 100% backward compatibility.
All logic has been modularized into:
  - repositories/statistics_repository.py
  - services/statistics/
  - services/statistics_service.py
  - routes/statistics_routes.py
"""

from routes.statistics_routes import statistics_bp, view_statistics
from services.statistics_service import get_statistics_context

__all__ = [
    'statistics_bp',
    'view_statistics',
    'get_statistics_context'
]