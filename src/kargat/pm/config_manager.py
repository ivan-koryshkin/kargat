import os
import sys
from typing import List
import yaml
import pathlib
import subprocess

from .config import FILE_NAME, DEV
from .base_manager import BaseManager
from .package_manager import PackageManager
from .env_manager import EnvironmentManager
from .command_manager import CommandManger


class ConfigManger(BaseManager):
    def __init__(
            self, 
            init: bool = False,
            install: bool | List[str] = False,
            uninstall: bool | List[str] = False,
            run: bool | List[str] = False,
            upgrade=False,
            mode: str = DEV
    ):
        super().__init__("kargat", mode=mode[0])
        self._file_repr = {}
        self.pkg_mgr = PackageManager(mode=mode[0])
        self.em = EnvironmentManager(mode=mode[0])
        self.cmd_mgr = CommandManger(mode=mode[0])
        # cli flags
        self._init_project = init
        self._install = self.handle_arg_list(install)
        self._uninstall = self.handle_arg_list(uninstall)
        self._run = self.handle_arg_list(run)
        self._upgrade = upgrade

    def _load_file(self):
        with open(FILE_NAME, 'r') as f:
            self._file_repr = yaml.safe_load(f)

    def run(self) -> bool:
        if not self._init_project:
            self._load_file()
        self.cmd_mgr.file_repr = self._file_repr
        self.pkg_mgr.file_repr = self._file_repr

        if self._init_project:
            name = self.request_name()
            author = self.request_author()
            version = self.request_version()
            self.generate(name, version, author)
            return True
        elif self._install is True:
            self.pkg_mgr.install_all(self._upgrade)
            return True
        elif self._uninstall is True:
            self.pkg_mgr.uninstall_all()
        elif self._install:
            for pkg in self._install:
                self.pkg_mgr.install(pkg, self._upgrade)
            return True
        elif self._uninstall:
            for pkg in self._uninstall:
                self.pkg_mgr.uninstall(pkg)
        elif self._run:
            with EnvironmentManager(file_repr=self._file_repr, mode="dev") as em:
                self.cmd_mgr.run(self._run)
            return True

    @staticmethod
    def request_name():
        default_name = pathlib.Path(os.getcwd()).name
        name = input(f"Project name ({default_name}): ")
        return name if name else default_name

    @staticmethod
    def request_author():
        user = os.environ.get('USER', os.environ.get('USERNAME'))
        author = input(f"Author ({user}): ")
        return author if author else user

    @staticmethod
    def request_version():
        default_version = "1.0.0"
        version = input(f"Version ({default_version}): ")
        return version if version else default_version

    @staticmethod
    def request_recreate_venv():
        answer = input(f"dir .venv exist, do you want to recreate? [N/y]")
        return answer == 'y'

    @staticmethod
    def venv_create():
        subprocess.check_call([sys.executable, '-m', 'venv', '.venv'])

    @staticmethod
    def has_venv():
        working_dir = os.getcwd()
        files = os.listdir(working_dir)
        flt_iter = next(filter(lambda file: file == '.venv', files), None)
        return flt_iter is not None

    @staticmethod
    def handle_arg_list(cli_args) -> List[str] | bool:
        if isinstance(cli_args, list):
            return cli_args if cli_args else True
        return False
