"""
Dynaconf app configuration
"""
import os
from pathlib import Path

from dynaconf import LazySettings

config = LazySettings(
    ROOT_PATH_FOR_DYNACONF=Path(os.path.abspath(__file__)).parent,
    PRELOAD_FOR_DYNACONF=['config/*'],
)
