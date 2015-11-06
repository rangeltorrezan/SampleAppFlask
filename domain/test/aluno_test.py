__author__ = 'rangel'

import unittest

from escola.api import repositorio_alunos
from domain.test import get_datastore, set_datastore, get_datastore_uri

from test import create_datastore, prepara_base_de_testes


class AlunoDomainTest(unittest.TestCase):

    def setUp(self):
        set_datastore(create_datastore(get_datastore_uri()))
        prepara_base_de_testes()

    def test_deve_ser_possivel_listar_alunos(self):
        result = repositorio_alunos.all(get_datastore())[0]
        expect = repositorio_alunos.new(**{"id":1, "nome": "Aluno Teste 1", "endereco": "Itacorubi"})
        self.assertEqual(result.nome,expect.nome)
        self.assertEqual(result.endereco,expect.endereco)

    def test_deve_ser_possivel_listar_aluno_por_id(self):
        result = repositorio_alunos.get(get_datastore(), 1)
        expect = repositorio_alunos.new(**{"id":1, "nome": "Aluno Teste 1", "endereco": "Itacorubi"})
        self.assertEqual(result.nome,expect.nome)
        self.assertEqual(result.endereco,expect.endereco)

    def test_deve_ser_possivel_cadastrar_aluno(self):
        expect = repositorio_alunos.new(**{"nome": "Rangel Teste", "endereco": "Itacorubi"})
        result = repositorio_alunos.save(get_datastore(), expect)
        self.assertEqual(result.nome,expect.nome)
        self.assertEqual(result.endereco,expect.endereco)

    def test_deve_ser_possivel_atualizar_dados_do_aluno(self):
        aluno = repositorio_alunos.get(get_datastore(), 3)
        expect = {"nome": "Rangel Teste", "endereco": "Itacorubi"}
        result = repositorio_alunos.update(get_datastore(), aluno, **expect)
        self.assertEqual(result.nome, "Rangel Teste")

    def test_deve_ser_possivel_apagar_um_aluno(self):
        aluno = repositorio_alunos.get(get_datastore(), 2)
        expect = {"nome": "Aluno Teste 2", "endereco": "Centro"}
        result = repositorio_alunos.delete(get_datastore(), aluno)
        self.assertEqual(result.nome, "Aluno Teste 2")