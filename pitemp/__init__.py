import json
from os.path import join, dirname

ROOT_DIR = dirname(dirname(__file__))

_config = None


def _load_config():
    global _config
    with open(join(ROOT_DIR, 'config.json'), 'r') as fp:
        _config = json.load(fp)


def get_config(key, default):
    global _config
    if not _config:
        _load_config()
    return _config.get(key, default)
