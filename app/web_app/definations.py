import os
import configparser

# Environment defination variable
ENV = os.environ["ENVIRONMENT"]
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_ROOT = os.path.join(ROOT_DIR, '/conf')


# settings
settings = configparser.ConfigParser()
BASEDIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = os.path.join(BASEDIR + '/conf/' + ENV + '_config.ini')
settings.read(CONFIG_FILE)
