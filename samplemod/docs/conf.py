# -*- coding: utf-8 -*-
#
# Sphinx documentation build configuration file
#

# -- Project information -----------------------------------------------------
project = 'sample'
copyright = '2012, Kenneth Reitz'
author = 'Kenneth Reitz'
release = 'v0.0.1'
version = 'v0.0.1'

# -- General configuration ---------------------------------------------------
extensions = []
templates_path = ['_templates']
exclude_patterns = ['_build']

# -- Options for HTML output -------------------------------------------------
html_theme = 'default'
html_static_path = ['_static']

# HTML help builder
htmlhelp_basename = 'sampledoc'

# LaTeX documents
latex_documents = [
    ('index', 'sample.tex', 'sample Documentation', 'Kenneth Reitz', 'manual'),
]

# Manual pages
man_pages = [
    ('index', 'sample', 'sample Documentation', ['Kenneth Reitz'], 1)
]

# Texinfo documents
texinfo_documents = [
    (
        'index',
        'sample',
        'sample Documentation',
        'Kenneth Reitz',
        'sample',
        'One line description of project.',
        'Miscellaneous',
    ),
]
