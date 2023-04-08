"""
Module with a base mixin that is supposed to support
"""
from ansible_runner import Runner


class BaseExecutorMixin:
    """ Class is responsible for supporting mixins """

    @property
    def target_host_pattern(self) -> str:
        """ Target host pattern for which ansible executor is running """
        raise NotImplementedError

    def _run_playbook(self, params_to_execute: dict) -> Runner:
        """ Launches ansible runner with passed parameters as an `ansible-playbook` command
        See 'abstract ansible executor' for more info """
        raise NotImplementedError

    def _run_ad_hoc_command(self, params_to_execute: dict) -> Runner:
        """ Launches ansible runner with passed parameters as an `ad-hoc` command
        See 'abstract ansible executor' for more info"""
        raise NotImplementedError
