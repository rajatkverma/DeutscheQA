import yaml
import traceback


class Config:
    """
    load configuration file
    """

    def __init__(self, path_to_config='../config.yml'):
        self.path_to_config = path_to_config
        self.cfg = self.load_config()

    def load_config(self):
        """
        :return: return configurations
        """
        try:
            with open(self.path_to_config, 'r') as config:
                return yaml.load(config)
        except IOError:
            traceback.print_exc()
