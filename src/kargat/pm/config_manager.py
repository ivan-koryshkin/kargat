import os
import yaml
import pathlib

from .config import FILE_NAME
from .base_manager import BaseManager
from .package_manager import PackageManager
from .env_manager import EnvironmentManager
from .command_manager import CommandManger


class ConfigManger(BaseManager):
    def __init__(self, command):
        super().__init__("kargat")
        self._file_repr = {}
        self.command = command
        self.pkg_mgr = PackageManager()
        self.em = EnvironmentManager()
        self.cmd_mgr = CommandManger()

    def _load_file(self):
        with open(FILE_NAME, 'r') as f:
            self._file_repr = yaml.safe_load(f)

    def run(self):
        self._load_file()
        self.cmd_mgr.file_repr = self._file_repr
        self.pkg_mgr.file_repr = self._file_repr
        self.cmd_mgr.mode = "dev"
        self.pkg_mgr.mode = "dev"

        if self.command[0] == "init":
            name = self.request_name()
            author = self.request_author()
            version = self.request_verion()
            self.generate(name, version, author)
        elif self.command[0] == "install" and len(self.command) == 1:
            self.pkg_mgr.install_all()
        elif self.command[0] == "install":
            for pkg in self.command[1:]:
                self.pkg_mgr.install(pkg)
        elif self.command[0] == "uninstall":
            for pkg in self.command[1:]:
                self.pkg_mgr.uninstall(pkg)
        else:
            with EnvironmentManager(file_repr=self._file_repr, mode="dev") as em:
                self.cmd_mgr.run(self.command)
    
    def request_name(self):
        default_name = pathlib.Path(os.getcwd()).name
        name = input(f"Project name ({default_name}): ")
        return name if name else default_name
        
    def request_author(self):
        user = os.environ.get('USER', os.environ.get('USERNAME'))
        author = input(f"Author ({user}): ")
        return author if author else user
    
    def request_verion(self):
        default_version = "1.0.0"
        version = input(f"Version ({default_version}): ")
        return version if version else default_version