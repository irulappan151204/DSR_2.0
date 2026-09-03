# wsgi.py
# Production WSGI entry point for Gunicorn, Waitress, or uWSGI

import os
import sys

# Ensure application root directory is on Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app as application

if __name__ == "__main__":
    application.run()
