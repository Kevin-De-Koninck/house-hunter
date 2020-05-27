import os
import sys
import yaml
from logzero import logger
from ..helpers.helpers import Anon_dict


class Yaml_parser:
    def __init__(self, config_file):
        self.config_file = config_file
        self.check_if_file_exists()

    def check_if_file_exists(self):
        if not os.path.exists(self.config_file):
            logger.error("File '%s' does not exist...", self.config_file)
            sys.exit(1)
        if not os.path.isfile(self.config_file):
            logger.error("Path '%s' is not a file...", self.config_file)
            sys.exit(1)

    def parse_yaml(self):
        results = {}
        with open(self.config_file, 'r') as stream:
            try:
                results = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                logger.error("Error while parsing YAML file '%s':\n%s", self.config_file, exc)
                sys.exit(1)
        return results


class Settings:
    def __init__(self, config_file):
        self.pushover = None
        self.househunter = None
        for k, v in Yaml_parser(config_file).parse_yaml().items():
            if isinstance(v, dict):
                setattr(self, k, Anon_dict(v))
            else:
                setattr(self, k, v)

