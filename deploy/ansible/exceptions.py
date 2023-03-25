"""
Deployment exceptions
"""


class AnsibleExecuteError(Exception):
    """ Class of the exception that may be raised in the course of executing playbook by ansible """

    def __init__(self, err_code: int, playbook_file: str, fatal_output: str):
        super().__init__()
        self.code = err_code
        self.playbook_file = playbook_file
        self.fatal_output = fatal_output

    def __str__(self):
        return f"[rc: {self.code}] error during executing playbook '{self.playbook_file}'"
