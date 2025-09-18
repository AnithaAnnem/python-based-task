# -*- coding: utf-8 -*-
"""
Context setup for tests.
Ensures the `sample` module is importable during testing.
"""

import os
import sys
import sample  # noqa: F401  # Import placed at top to avoid E402

# Add the parent directory to sys.path so imports work
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)
