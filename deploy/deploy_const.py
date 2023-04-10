"""
Deploy constants
"""
from pathlib import Path

PROJECT_ROOT_PATH = str(Path(__file__).parent.parent.resolve())

# allowed modes
DEVELOPMENT_MODE = 'development'
PRODUCTION_MODE = 'production'
