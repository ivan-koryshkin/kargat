from typing import List, Dict
import subprocess
import sys
import yaml

from .config import REQUIREMENTS, ROOT, DEV, TEST, PROD
from .base_manager import BaseManager

INSTALL = "install"
UNINSTALL = "uninstall"


class PackageManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(REQUIREMENTS, *args, **kwargs)

    def parse_packages(self) -> Dict[str, str]:
        """
        Get all requirement list from 'mode' section
        :return: {package_name: version}
        """
        body = self._file_repr.get(ROOT)
        reqs = body.get(REQUIREMENTS)
        if self._mode == PROD:
            req = reqs.get(self._mode)
        elif self._mode == DEV:
            req = reqs.get(self._mode)
            prod_req = reqs.get(PROD)
            req.update(prod_req)
        else:
            req = reqs.get(self._mode)
            dev_req = reqs.get(DEV)
            prod_req = reqs.get(PROD)
            req.update(dev_req)
            req.update(prod_req)
        return req

    @staticmethod
    def _pkg_str(name, version):
        return f"{name}=={version}" if version else name

    def _pip_do(self, cmd, name, version=None):
        """
        Python-pip wrapper
        :param cmd: pip command
        :param name: Package name
        :param version: Package version
        :return: None
        """
        if not version or version == "latest":
            pkg = name
        else:
            pkg = f"{name}=={version}"
        args = [sys.executable, "-m", "pip", cmd, pkg]
        if cmd == UNINSTALL:
            args += ['-y']
        
        self.console_info(f"[REQUIREMENT] {pkg}")
        res = subprocess.check_call(
            args, 
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT
        )
        if res.returncode != 0:
            print("Error")

    def for_each_package(self, cmd):
        """
        Run python-pip for each package in section 'mode'
        :param cmd: python-pip command
        :return: None
        """
        packages = self.parse_packages()
        for name in packages:
            version = packages[name]
            if version == 'latest':
                version = None
            self._pip_do(cmd, name, version)

    def install_all(self):
        self.for_each_package(INSTALL)

    def uninstall_all(self):
        self.for_each_package(UNINSTALL)

    def install(self, name: str):
        """
        cli `install` command 
        """
        section = self.get_section()
        parts = name.split("=")
        if len(parts) > 1:
            pkg = parts[0]
            version = parts[1]
        else:
            pkg = parts[0]
            version = 'latest'
        self._pip_do(INSTALL, pkg, version)
        section[self._mode][pkg] = version
        self.file_add_item(section)
    
    def uninstall(self, name: str):
        """
        cli `remove` command
        """
        parts = name.split("=")
        self._pip_do(UNINSTALL, parts[0])
        self.file_remove_item(parts[0])

    def run(self):
        self.install_all()

    def file_add_item(self, data):
        with open(self._config_file, 'r') as f:
            config_file = yaml.safe_load(f)
        with open(self._config_file, 'w') as f:
            config_file[ROOT][self._section] = data
            yaml.safe_dump(config_file, f)
    
    def file_remove_item(self, item):
        self._load_file()
        for stage in [DEV, PROD, TEST]:
            if item in self._file_repr[ROOT][REQUIREMENTS][stage]:
                self._file_repr[ROOT][REQUIREMENTS][stage].pop(item)
                with open(self._config_file, 'w') as f:
                    yaml.safe_dump(self._file_repr, f)