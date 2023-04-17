"""
TODO
"""
import os
import platform
import sys

from settings import config


class RootUtils:
    """
    Class with privilege escalation utilities for a Linux-based system
    """

    @property
    def sudo_passwd(self) -> str:
        """ Password of a user with sudo rights on the server """
        return config["deploy"]["local_sudo_passwd"]

    def create_protect_directory(self, dir_path: str) -> None:
        """ Equivalent of 'mkdirs -p {dir_path}' """
        if platform.system() == "Windows":  # dev support
            try:
                os.makedirs(dir_path)
            except FileExistsError:
                pass
            except PermissionError as err:
                sys.exit(f"\n PermissionError: {err}")

        else:  # target OS is Linux-based
            os.system(command=f"echo {self.sudo_passwd} | sudo -S mkdir -p {dir_path}")

    def touch_protected_file(self, file_path: str) -> None:
        """ Equivalent of 'touch {file_name}'"""
        if platform.system() == "Windows":  # dev support
            try:
                from pathlib import Path
                Path(file_path).touch()
            except PermissionError as err:
                sys.exit(f"\n PermissionError: {err}")

        else:  # target OS is Linux-based
            os.system(command=f"echo {self.sudo_passwd} | sudo -S touch {file_path}")

    def change_file_mode(self, file_path: str, access_rights: str):
        """ Equivalent of 'chmod {access_rights} {file_name}' with privilege escalation for Linux-based system """
        if platform.system() == "Windows":  # dev support
            pass

        else:  # target OS is Linux-based
            os.system(command=f"echo {self.sudo_passwd} | sudo -S chmod {access_rights} {file_path}")

