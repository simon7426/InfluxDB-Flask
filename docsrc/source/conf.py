# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from pallets_sphinx_themes import ProjectLink
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# sys.path.append(os.path.abspath('_themes'))


# -- Project information -----------------------------------------------------

project = u'InfluxDB-Flask'
copyright = '2022, Simon Islam'
author = 'Simon Islam'

# The full version, including alpha/beta/rc tags
release = '0.1.2'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "pallets_sphinx_themes",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

source_suffix = '.rst'

master_doc = 'index'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

html_theme = "flask"
html_theme_options = {"index_sidebar_logo": False}
html_context = {
    "project_links": [
        ProjectLink("PyPI Releases", "https://pypi.org/project/influxdb-flask/"),
        ProjectLink("Source Code", "https://github.com/simon7426/InfluxDB-Flask"),
        ProjectLink("Issue Tracker", "https://github.com/simon7426/InfluxDB-Flask/issues/")
    ]
}
html_sidebars = {
    "index": [
        "project.html",
        "localtoc.html",
        "searchbox.html",
        "ethicalads.html",
    ],
    '**': [
        "localtoc.html",
        "relations.html",
        "searchbox.html",
        "ethicalads.html",
    ]
}
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
