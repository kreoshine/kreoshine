"""
Different helpfully utils for deployment
"""
from os import makedirs

from ansible import ANSIBLE_PRIVATE_DATA_DIR


def create_ansible_dir_locally():
    """ Creates directories in project dir (i.e. tmp/ansible) """
    try:
        makedirs(ANSIBLE_PRIVATE_DATA_DIR)
        print(f"Directory {ANSIBLE_PRIVATE_DATA_DIR} successfully created")
    except FileExistsError:
        print(f"Directory {ANSIBLE_PRIVATE_DATA_DIR} already exist")
        pass
