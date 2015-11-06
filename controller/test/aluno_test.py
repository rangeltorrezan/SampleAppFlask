__author__ = 'rangel'
import unittest
import json

from controller.rest import create_app
from controller.test import prepara_base_de_testes

class AlunoControllerTest(unittest.TestCase):

    def setUp(self):
        prepara_base_de_testes()
        app = create_app('config')
        self.app = app.test_client()
        self.app.testing = True

    def test_deve_ser_possivel_listar_alunos(self):
        response = self.app.get('/api/v1/alunos')
        expect = [{"id": 1, "nome": "Aluno Teste 1", "endereco": "Itacorubi"},
                  {"id": 2, "nome": "Aluno Teste 2", "endereco": "Centro"},
                  {"id": 3, "nome": "Aluno Teste 3", "endereco": "Tapera"}]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data.decode('utf-8')),expect)

    def test_deve_ser_possivel_listar_aluno_por_id(self):
        response = self.app.get('/api/v1/alunos/1')
        expect = {"id": 1, "nome": "Aluno Teste 1", "endereco": "Itacorubi"}

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data.decode('utf-8')),expect)

    def test_deve_serv_possivel_cadastrar_aluno(self):
        headers = [('Content-Type', 'application/json')]
        data = {"nome": "Rangel Torrezan", "endereco": "Itacorubi 2"}
        expect = {"id": 1, "nome": "Rangel Torrezan", "endereco": "Itacorubi 2"}
        response = self.app.post('/api/v1/alunos', headers=headers, data=json.dumps(data))
        data_return = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data_return["nome"],expect["nome"])

    def test_deve_ser_possivel_atualizar_aluno(self):
        headers = [('Content-Type', 'application/json')]
        data = {"nome": "Rangel Torrezan 2", "endereco": "Itacorubi 2"}
        expect = {"id": 1, "nome": "Rangel Torrezan 2", "endereco": "Itacorubi 2"}
        response = self.app.put('/api/v1/alunos/1', headers=headers, data=json.dumps(data))
        data_return = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data_return["nome"],expect["nome"])

    def test_deve_ser_possivel_exluir_aluno(self):
        expect = 'Elemento Apagado'
        response = self.app.delete('/api/v1/alunos/1')
        data_return = response.data.decode('utf-8')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data_return,expect)