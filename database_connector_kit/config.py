# coding: utf-8


__author__ = 'Frederick NEY'

import logging

from . import exceptions
from . import yaml


def _load(file, loader):
    """
    Load file for the framework's configuration
    :param file: path to file to load
    :type file: str
    :param loader: file handler that has a load method in it
    :type loader: yaml
    :return: loaded file in the format the loader returns
    :rtype: any
    """
    return loader.load(file)


def load_file(file, loader=yaml):
    """
    Load
    :param file: path to file to load
    :type file: str
    :param loader: (Optional default: yaml) File handler that has a load method in it
    :type loader: yaml
    :return: loaded file in the format the loader returns
    :rtype: any
    """
    conf = _load(file, loader)
    return conf


class Environment(object):
    """
    Class Environment act as a singleton where after loaded all
    the content of the attributes is available at any part of the project.

    Requires CONFIG_FILE environment variable to be set before loading.

    Needs to be loaded first with:

    >>> import os
    >>> Environment.load(os.environ['CONFIG_FILE'])

    Contains following attributes:
    Attributes
    ----------
    Databases:
        All databases related configuration for sqlalchemy database engines.
        It uses the DATABASES field within the yaml configuration file.
    """
    Databases = {}
    __default_runtime_change = False

    @staticmethod
    def _load(file, loader):
        """
        Load config file using a specific file handler
        :param file: path to file to load
        :type file: str
        :param loader:
        :type loader: yaml
        """
        return loader.load(file)

    @classmethod
    def load(cls, file):
        """
        Load configuration file. and fulfills class's attributes for handling them anywhere on the code.
        :param file: path to file to load
        """
        conf = cls._load(file, yaml)
        cls.load_databases(conf)

    @classmethod
    def load_databases(cls, conf):
        """
        Load database configurations into Databases class's attribute
        :param conf: dictionary with all the content of the config file
        :type conf: dict[str, dict]
        """
        try:
            for type in conf["DATABASES"]:
                if type != 'default':
                    cls.add_database(type, conf["DATABASES"][type])
                else:
                    cls.set_default_database(conf["DATABASES"][conf["DATABASES"][type]])
        except KeyError:
            cls.Databases = {}

    @classmethod
    def add_database(cls, db_type, db_conf):
        """
        Add database configuration within Databases class's attribute
        :param db_type: database type
        :type db_type: str
        :param db_conf: database configuration
        :type db_conf: dict[str, dict|str|int]
        :raises database_connector_kit.exceptions.runtime.DatabaseChangeException:
        if the database is already loaded within Databases class's attribute
        """
        db = cls.Databases.get(db_type, None)
        if db is None:
            cls.Databases[db_type] = db_conf
        elif db is not None:
            logging.warning("Database '{}' already set".format(db_type))
            raise exceptions.runtime.DatabaseChangeException(
                "Not permitted to change database '{}'  while app is running".format(db_type)
            )

    @classmethod
    def set_default_database(cls, db_conf):
        """
        Add default database configuration within Databases class's attribute
        :param db_type: database type
        :type db_type: str
        :param db_conf: database configuration
        :type db_conf: dict[str, dict|str|int]
        :raises database_connector_kit.exceptions.runtime.DatabaseChangeException:
        if the default database is already loaded within Databases class's attribute
        """
        db = cls.Databases.get('default', None)
        if db is None and cls.__default_runtime_change is False:
            cls.Databases['default'] = db_conf
            cls.__default_runtime_change = True
        elif db is not None:
            logging.warning("Default database already set")
        else:
            raise exceptions.runtime.DatabaseChangeException(
                "Not permitted to change default database while app is running"
            )
