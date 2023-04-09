import os
from typing import List, Optional
from .base_manager import BaseManager


class EnvironmentManager(BaseManager):
    def __init__(
            self,
            file_repr: Optional[dict] = None,
            mode: Optional[str] = None
    ):
        super().__init__('env')
        self.vars: List[str] = []
        self._file_repr = file_repr
        self._mode = mode

    def run(self):
        self._set_config_vars()

    def _read_vars(self):
        env = self.get_section()
        self.vars = env.get(self._mode)

    @staticmethod
    def _set_var(var: str):
        var_parts = var.split('=')
        os.environ[var_parts[0]] = var_parts[1]
        print(f'[ENV SET] {var_parts[0]}')

    @staticmethod
    def _clear_var(var: str):
        var_parts = var.split('=')
        os.environ.pop(var_parts[0])
        print(f'[ENV DEL] {var_parts[0]}')

    @staticmethod
    def _get_from_file(file_path: str) -> List[str]:
        with open(file_path, 'r') as f:
            var_list = f.readlines()
        return var_list if var_list else []

    def _set_all(self, var_list: List[str]):
        for var in var_list:
            self._set_var(var)

    def _set_config_vars(self):
        self._read_vars()
        if isinstance(self.vars, list):
            self._set_all(self.vars)
        elif isinstance(self.vars, dict):
            file = self.vars.get('env_file')
            self.vars = self._get_from_file(file)
            self._set_all(self.vars)

    def _clear_config_vars(self):
        for var in self.vars:
            self._clear_var(var)

    def __enter__(self):
        self._set_config_vars()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._clear_config_vars()

