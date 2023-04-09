"""
Automatic deployment with Ansible and ansible-runner
"""
import asyncio
import os

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from deploy import perform_deployment
from settings import config


def create_directory(dir_path: str):
    """ Creates a directory on the path if it is not created """
    try:
        os.makedirs(dir_path)
        print(f"Directory {dir_path} successfully created")
    except FileExistsError:
        print(f"Directory {dir_path} already exist")


if __name__ == '__main__':
    project_dir = str(Path(__file__).parent.parent.resolve())
    tmp_directory = os.path.join(project_dir, 'tmp/')
    create_directory(dir_path=tmp_directory)

    asyncio.new_event_loop().set_default_executor(ThreadPoolExecutor(max_workers=2))
    asyncio.run(
        perform_deployment(deploy_mode=config.deploy.mode,
                           local_output_dir=tmp_directory)
    )
