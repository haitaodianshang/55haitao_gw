#coding: utf8

"""
@author: Wanzhi Du
@email : duwanzhi@55haitao.com
@time  : 2/18/16 5:23 PM
"""

# coding: utf8

import logging
import os, traceback

from tornado.options import parse_command_line, options, define

define("tornado_settings", default=None, help="tornado settings file")

def parse_config_file(path):
    """Rewrite tornado default parse_config_file.

    Parses and loads the Python config file at the given path.

    This version allow customize new options which are not defined before
    from a configuration file.
    """
    config = {}

    execfile(path, config, config)
    for name in config:
        if name in options:
            setattr(options, name, config[name])
        else:
            define(name, config[name])

def parse_options():
    _root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    _settings = os.path.join(_root, "settings.py")
    _settings_local = os.path.join(_root, "settings_local.py")

    try:
        parse_config_file(_settings)
        logging.info("Using settings.py as default settings.")
    except Exception, e:
        logging.error("No any default settings, are you sure? Exception: %s" % e)
        raise e

    try:
        parse_config_file(_settings_local)
        logging.info("Override some settings with local settings.")
    except Exception, e:
        logging.error("No local settings. Exception: %s" % e)

    parse_command_line()
    if options.tornado_settings:
        try:
            parse_config_file(os.path.join(_root, options.tornado_settings))
            logging.info("Override some settings with command line settings.")
        except Exception, e:
            logging.error("No command line settings. Exception: %s" % e)

    logger = logging.getLogger()
    for handler in logger.handlers:
        handler.setFormatter(logging.Formatter(fmt='[%(levelname)s %(asctime)s %(name)s %(module)s:%(lineno)d] %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
