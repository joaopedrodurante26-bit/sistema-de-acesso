import click
from flask.cli import with_appcontext

from .extensions import db
from .models import User, UserRole


@click.command("seed-admin")
@click.option("--username", default=None, help="Admin username")
@click.option("--password", default=None, help="Admin password")
@with_appcontext
def seed_admin(username, password):
    from flask import current_app

    admin_username = username or current_app.config.get("ADMIN_USERNAME") or "admin"
    admin_password = password or current_app.config.get("ADMIN_PASSWORD") or "Admin@123456"

    existing = User.query.filter_by(username=admin_username).first()
    if existing:
        existing.role = UserRole.ADMIN.value
        existing.is_active = True
        existing.set_password(admin_password)
        db.session.commit()
        click.echo(f"Updated admin user '{admin_username}'.")
        return

    user = User(username=admin_username, role=UserRole.ADMIN.value, is_active=True)
    user.set_password(admin_password)
    db.session.add(user)
    db.session.commit()
    click.echo(f"Created admin user '{admin_username}'.")


def register_cli_commands(app):
    app.config.setdefault("ADMIN_USERNAME", "admin")
    app.config.setdefault("ADMIN_PASSWORD", "Admin@123456")
    app.cli.add_command(seed_admin)
