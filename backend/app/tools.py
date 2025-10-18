#!/usr/bin/env python3
import click
import os
import shutil
import subprocess


@click.group()
def cli():
    """Utility commands outside Flask app (safe from app init)."""
    pass


@cli.command("clean-cache")
def clean_cache():
    """Delete Python cache files (__pycache__, .pyc, .pyo)."""
    click.echo("🧹 Cleaning Python cache files...")
    subprocess.run(
        'find . -type d -name "__pycache__" -exec rm -rf {} + '
        '-o -type f -name "*.pyc" -delete '
        '-o -type f -name "*.pyo" -delete',
        shell=True,
        check=False
    )
    click.echo("✅ Cache cleaned.")


@cli.command("delete-instance-migrations")
def delete_instance_migrations():
    """Delete instance/ and migrations/ folders."""
    for folder in ["instance", "migrations"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            click.echo(f"🗑️  Deleted {folder}/")
        else:
            click.echo(f"⚠️  {folder}/ not found, skipping...")
    click.echo("✅ instance/ and migrations/ deleted.")


@cli.command("reinit-migrations")
def reinit_migrations():
    """Delete migrations and reinitialize Alembic."""
    if os.path.exists("migrations"):
        shutil.rmtree("migrations")
        click.echo("🗑️  Deleted migrations/")

    click.echo("⚡ Reinitializing Alembic...")
    subprocess.run("flask db init", shell=True, check=False)
    subprocess.run("flask db migrate -m 'Initial migration'", shell=True, check=False)
    subprocess.run("flask db upgrade", shell=True, check=False)

    click.echo("✅ Migrations reinitialized.")


if __name__ == "__main__":
    cli()
