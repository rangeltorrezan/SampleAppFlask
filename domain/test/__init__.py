import os
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from escola import Base

__author__ = 'rangel'

# Private Singleton
_DATASTORE = None
_DATASTORE_URI = 'sqlite:///datatest.db'

def set_datastore(ds):
    """ Configura o data store.
    """
    global _DATASTORE
    _DATASTORE = ds

def get_datastore():
    """ Retorna o data store configurado.
    """
    return _DATASTORE

def get_datastore_uri():
    return _DATASTORE_URI


def prepara_base_de_testes():
    db_filename = 'datatest.db'
    schema_filename = 'schema.sql'
    db_is_new = not os.path.exists(db_filename)

    with sqlite3.connect(db_filename) as conn:
        if db_is_new:
            with open(schema_filename, 'rt') as f:
                schema = f.read()
            conn.executescript(schema)

        else:
            os.remove('datatest.db')
            prepara_base_de_testes()


def create_datastore(uri):
    engine = create_engine(uri, convert_unicode=True)
    db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False, bind=engine))
    Base.metadata.create_all(bind=engine)
    return db_session