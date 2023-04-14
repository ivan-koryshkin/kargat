from typing import List
import subprocess
from .base_manager import BaseManager


class CommandManger(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__("command", *args, **kwargs)
        self._section_cmd = {}

    def _get_linked_commands(self, command):
        if not self._section_cmd:
            self._section_cmd = self.get_section()
        command = self._section_cmd.get(command)
        return command.get("before", []) if command else []

    def _run_command(self, command_key: str):
        command = self._section_cmd.get(command_key)
        shell_script = command.get("cmd")
        parts = shell_script.split()
        subprocess.check_call(parts)

    def run(self, commands: List[str]):
        for command in commands:
            linked_commands = self._get_linked_commands(command)
            if linked_commands:
                self.run(linked_commands)
            else:
                self._run_command(command)
