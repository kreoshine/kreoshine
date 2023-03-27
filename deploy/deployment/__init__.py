"""
Package is responsible for deployment in different modes.
"""
import os
from pathlib import Path

PROJECT_DIR = str(Path(__file__).parent.parent.parent.resolve())
TEMPORARY_DIR = os.path.join(PROJECT_DIR, 'tmp/')

# allowed deployment modes
DEVELOPMENT_MODE = 'development'
PRODUCTION_MODE = 'production'
