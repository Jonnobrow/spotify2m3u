import confuse
import logging
import os
import sys

__version__ = "0.0.2"
__author__ = "Jonathan Bartlett <jonathan@jonnobrow.co.uk>"

config = confuse.LazyConfig('spotify2m3u', __name__)


# Get the environment variable, default INFO
log_level: str = os.getenv("LOGLEVEL", "INFO")
# Overwrite with config value
if "log_level" in config.keys():
    log_level = str(config["log_level"].get(str))
logger = logging.getLogger("spotify2m3u")
logger.setLevel(log_level)

sh = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
sh.setFormatter(formatter)
logger.handlers.clear()
logger.addHandler(sh)


def get_logger(module_name):
    return logging.getLogger('spotify2m3u').getChild(module_name)
