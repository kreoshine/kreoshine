"""
Automatic deployment with Ansible and ansible-runner
"""
import asyncio
import os

from concurrent.futures import ThreadPoolExecutor

from deploy import perform_deployment
from deploy.deploy_const import PROJECT_ROOT_PATH
from settings import config


def create_directory(dir_path: str):
    """ Creates a directory on the path if it is not created """
    try:
        os.makedirs(dir_path)
        print(f"Directory {dir_path} successfully created")
    except FileExistsError:
        print(f"Directory {dir_path} already exist")


def save_sudo_pass():
    sudo_pass = input("Enter sudo passwd of your user: ")
    config["deploy"]["local_sudo_passwd"] = sudo_pass


def create_ssh_keys():
    pass


if __name__ == '__main__':
    tmp_directory = os.path.join(PROJECT_ROOT_PATH, 'tmp/')
    create_directory(dir_path=tmp_directory)
    private_dir = os.path.join(PROJECT_ROOT_PATH, 'ansible/remote_deploy')
    create_directory(dir_path=private_dir)

    save_sudo_pass()
    create_ssh_keys()

    asyncio.new_event_loop().set_default_executor(ThreadPoolExecutor(max_workers=2))
    asyncio.run(
        perform_deployment(deploy_mode=config.deploy.mode,
                           runner_private_directory=private_dir,
                           local_output_dir=tmp_directory)
    )
