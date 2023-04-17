"""
Package with different helpfully utils
"""
import logging
import os

logger = logging.getLogger('ansible_deploy')


def create_directory(dir_path: str):
    """ Creates a directory on the path if it is not created """
    try:
        os.makedirs(dir_path)
        logger.debug("Directory %s successfully created", dir_path)
    except FileExistsError:
        logger.debug("Directory %s already exist", dir_path)
