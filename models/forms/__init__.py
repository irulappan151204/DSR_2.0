# models/forms/__init__.py
import inspect
from .base import BaseForm
from . import team1, team2, team3

# Collect all model classes defined in submodules
for mod in (team1, team2, team3):
    for name, cls in inspect.getmembers(mod, inspect.isclass):
        if cls.__module__ == mod.__name__:
            globals()[name] = cls
