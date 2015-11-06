"""
Entidade persistente (modelo)
"""
__author__ = 'rangel.torrezan'
from sqlalchemy import Column, Integer, String, Sequence
from escola import Base


class Aluno(Base):
    """ Aluno """
    __tablename__ = 'aluno'

    id = Column(Integer, Sequence('id_seq'), primary_key=True, nullable=False, unique=True)
    nome = Column('aluno', String(20))
    endereco = Column('endereco', String(20))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
