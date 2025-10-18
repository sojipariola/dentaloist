#!/usr/bin/env python3
import subprocess
import click
import sys

@click.command()
def clean_cache():
    """Delete Python cache files without loading Flask app."""
    click.echo("🧹 Cleaning Python cache files...")
    try:
        subprocess.run(
            'find . -type d -name "__pycache__" -exec rm -rf {} + -o -type f -name "*.pyc" -delete -o -type f -name "*.pyo" -delete',
            shell=True,
            check=True
        )
        click.echo("✅ Cache cleaned successfully!")
    except Exception as e:
        click.echo(f"❌ Error while cleaning cache: {e}")
        sys.exit(1)

if __name__ == "__main__":
    clean_cache()

# python3 scripts/clean_cache.py

