# -*- coding: utf-8 -*-
__author__ = 'rangel'
from flask import Flask
import json
import pkgutil
import importlib

from sqlalchemy.ext.declarative import DeclarativeMeta
from flask import Blueprint, current_app
from flask.ext.sqlalchemy import SQLAlchemy
from escola import Base

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)
    ds_plugin = SQLAlchemy(app)
    SQLAlchemy(app, session_options={
        'autocommit': True,
        'autoflush': False
    })
    register_blueprints(app)
    Base.metadata.create_all(bind=ds_plugin.engine)  # Inserir sempre apos registrar os blueprints
    return app


def get_datastore_session():
    """ Retorna o data store configurado.
    """
    return current_app.extensions['sqlalchemy'].db.session

def register_blueprints(app):
    """Registra todos os blueprints em uma aplicação Flask.
    :param app: Flask aluno
    """
    package_name = __name__
    package_path = __path__

    register = []
    for _, name, _ in pkgutil.iter_modules(package_path):
        module = importlib.import_module('%s.%s' % (package_name, name))
        for item in dir(module):
            item = getattr(module, item)
            if isinstance(item, Blueprint):
                app.register_blueprint(item)
            register.append(item)
    return register



class JSONEncoder(json.JSONEncoder):
    """Classe customizada para serializar objetos em Json
    """
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)
