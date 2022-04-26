import datetime      # pip install datetime?
# import itertools     # pip install itertools?
from tinydb import TinyDB, Query  # pip install tinydb
from tinydb.operations import set


class Tournoi:
    paires = []

    def __init__(self, nom, lieu, date_debut, timecontrol, description, tours, joueurs,
                 idtournoi=1, nbtours=4, date_fin=''):
        self.idtournoi = idtournoi
        self.nom = nom
        self.lieu = lieu
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.tours = tours
        self.joueurs = joueurs
        self.timecontrol = timecontrol
        self.description = description
        self.nbtours = int(nbtours)

    def addJoueur(self, joueur):
        self.joueurs.append(joueur.idjoueur)

    def addTour(self, tour):
        self.tours.append(tour.idtour)

    def cloturerTournoi(self):
        self.date_fin = datetime.datetime.today().strftime('%Y-%m-%d')
        print(self.nom + " cloturé.")

    def serialize(self):
        # return json.dumps(self.__dict__, lambda o: o.__dict__, indent=4)
        return {'idtournoi': self.idtournoi, 'nom': self.nom, 'lieu': self.lieu,
                'date_debut': self.date_debut, 'date_fin': self.date_fin, 'tours': self.tours,
                'joueurs': self.joueurs, 'timecontrol': self.timecontrol,
                'description': self.description, 'nbtours': self.nbtours
                }

    def genererPaires(self):
        # réinitialisation en dehors de la classe ?
        nb_joueurs = len(self.joueurs)
        mid = int(nb_joueurs/2)
        # 1er tour : tri par classement
        if len(self.tours) == 1:
            # REINITIALISATION des paires
            del self.paires
            # tri des joueurs par classement
            self.joueurs.sort(key=lambda x: x.classement, reverse=False)
            print("liste joueurs par classement:")
            print(self.joueurs)
            # définition des paires
            for paire in map(lambda x, y: [x, y], self.joueurs[0:mid], self.joueurs[mid:nb_joueurs]):
                self.paires.append(paire)
                # creer le match : paire = Match(current_tour, x.__name__, y.__name__, 0, 0)
                # print(paire)
        # tours suivants : tri par points et par classement si égalité de points
        else:
            pass
            """
            self.joueurs.sort(key=lambda x: x.classement, reverse=False)
            self.joueurs.sort(key=lambda x: x.points, reverse=True)
            print("liste joueurs par points:")
            print(self.joueurs)
            for paire in map(lambda x, y: [x, y], self.joueurs[0:mid], self.joueurs[mid:nb_joueurs]):
                # vérifier que la combinaison n'a pas déjà été joué
                if paire not in self.paires :  # matchs déjà joués self.tours.matchs
                    self.paires.append(paire)
                    print(paire)
                    # créer le match
                    newmatch = "m" + str(tour.idtour) + str(paire[0]) + str(paire[1])
                    newmatch = Match(self.idtournoi, tour, paire[0], paire[1])
                    db.insert(newmatch)
                    # ajouter le match au tour
                    tour.addMatch(newmatch)
                    db.update(tour.matchs) # affiner : maj uniquement la liste des matchs

                else:  # si paire déjà joué, second joueur = joueur suivant
                    paire[1]=next(paire)[1]
                    print(paire)
                    paires.append(paire) 
                    pass
            """
        print(self.paires)


class Joueur:

    def __init__(self, nom, prenom, date_naissance, sexe, classement=0, points=0, idjoueur=1):
        self.idjoueur = int(idjoueur)
        self.nom = str(nom)
        self.prenom = str(prenom)
        self.date_naissance = date_naissance
        self.sexe = sexe
        self.classement = int(classement)    # entier
        self.points = float(points)    # nb points
        # print(str("Joueur crée. ID: " + str(self.idjoueur)))

    def __str__(self):
        return f"{self.nom} {self.prenom}"

    def __repr__(self):
        return f"{self.nom} {self.prenom}, classement : {self.classement}, points : {self.points}"

    def serialize(self):
        return {'idjoueur': self.idjoueur, 'nom': self.nom, 'prenom': self.prenom,
                'date_naissance': self.date_naissance, 'sexe': self.sexe, 'classement': self.classement,
                'points': self.points}

    def majClassement(self, newclassement):
        self.classement = int(newclassement)
        print("classement mis à jour.")

    def majPoints(self, pointsgagnes):
        self.points = self.points + float(pointsgagnes)
        print("score mis à jour")


class Tour:

    def __init__(self, idtournoi, nom_tour, matchs, idtour,
                 date_heure_debut=datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
                 date_heure_fin="", etat="en cours"):
        self.idtournoi = idtournoi
        self.idtour = idtour
        self.nom = nom_tour
        self.date_heure_debut = date_heure_debut
        self.date_heure_fin = date_heure_fin
        self.etat = etat
        self.matchs = matchs

    def serialize(self):
        return {'idtournoi': self.idtournoi, 'idtour': self.idtour, 'nom': self.nom,
                'date_heure_debut': self.date_heure_debut, 'date_heure_fin': self.date_heure_fin,
                'etat': self.etat, 'matchs': self.matchs}

    def addMatch(self, match):
        result_j1 = [match.joueur1, match.score1]
        result_j2 = [match.joueur2, match.score2]
        match_result = (result_j1, result_j2)
        self.matchs.append(match_result)
        print("Match ajouté au tour.")

    def cloturerTour(self):
        self.etat = "Terminé"
        self.date_heure_fin = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        print(self.nom + " cloturé à " + self.date_heure_fin)


class Match:

    def __init__(self, idtour, joueur1, joueur2, idmatch="M1", score1=0, score2=0):
        self.idtour = idtour
        self.idtournoi = str(self.idtour)[0:1]
        self.idmatch = idmatch
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.score1 = int(score1)
        self.score2 = int(score2)

    def serialize(self):
        return {'idtournoi': self.idtournoi, 'idtour': self.idtour, 'idmatch': self.idmatch,
                'joueur1': self.joueur1, 'joueur2': self.joueur2,
                'score1': self.score1, 'score2': self.score2}

    def saveScore(self, joueur1, joueur2):
        self.score1 = input("Score de joueur " + str(self.joueur1) + " ?")
        self.score2 = input("Score de joueur " + str(self.joueur2) + " ?")
        if self.score1 == self.score2:
            joueur1.majPoints(0.5)
            joueur2.majPoints(0.5)
            print("EGALITE: +0.5 points")
            print(str(joueur1.prenom) + " : " + str(joueur1.points) + " points.")
            print(str(joueur2.prenom) + " : " + str(joueur2.points) + " points.")
        elif self.score1 > self.score2:
            joueur1.majPoints(1)
            print(str(joueur1.prenom) + " GAGNANT: + 1 point . Total de points: " + str(joueur1.points))
        elif self.score2 > self.score1:
            joueur2.majPoints(1)
            print(str(joueur2.prenom) + " GAGNANT: + 1 point . Total de points: " + str(joueur2.points))


class Database:
    def __init__(self, db_name):
        self.db = TinyDB(str(db_name) + '.json')

    def truncate(self, table_):
        self.db.table(table_.upper()).truncate()

    def insert(self, objet_):
        table_ = str(type(objet_)).upper().split(".")[1][:-2]
        self.db.table(table_).insert(objet_.serialize())

    def update_item(self, table_, var1, val1, var_cond, val_cond):
        q = Query()
        self.db.table(table_.upper()).update(set(var1, val1), q[var_cond] == val_cond)

    def get_all(self, table_):
        return self.db.table(table_.upper()).all()

    def query_1(self, table_, var_, val_):
        q = Query()
        return self.db.table(table_.upper()).search(q[var_] == val_)

    def query_2(self, table_, var_1, val_1, var_2, val_2):
        q = Query()
        return self.db.table(table_.upper()).search((q[var_1] == val_1) & (q[var_2] == val_2))

    def query_3(self, table_, var_1, val_1, var_2, val_2, var_3, val_3):
        q = Query()
        return self.db.table(table_.upper()).search((q[var_1] == val_1) & (q[var_2] == val_2) & (q[var_3] == val_3))

    def get_current_tournament(self):
        return self.query_1('TOURNOI', 'date_fin', '')[0]['nom']

    def get_current_tour(self):
        return self.query_1('TOUR', 'etat', 'en cours')[0]['nom']
