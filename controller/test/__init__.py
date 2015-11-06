__author__ = 'rangel'

import os
import sqlite3

def prepara_base_de_testes():
    db_filename = 'test.db'
    schema_filename = 'schema.sql'
    db_is_new = not os.path.exists(db_filename)

    with sqlite3.connect(db_filename) as conn:
        if db_is_new:
            with open(schema_filename, 'rt') as f:
                schema = f.read()
            conn.executescript(schema)

        else:
            os.remove('test.db')
            prepara_base_de_testes()
