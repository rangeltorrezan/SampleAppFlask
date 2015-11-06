""" Implementação da API de persistencia da classe modelo.
"""
__author__ = 'rangel'

from escola.abstractRepository import AbstractRepository
from ..aluno.model import Aluno


class AlunoRepository(AbstractRepository):
    """ Cria um repositorio injetando o comportamento CRUD para expor a camada controller.
    """
    __model__ = Aluno

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

