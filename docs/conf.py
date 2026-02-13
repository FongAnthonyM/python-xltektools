#!/usr/bin/env python
"""Sphinx configuration for xltektools.

This configuration enables extensive API documentation using autodoc and autosummary, better type and Google/NumPy style
docstring parsing via Napoleon, and several convenience extensions like viewcode, intersphinx, and todo.
"""

# Imports #
# Standard Libraries #
import sys
from datetime import datetime, timezone
from pathlib import Path

# Ensure src is on sys.path for autodoc
ROOT = Path(__file__).parent.parent.resolve()
SRC = ROOT / "src"
if SRC.is_dir() and str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

# Project Information #
project = "xltektools"
author = "Anthony Fong"
copyright = f"{datetime.now(tz=timezone.utc).year}, {author}"

# General configuration #
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx_click",
    "myst_parser",
]

exclude_patterns = ["python-styleguide", "_build"]

# Autodoc / Autosummary
autodoc_typehints = "description"
autosummary_generate = True
add_module_names = False
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_attr_annotations = True

# Intersphinx
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# HTML output
html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "collapse_navigation": False,
    "navigation_depth": 4,
}

todo_include_todos = True
