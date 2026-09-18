import click
from flask.cli import with_appcontext
from extensions import db, bcrypt
from models import User

@click.command('create-admin')
@with_appcontext
def create_admin_command():
    """Create an admin user."""
    username = click.prompt('Enter admin username')
    password = click.prompt('Enter admin password', hide_input=True, confirmation_prompt=True)
    
    if User.query.filter_by(username=username).first():
        click.echo('Username already exists.')
        return
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    admin = User(username=username, password=hashed_password, role='Admin')
    db.session.add(admin)
    db.session.commit()
    click.echo('Admin user created successfully.')


@click.command('sync-tables')
@click.option('--dry-run', is_flag=True, help='Preview missing tables without creating them.')
@with_appcontext
def sync_tables_command(dry_run):
    """Synchronise MySQL tables with SQLAlchemy models.

    Compares every model defined in the codebase against the live
    database and creates any missing tables.  Existing tables and
    data are never modified or dropped.
    """
    from sync_tables import sync_tables
    result = sync_tables(dry_run=dry_run)
    if result.get('still_missing'):
        raise SystemExit(1)