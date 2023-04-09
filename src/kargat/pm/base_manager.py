import logging
import yaml
from typing import Optional, Dict
from .config import *


class BaseManager:
    def __init__(self, section: str, file: Optional[str] = None):
        self._file_repr = {}
        self._mode = ""
        self._section = section
        self._config_file = file if file else FILE_NAME
        self.logger = logging.getLogger("kargat")

    def get_root(self):
        return self._file_repr.get('kargat')

    def get_section(self):
        root = self.get_root()
        section = root.get(self._section)
        return section

    @property
    def file_repr(self):
        return self._file_repr

    @property
    def mode(self):
        return self.mode

    @file_repr.setter
    def file_repr(self, value):
        self._file_repr = value

    @mode.setter
    def mode(self, value):
        self._mode = value

    def run(self, *args, **kwargs):
        raise Exception('Not implemented')

    def _load_file(self):
        with open(FILE_NAME, 'r') as f:
            self._file_repr = yaml.safe_load(f)

    @staticmethod
    def pattern(name, version, author) -> Dict:
        return {
            ROOT: {
                NAME: name,
                VERSION: version,
                AUTHOR: author,
                COMMAND: {
                    COMMAND_DEFAULT: {
                        COMMAND_CMD: "python3 main.py"
                    }
                },
                REQUIREMENTS: {
                    DEV: {'pytest': 'latest'},
                    PROD: {'pytest': 'latest'},
                    TEST: {'pytest': 'latest'}
                },
                ENVIRONMENT: {
                    DEV: [PYTHONUNBUFFERED],
                    PROD: [PYTHONUNBUFFERED],
                    TEST: [PYTHONUNBUFFERED]
                }
            }
        }

    
    def generate(self, name, version, author):
        file_content = self.pattern(name, version, author)
        with open(FILE_NAME, 'w') as f:
            yaml.safe_dump(file_content, f, sort_keys=False)

    def console_info(self, msg):
        self.logger.info(msg)