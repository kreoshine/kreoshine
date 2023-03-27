"""
Script for compatibility ansible-runner with Windows
"""
import os.path
from platform import platform

from deploy.deployment import PROJECT_DIR


def remove_lines_in_files(target_file: str, deletion_indicator_word: str) -> None:
    """
    Removes all lines in file with defined word

    Args:
        target_file: file to be operated
        deletion_indicator_word: word-indicator for removing
    """
    with open(target_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(target_file, 'w') as file:
        for line in lines:
            if deletion_indicator_word not in line:
                file.write(line)


if __name__ == '__main__':
    if platform == 'Windows':
        problem_file = os.path.join(PROJECT_DIR, 'venv/lib/python3.9/site-packages/ansible_runner/utils/__init__.py')
        remove_lines_in_files(target_file=problem_file, deletion_indicator_word='fcntl')
