import configparser
import os
import sys


class Config():

    def _configFile(self):
        configFileName = "com.galyuk.PhotoOrganizer.ini"
        configPath = {
            "darwin": str(os.path.expanduser("~"))+"/Library/Preferences",
            "win32": str(os.path.expanduser("~")),
            "linux": str(os.path.expanduser("~"))
        }

        return os.path.join(configPath[sys.platform], configFileName)

    def __enter__(self):
        self.config = configparser.ConfigParser()
        self.config.read_dict(self._defaults())
        self.config.read(self._configFile())

        return self.config

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type: raise
        with open(self._configFile(), 'w') as configfile:
            self.config.write(configfile)

    def _defaults(self):
        defaults = {
            "UI": {
                "geometry": "800x600+50+50",
            },
            "sourceList": {
                "Width": "400",
            },
            "trashList": {
                "height": "400",
            },
            "outputList": {
                "Width": "400",
            },
            "Pathes": {
                "source": os.path.expanduser("~"),
                "destination": os.path.expanduser("~")
            }
        }
        return defaults
