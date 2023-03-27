"""
Package is responsible for deployment in different modes.
"""
import os
from pathlib import Path

from deploy.settings import DYNACONF_ROOT_PATH

PROJECT_DIR = str(Path(__file__).parent.parent.parent.resolve())
TEMPORARY_DIR = os.path.join(PROJECT_DIR, 'tmp/')

# allowed deployment modes
DEVELOPMENT_MODE = 'development'
PRODUCTION_MODE = 'production'

DEV_SETTINGS_FILE = os.path.join(DYNACONF_ROOT_PATH, 'config/dev-settings.yaml')
