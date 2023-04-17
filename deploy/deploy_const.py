"""
Deploy constants
"""
import os
from pathlib import Path

PROJECT_ROOT_PATH = str(Path(__file__).parent.parent.resolve())

PRIVATE_SSH_DIR = os.path.join(PROJECT_ROOT_PATH, ".ssh")

# allowed modes
DEVELOPMENT_MODE = 'development'
PRODUCTION_MODE = 'production'
