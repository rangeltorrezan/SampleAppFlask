__author__ = 'rangel'


class AbstractRepository(object):
    """ CRUD padrão para ser herdado pelas classes."""
    __model__ = None

    def _isinstance(self, model, raise_error=True):
        """ Verifica se o objeto especificado corresponde ao modelo do serviço.
        """
        rv = isinstance(model, self.__model__)
        if not rv and raise_error:
            raise ValueError('%s is not of type %s' % (model, self.__model__))
        return rv

    def _preprocess_params(self, kwargs):
        """Retorna um dicionário pré-processado de parâmetros. Usado por padrão
        antes de criar uma nova instância ou atualizar uma instância existente.
        :param kwargs: um dicionario de parametros.
        """
        kwargs.pop('csrf_token', None)
        return kwargs

    def save(self, db, model):
        """Persiste o objeto no banco de dados e o retorna.
        :param model: objeto a ser persistido.
        """
        self._isinstance(model)
        db.add(model)
        db.flush()
        return model

    def all(self, db):
        """Retorna uma lista de objetos.
        """
        return db.query(self.__model__).all()


    def get(self, db, id):
        """Retorna o objeto identificado pelo id.
        Retona 'None' se o objeto não existir.
        :param id: id do objeto.
        """
        return db.query(self.__model__).get(id)

    def get_all(self, db, *ids):
        """Retorna uma lista de objetos correspondentes aos ids.
        :param *ids: ids dos objetos.
        """
        return db.query(self.__model__).filter(self.__model__.id.in_(ids)).all()

    def find(self, db, **kwargs):
        """Retorna uma lista de objetos filtrados pelos parametros.
        :param **kwargs: filtros
        """
        return db.query(self.__model__).filter_by(**kwargs)

    def first(self, db, **kwargs):
        """Retorna o primeiro objeto encontrado do modelo do serviço filtrado pelo
        os argumentos de palavra chave especificada.
        :param **kwargs: filtros
        """
        return self.find(db, **kwargs).first()

    def new(self, **kwargs):
        """Retorna uma nova instancia, nao salvos de classe do modelo do serviço.
        :param **kwargs: instance parameters
        """
        return self.__model__(**self._preprocess_params(kwargs))

    def create(self, db, **kwargs):
        """Retorna uma nova instancia persistida no banco.
        :param **kwargs: parametros da nova instancia.
        """
        return self.save(db, self.new(**kwargs))

    def update(self, db, model, **kwargs):
        """Retorna uma instancia atualizada do modelo de classe do servico.
        :param model: instancia a ser atualizada.
        :param **kwargs: novos parametros.
        """
        self._isinstance(model)
        for k, v in self._preprocess_params(kwargs).items():
            setattr(model, k, v)
        self.save(db, model)
        return model

    def delete(self, db, model):
        """Apaga imediatamente uma instância especificada.
        :param model: objeto.
        """
        self._isinstance(model)
        db.delete(model)
        db.flush()
        return model