"""
Package with different helpfully utils
"""
import logging
import os
import shutil

logger = logging.getLogger('ansible_deploy')


def create_directory(dir_path: str):
    """ Creates a directory on the path if it is not created """
    try:
        os.makedirs(dir_path)
        logger.debug("Directory %s successfully created", dir_path)
    except FileExistsError:
        logger.debug("Directory %s already exist", dir_path)


def clear_directory(target_dir: str):
    """ Deletes all files in the directory

    ``rm -rf {target_dir} %% mkdir {target_dir}``
    Args:
        target_dir: directory path
    """
    for file in os.listdir(target_dir):
        filename = os.path.join(target_dir, file)
        if os.path.isfile(filename):
            os.remove(filename)
        elif os.path.isdir(filename):
            shutil.rmtree(filename)
