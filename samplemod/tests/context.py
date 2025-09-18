# -*- coding: utf-8 -*-
"""
Context setup for tests.
Ensures the `sample` module is importable during testing.
"""

import os
import sys

# Add the parent directory to sys.path so imports work
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)

# Import the package to confirm availability
import sample  # noqa: F401
