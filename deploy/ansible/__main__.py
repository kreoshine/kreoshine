"""
Entry point for deploy via ansible
"""
import asyncio
from pathlib import Path

from concurrent.futures import ThreadPoolExecutor


async def execute_shell_command(shell_command: str) -> None:
    """
    Executes 'shell' command  and optionality saves its output

    Args:
        shell_command: ansible command to execute
    """
    shell_process = await asyncio.create_subprocess_shell(cmd=shell_command,
                                                          stdout=asyncio.subprocess.PIPE,
                                                          stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await shell_process.communicate()
    print(stderr.decode(encoding='utf-8'), stdout.decode(encoding='utf-8'))


if __name__ == '__main__':
    asyncio.get_event_loop().set_default_executor(ThreadPoolExecutor(max_workers=2))

    deploy_playbook = str(Path(__file__).parent.joinpath('playbooks/echo.yml'))
    inventory_file = str(Path(__file__).parent.joinpath('hosts'))

    asyncio.run(
        execute_shell_command(
            shell_command=f'ansible-playbook -v --inventory-file {inventory_file} {deploy_playbook}')
    )
