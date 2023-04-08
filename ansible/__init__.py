"""
Contains a class responsible for executing ansible tasks via ansible-runner
"""
from ansible.abstract_executor import AbstractAnsibleExecutor
from ansible.mixins import PlaybookExecutorMixin, ModuleExecutorMixin


# pylint: disable = too-few-public-methods
class AnsibleExecutor(AbstractAnsibleExecutor, PlaybookExecutorMixin, ModuleExecutorMixin):
    """
    Represents async methods for running different tasks via ansible-runner
    """

    def __init__(self, host_pattern: str, private_data_dir: str, verbosity: int):
        super().__init__(private_data_dir, verbosity)
        self._host_pattern = host_pattern

    @property
    def target_host_pattern(self) -> str:
        """ Target host pattern for which ansible executor is running """
        return self._host_pattern
