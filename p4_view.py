from tinydb import TinyDB, Query, where   # pip install tinydb
from pprint import pprint

class Database:
    def __init__(self, db_name):
        self.db = TinyDB(str(db_name) + '.json')

    def truncate(self, table_):
        self.db.table(table_.upper()).truncate()

    def insert(self, objet_):
        table_ = str(type(objet_)).upper().split(".")[1][:-2]
        self.db.table(table_).insert(objet_.serialize())

    def upsert(self, objet_):
        table_ = str(type(objet_)).upper().split(".")[1][:-2]
        self.db.table(table_).upsert(objet_.serialize())

    def update(self, objet_):
        table_ = str(type(objet_)).upper().split(".")[1][:-2]
        self.db.table(table_).update(objet_.serialize())

    def get_all(self, table_):
        return self.db.table(table_.capitalize()).all()

    def query_1(self, table_, var_, val_):
        q = Query()
        return self.db.table(table_.upper()).search(q[var_] == val_)

    def query_2(self, table_, var_1, val_1, var_2, val_2):
        q = Query()
        return self.db.table(table_.upper()).search((q[var_1] == val_1) & (q[var_2] == val_2))
