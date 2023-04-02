# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


import sphinx_rtd_theme
import os, sys
from recommonmark.transform import AutoStructify

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'terminal-tracker'
copyright = '2023, Miloni Atal'
author = 'Miloni Atal'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

master_doc = "index"
extensions = [
    "recommonmark", 
    "sphinx.ext.napoleon", 
    "sphinx.ext.coverage", 
    "sphinx.ext.viewcode", 
    "sphinx.ext.napoleon", 
    "sphinx.ext.autosummary",
    "sphinx.ext.autodoc",
    "sphinx.ext.todo"
    ]
todo_include_todos = True
autodoc_mock_imports = ["pandas", "pytz"]
source_suffix = [".rst", ".md"]
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

sys.path.append(os.path.join(os.path.dirname(__name__), '..'))


def setup(app):
    app.add_config_value('recommonmark_config', {
        'auto_toc_tree_section': 'Contents',
    }, True)
    app.add_transform(AutoStructify)