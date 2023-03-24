"""
Dynaconf app configuration
"""
import os
from pathlib import Path

from dynaconf import LazySettings

settings = LazySettings(
    ROOT_PATH_FOR_DYNACONF=Path(os.path.abspath(__file__)).parent,
    PRELOAD_FOR_DYNACONF=['app.toml', 'logging.toml'],
    # SETTINGS_FILE_FOR_DYNACONF="settings.yaml"
)
