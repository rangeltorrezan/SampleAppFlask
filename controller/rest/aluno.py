# -*- coding: utf-8 -*-
""" API Rest Alunos
"""
__author__ = 'rangel.torrezan'

import json
from flask import abort, request, Blueprint

from rest import JSONEncoder, get_datastore_session
from escola.api import repositorio_alunos

bp = Blueprint('aluno', __name__)

@bp.route("/api/v1/alunos", methods=['GET'])
def get():
    """ Lista todos os alunos"""
    return json.dumps(repositorio_alunos.all(get_datastore_session()), cls=JSONEncoder)


@bp.route("/api/v1/alunos/<int:id>", methods=['GET'])
def get_id(id):
    """ Busca um aluno com id informado"""
    application = repositorio_alunos.get(get_datastore_session(), id)
    return json.dumps(application, cls=JSONEncoder)


@bp.route("/api/v1/alunos", methods=['POST'])
def create():
    """ Cria novo aluno com os parametros informado"""
    if not request.json:
        abort(400)

    return json.dumps(repositorio_alunos.create(get_datastore_session(), **request.json), cls=JSONEncoder)


@bp.route("/api/v1/alunos/<int:id>", methods=['PUT'])
def update(id):
    """ Atualiza aluno com id informado"""
    application = repositorio_alunos.update(get_datastore_session(), repositorio_alunos.get(get_datastore_session(), id), **request.json)
    return json.dumps(application, cls=JSONEncoder)


@bp.route("/api/v1/alunos/<int:id>", methods=['DELETE'])
def delete(id):
    """ Apaga aluno com id informado"""
    try:
        repositorio_alunos.delete(get_datastore_session(), repositorio_alunos.get(get_datastore_session(), id))
        return "Elemento Apagado"
    except ValueError:
        return None
