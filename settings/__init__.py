"""
Dynaconf app configuration
"""
import os
from pathlib import Path

from dynaconf import LazySettings

DYNACONF_ROOT_PATH = Path(os.path.abspath(__file__)).parent

config = LazySettings(
    ROOT_PATH_FOR_DYNACONF=DYNACONF_ROOT_PATH,
    SETTINGS_FILE_FOR_DYNACONF=[
        'config/deploy/config.toml',
        'config/server/config.toml',
        'config/app/config.toml',
        'config/logging/main_service.toml',
    ],
    ENV_SWITCHER_FOR_DYNACONF='KREOSHINE_ENV',  # `export KREOSHINE_ENV=target_environment` in .env file
    YAML_LOADER_FOR_DYNACONF='safe',
    environments=True,  # activate layered environments
    load_dotenv=True,  # read a .env file
)
