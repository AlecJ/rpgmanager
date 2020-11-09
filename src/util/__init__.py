import os
import logging
import logging.config
import configparser
from contextlib import contextmanager
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database

class Config(object):
    _cfg_parser = None
    _OPEN_WEAPTHER_API_KEY = None
    _LATITUDE = None
    _LONGITUDE = None
    _DB_URL = None
    _engine = None

    @property
    def cfg_parser(self):
        if self._cfg_parser is None:
            self._cfg_parser = configparser.ConfigParser()
            self._cfg_parser.read(self.CONFIG_PATH)
        return self._cfg_parser

    @property
    def OPEN_WEATHER_API_KEY(self):
        if self._OPEN_WEAPTHER_API_KEY is None:
            self._OPEN_WEAPTHER_API_KEY = self.cfg_parser.get('api', 'open_weather_api_key')
        return self._OPEN_WEAPTHER_API_KEY

    @property
    def LATITUDE(self):
        if self._LATITUDE is None:
            self._LATITUDE = self.cfg_parser.get('api', 'latitude')
        return self._LATITUDE

    @property
    def LONGITUDE(self):
        if self._LONGITUDE is None:
            self._LONGITUDE = self.cfg_parser.get('api', 'longitude')
        return self._LONGITUDE

    @property
    def DB_URL(self):
        if self._DB_URL is None:
            if self.ENVIRONMENT == 'development':
                self._DB_URL = self.cfg_parser.get('database', 'db_dev_url')
            else:
                self._DB_URL = self.cfg_parser.get('database', 'db_prod_url')
        return self._DB_URL

    @property
    def engine(self):
        if self._engine is None:
            url = os.environ.get('DATABASE_URL')
            if not url:
                url = self.DB_URL

            # Queue pool is already there by default, and we can just set the
            # pool parameters without creating or referencing a pool object
            # pool size is how many connections to hand out, 15 is the
            # max, and the pool recycle parameter says that don't keep
            # a connection for more than 900 seconds (15 minutes).
            self._engine = sqlalchemy.create_engine(
                url,
                # json_serializer=custom_dumps,
                # json_deserializer=custom_loads,
                isolation_level='READ_COMMITTED',
                pool_size=5,
                max_overflow=15,
                pool_recycle=900
            )

            # make sure database exists
            # TODO does not work with heroku db
            # if not database_exists(url):
                # create_database(url)

        return self._engine

    @property
    def ENVIRONMENT(self):
        return os.environ.get('ENV') or 'development'

    @property
    def CONFIG_PATH(self):
        return os.environ.get('CONFIG_PATH') or 'config.ini'

config = Config()


# Logging
logging.config.fileConfig(config.CONFIG_PATH)

def loggingFactory(module):
    """
    Factory method that returns a logger generation function with the
    prefix for the modules where it is used.
        _getLogger=loggingFactory('util.alstore')
        logger=_getLogger('method')
        logger.debug('Bla')
    :param module: optional namespace
    :return:
    """        

    def getLogger(method=None):
        name = "phnx." + (module if method is None else module + "." + method)
        return logging.getLogger(name)

    return getLogger


Session = None

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    # Init session
    if Session is None:
        Session = sessionmaker(bind=config.engine)

    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()