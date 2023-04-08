"""
Module with class for playbook paths resolving
"""
import os
from pathlib import Path


class PermittedPlaybooksMixin:
    """ Class is responsible for playbook paths resolving """

    @property
    def _playbook_location_dir(self) -> str:
        """ Directory where the playbooks are located """
        return os.path.join(str(Path(__file__).parent.parent.resolve()), 'playbooks/')

    @property
    def echo_playbook(self) -> str:
        """ Path of the 'echo' playbook """
        return os.path.join(self._playbook_location_dir, 'echo.yml')

    @property
    def file_create_playbook(self) -> str:
        """ Path of the 'file_create' playbook """
        return os.path.join(self._playbook_location_dir, 'file_create.yml')
