#!/usr/bin/env python3
"""
sync_tables.py — Production-Safe Database Table Synchronisation
================================================================
Compares every SQLAlchemy model in the codebase against the live MySQL
database and creates any tables that are missing.

Safety guarantees
-----------------
* Uses ``CREATE TABLE IF NOT EXISTS`` via ``db.create_all()`` — MySQL
  silently skips tables that already exist.
* **Never** issues DROP, ALTER, or TRUNCATE.
* Existing data is completely untouched.

Usage
-----
    # Preview only — no changes made
    python sync_tables.py --dry-run

    # Create missing tables
    python sync_tables.py

    # Also available as a Flask CLI command (after registering in commands.py)
    flask sync-tables
    flask sync-tables --dry-run
"""

import sys
import os
import argparse
from datetime import datetime

# ---------------------------------------------------------------------------
# Ensure the project root is on sys.path so that local imports work when the
# script is executed directly (``python sync_tables.py``).
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from extensions import db
from sqlalchemy import inspect

# Importing models is mandatory so that SQLAlchemy registers every table in
# ``db.metadata``.  The models/__init__.py barrel-export takes care of that.
import models  # noqa: F401


# ── Colour helpers (safe for terminals that don't support ANSI) ───────────
def _green(text):
    return f"\033[92m{text}\033[0m"

def _red(text):
    return f"\033[91m{text}\033[0m"

def _yellow(text):
    return f"\033[93m{text}\033[0m"

def _cyan(text):
    return f"\033[96m{text}\033[0m"

def _bold(text):
    return f"\033[1m{text}\033[0m"


def sync_tables(dry_run: bool = False, verbose: bool = True):
    """
    Core sync logic.  Returns a dict with summary info so the Flask CLI
    command can re-use it.

    Parameters
    ----------
    dry_run : bool
        When True the script only reports what *would* happen; no DDL is
        executed.
    verbose : bool
        Print detailed output to stdout.
    """
    with app.app_context():
        inspector = inspect(db.engine)

        # Tables that exist in the live database right now
        existing_tables = set(inspector.get_table_names())

        # Tables defined in SQLAlchemy model metadata
        defined_tables = set(db.metadata.tables.keys())

        missing_tables = sorted(defined_tables - existing_tables)
        present_tables = sorted(defined_tables & existing_tables)
        extra_tables   = sorted(existing_tables - defined_tables)

        # ── Report ────────────────────────────────────────────────────────
        if verbose:
            print()
            print(_bold("=" * 65))
            print(_bold("  QMIS DSR — Database Table Sync Report"))
            print(_bold(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"))
            print(_bold("=" * 65))
            print()
            print(f"  Database URI : {_cyan(str(db.engine.url))}")
            print(f"  Tables in code (models)  : {_bold(str(len(defined_tables)))}")
            print(f"  Tables in database       : {_bold(str(len(existing_tables)))}")
            print(f"  Already present          : {_green(str(len(present_tables)))}")
            print(f"  Missing (to create)      : {_red(str(len(missing_tables)))}")
            print(f"  Extra (in DB only)       : {_yellow(str(len(extra_tables)))}")
            print()

            if present_tables:
                print(_green("  [OK] Already present tables:"))
                for i, t in enumerate(present_tables, 1):
                    print(f"    {i:3d}. {t}")
                print()

            if missing_tables:
                print(_red("  [MISSING] Missing tables (will be created):"))
                for i, t in enumerate(missing_tables, 1):
                    print(f"    {i:3d}. {t}")
                print()

            if extra_tables:
                print(_yellow("  [INFO] Extra tables (in DB but not in code -- left untouched):"))
                for i, t in enumerate(extra_tables, 1):
                    print(f"    {i:3d}. {t}")
                print()

        # ── Action ────────────────────────────────────────────────────────
        if not missing_tables:
            if verbose:
                print(_green("  [OK] All tables are in sync. Nothing to do."))
                print()
            return {
                "status": "in_sync",
                "created": [],
                "already_present": present_tables,
                "extra": extra_tables,
            }

        if dry_run:
            if verbose:
                print(_yellow("  [DRY RUN] No changes have been made."))
                print(f"    Run without --dry-run to create the {len(missing_tables)} missing table(s).")
                print()
            return {
                "status": "dry_run",
                "would_create": missing_tables,
                "already_present": present_tables,
                "extra": extra_tables,
            }

        # Create missing tables (existing ones are silently skipped)
        if verbose:
            print("  Creating missing tables …")

        db.create_all()

        # Verify
        inspector = inspect(db.engine)
        new_existing = set(inspector.get_table_names())
        created = sorted(set(missing_tables) & new_existing)
        still_missing = sorted(set(missing_tables) - new_existing)

        if verbose:
            print()
            if created:
                print(_green(f"  [CREATED] Successfully created {len(created)} table(s):"))
                for i, t in enumerate(created, 1):
                    print(f"    {i:3d}. {t}")
                print()

            if still_missing:
                print(_red(f"  [FAIL] {len(still_missing)} table(s) could NOT be created:"))
                for i, t in enumerate(still_missing, 1):
                    print(f"    {i:3d}. {t}")
                print("    Check the SQLAlchemy model definitions for errors.")
                print()

            total_now = len(inspector.get_table_names())
            print(_bold(f"  Database now has {total_now} tables."))
            print(_green("  [DONE] Sync complete."))
            print()

        return {
            "status": "completed",
            "created": created,
            "still_missing": still_missing,
            "already_present": present_tables,
            "extra": extra_tables,
        }


# ── CLI entry-point ──────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Synchronise MySQL tables with SQLAlchemy models."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only report what would happen; do not create tables.",
    )
    args = parser.parse_args()

    result = sync_tables(dry_run=args.dry_run)

    # Exit with non-zero if tables could not be created
    if result.get("still_missing"):
        sys.exit(1)
