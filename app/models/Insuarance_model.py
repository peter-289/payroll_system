"""Compatibility shim for misspelled insurance model module.

Exports `Insurance` from the canonical `insurance_model` to keep
imports like `app.models.Insuarance_model` working.
"""
from .insurance_model import Insurance  # noqa: F401

__all__ = ["Insurance"]
