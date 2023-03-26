"""
Automatic deployment with Ansible and ansible-runner
"""
import asyncio
import os.path
from os import makedirs

from concurrent.futures import ThreadPoolExecutor

from deploy.ansible import ANSIBLE_PRIVATE_DATA_DIR, AnsibleExecutor, TEMPORARY_DIR
from settings import config, DYNACONF_ROOT_PATH

DEVELOPMENT_MODE = 'development'
PRODUCTION_MODE = 'production'

DEV_SETTINGS_FILE = os.path.join(DYNACONF_ROOT_PATH, 'config/dev-settings.yaml')


def create_ansible_dir_locally():
    """ Creates directories in project dir (i.e. tmp/ansible) """
    try:
        makedirs(ANSIBLE_PRIVATE_DATA_DIR)
        print(f"Directory {ANSIBLE_PRIVATE_DATA_DIR} successfully created")
    except FileExistsError:
        print(f"Directory {ANSIBLE_PRIVATE_DATA_DIR} already exist")
        pass


async def process_dev_deploy(ansible: AnsibleExecutor) -> None:
    """
    Entry point of deployment for the dev needs

    Args:
        ansible: instance of AnsibleExecutor class
    """
    print(f"Create .gitignore file to ignore dev settings change: {os.path.join(DYNACONF_ROOT_PATH, '.gitignore')}")
    gitignore_content = 'config/dev-settings.yaml'
    gitignore_creation_task = asyncio.create_task(ansible.execute_file_create_task(target_dir=DYNACONF_ROOT_PATH,
                                                                                   file_name='.gitignore',
                                                                                   file_content=gitignore_content))
    await gitignore_creation_task

    print(f"Set the file name for the log handler in dev settings file ({DEV_SETTINGS_FILE})")
    structural_gaps = ' ' * 8
    dynamic_service_log_path = os.path.join(TEMPORARY_DIR, 'service.log')
    dev_settings_update_task = asyncio.create_task(
        ansible.execute_file_line_update_task(file_path=DEV_SETTINGS_FILE,
                                              string_to_replace='filename: ""',
                                              new_string=f'{structural_gaps}filename: "{dynamic_service_log_path}"'))

    print(f"Define 'dev' environment for dynaconf: {os.path.join(DYNACONF_ROOT_PATH, '.env')}")
    dote_env_content = 'export KREOSHINE_ENV=DEVELOPMENT'
    env_creation_task = asyncio.create_task(ansible.execute_file_create_task(target_dir=DYNACONF_ROOT_PATH,
                                                                             file_name='.env',
                                                                             file_content=dote_env_content))
    await asyncio.gather(
        dev_settings_update_task,
        env_creation_task
    )


async def init_deploy():
    """ Entry point for deployment initialization """
    deploy_mode = config.deploy_mode
    if deploy_mode == DEVELOPMENT_MODE:
        target_host = 'localhost'  # fixme: here should be just local — unable to read 'hosts' file
    else:
        assert deploy_mode == PRODUCTION_MODE, \
            f"Only two modes of deployment is allowed: '{DEVELOPMENT_MODE}' and '{PRODUCTION_MODE}'"
        target_host = 'remote'
    print(f"Initiate '{deploy_mode}' mode of deployment")
    ansible_executor = AnsibleExecutor(destination_host=target_host)
    print(f"Successfully initiate instance of 'ansible executor' class for the '{target_host}' host")

    echo_task = asyncio.create_task(ansible_executor.execute_echo_task())
    await echo_task
    print(f"Connection to {target_host} host available")

    if deploy_mode == DEVELOPMENT_MODE:
        await process_dev_deploy(ansible=ansible_executor)


if __name__ == '__main__':
    create_ansible_dir_locally()
    asyncio.new_event_loop().set_default_executor(ThreadPoolExecutor(max_workers=2))
    asyncio.run(init_deploy())
