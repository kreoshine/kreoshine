"""
Module is responsible for deployment in development mode.
"""
import asyncio
import os

from deploy.ansible import AnsibleExecutor, TEMPORARY_DIR
from settings import DYNACONF_ROOT_PATH


async def process_dev_deploy(ansible: AnsibleExecutor) -> None:
    """
    Entry point of deployment for the dev needs

    Args:
        ansible: instance of AnsibleExecutor class
    """
    dev_config_file = os.path.join(DYNACONF_ROOT_PATH, 'config/log/dev_config.toml')
    print(f"Set the file name for the log handler ({dev_config_file})")
    dynamic_service_log_path = os.path.join(TEMPORARY_DIR, 'service.log')
    dev_settings_update_task = asyncio.create_task(
        ansible.execute_file_line_update_task(file_path=dev_config_file,
                                              string_to_replace='filename',
                                              new_string=f'filename = "{dynamic_service_log_path}"'))

    print(f"Define 'dev' environment for dynaconf: {os.path.join(DYNACONF_ROOT_PATH, '.env')}")
    dote_env_content = 'export KREOSHINE_ENV=DEVELOPMENT'
    env_creation_task = asyncio.create_task(ansible.execute_file_create_task(target_dir=DYNACONF_ROOT_PATH,
                                                                             file_name='.env',
                                                                             file_content=dote_env_content))
    await asyncio.gather(
        dev_settings_update_task,
        env_creation_task
    )
