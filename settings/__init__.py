"""
Dynaconf app configuration
"""
import os
from pathlib import Path

from dynaconf import LazySettings


config = LazySettings(
    ROOT_PATH_FOR_DYNACONF=Path(os.path.abspath(__file__)).parent,
    SETTINGS_FILE_FOR_DYNACONF="settings.yaml",
    ENV_SWITCHER_FOR_DYNACONF='KREOSHINE_ENV',  # `export KREOSHINE_ENV=target_environment` in .env file
    YAML_LOADER_FOR_DYNACONF='safe',
    environments=True,  # activate layered environments
    load_dotenv=True,  # read a .env file
)
