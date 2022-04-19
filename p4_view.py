from tinydb import TinyDB, Query, where   # pip install tinydb
from pprintpp import pprint as pp  # pip install pprintpp

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
        return self.db.table(table_.upper()).all()

    def query_1(self, table_, var_, val_):
        q = Query()
        return self.db.table(table_.upper()).search(q[var_] == val_)

    def query_2(self, table_, var_1, val_1, var_2, val_2):
        q = Query()
        return self.db.table(table_.upper()).search((q[var_1] == val_1) & (q[var_2] == val_2))

    def get_list(self, object_):
        return list(map(lambda x: x["id"], self.get_all(object_)))

    def get_current_tournament(self):
        return self.query_1('TOURNOI', 'date_fin', '')[0]['nom']

    def get_current_tour(self):
        return self.query_1('TOUR', 'etat', 'en cours')[0]['nom']

    def get_list_rounds(self):
            return list(list(i.split(":")) for i in
                        set(map(lambda x: str(x['idtour']) + ":" + str(x['idtournoi']), self.get_all('MATCH'))))