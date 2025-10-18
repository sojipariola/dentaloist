# tests/test_mapper_conflicts.py
from sqlalchemy.orm import class_mapper, configure_mappers
from sqlalchemy.exc import InvalidRequestError
import pytest
import importlib
import sys

def test_duplicate_mappers():
    """
    Detects if a model (e.g., WidgetConfig or User)
    has been registered twice in the SQLAlchemy mapper registry.
    """

    # Import app and models once
    from app import create_app
    from app.models import User, WidgetConfig
    from app.models import db

    app = create_app("testing")

    # Force SQLAlchemy to configure all mappers
    try:
        configure_mappers()
    except InvalidRequestError as e:
        pytest.fail(f"SQLAlchemy mapper conflict: {e}")

    # Inspect mappers to see if same table mapped twice
    all_mappers = list(db.Model.registry.mappers)
    mapper_names = [m.class_.__name__ for m in all_mappers]

    print("\nRegistered mappers:", mapper_names)

    duplicates = {name for name in mapper_names if mapper_names.count(name) > 1}

    assert not duplicates, f"Duplicate model mapping detected: {duplicates}"

def test_import_paths_consistency():
    """
    Checks that model imports resolve to the same module reference.
    """
    from app.models import WidgetConfig

    alt_import = importlib.import_module("app.models.analytics").WidgetConfig

    assert WidgetConfig is alt_import, (
        f"WidgetConfig imported twice: {WidgetConfig.__module__} vs {alt_import.__module__}"
    )

# pytest -q tests/test_mapper_conflicts.py -s
