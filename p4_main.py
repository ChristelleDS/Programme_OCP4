import datetime
import itertools
from tinydb import TinyDB, Query


class Database:
    def __init__(self, db_name):
        self.db_ = TinyDB(str(db_name) + '.json')

    def truncate_table(self, table_):
        self.db_.table(table_.capitalize()).truncate()

    def insert(self, objet_):
        table_ = str(type(objet_)).capitalize()
        self.db_.table(table_).insert(objet_.serialize())

    def upsert(self, objet_):
        table_ = str(type(objet_)).capitalize()
        self.db_.table(table_).upsert(objet_.serialize())

    def update(self, objet_):
        table_ = str(type(objet_)).capitalize()
        self.db_.table(table_).update(objet_.serialize())


class Tournoi:
    idtournoi_counter = itertools.count(1)

    def __init__(self, nom, lieu, debut, timecontrol, description, nbtours=4, fin=''):
        self.idtournoi = next(self.idtournoi_counter)
        self.nom = nom
        self.lieu = lieu
        self.debut = debut
        self.fin = fin
        self.tours = []
        self.joueurs = []
        self.timecontrol = timecontrol
        self.description = str(description)
        self.nbtours = int(nbtours)
        print(self.nom + " crée. ID: " + str(self.idtournoi))
        db.insert(self)
        print("sauvegardé en base de données")

    def addJoueur(self, joueur):
        self.joueurs.append(joueur)
        #db.update(self)
        return str(joueur) + " inscrit."

    def addTour(self, tour):
        self.tours.append(tour)
        #db.update(self)
        print(tour.nom + " ajouté au " + self.nom)

    def cloturerTournoi(self):
        self.fin = datetime.datetime.today().strftime('%Y-%m-%d')
       # db.update(self)
        print(self.nom + " cloturé.")

    def serialize(self):
        return {'idtournoi': self.idtournoi,
                'nom': self.nom,
                'lieu': self.lieu,
                'date_debut': self.debut,
                'date_fin': self.fin,
                'tours': self.tours,
                'joueurs': self.joueurs,
                'timecontrol': self.timecontrol,
                'description': self.description,
                'nbtours': self.nbtours
                }

    def genererPaires(self):
        paires = []
        nb_joueurs = len(self.joueurs)
        mid = int(nb_joueurs/2)
        # 1er tour : tri par classement
        if len(self.tours) == 1 :
            # tri des joueurs par classement
            self.joueurs.sort(key=lambda x:x.classement, reverse=False)
            print("liste joueurs par classement:")
            print(self.joueurs)
            for paire in map(lambda x,y:[x,y],self.joueurs[0:mid], self.joueurs[mid:nb_joueurs]):
                paires.append(paire)
        # tours suivants : tri par points et par classement si égalité de points
        else:
            self.joueurs.sort(key=lambda x:x.classement, reverse=False)
            self.joueurs.sort(key=lambda x:x.points, reverse=True)
            print("liste joueurs par points:")
            print(self.joueurs)
            for paire in map(lambda x,y:[x,y],self.joueurs[0:mid], self.joueurs[mid:nb_joueurs]):
                # vérifier que la combinaison n'a pas déjà été joué
                if paire not in paires: # matchs déjà joués self.tours.matchs
                    paires.append(paire)
                    print(paire)
                else: # si paire déjà joué, second joueur = joueur suivant
                    """ paire[1]=next(paire)[1]
                    print(paire)
                    paires.append(paire) """
                    pass
        print(paires)


class Joueur:
    idjoueur_counter = itertools.count(1)

    def __init__(self, nom, prenom, naissance, sexe, classement, points=0):
        self.idjoueur = next(self.idjoueur_counter)
        self.nom = str(nom)
        self.prenom = str(prenom)
        self.date_naissance = naissance
        self.sexe = sexe
        self.classement = int(classement)    # entier
        self.points = int(points)    # nb points
        print(self.nom + " " + self.prenom + " crée. ID:" + str(self.idjoueur))
       # db.insert(self)
        print("sauvegardé en base de données")

    def __str__(self):
        return f"{self.nom} {self.prenom}"

    def __repr__(self):
        return f"{self.idjoueur}, classement : {self.classement}, points : {self.points}"
        #return f"{self.idjoueur}"

    def serialize(self):
        return {'idjoueur': self.idjoueur,
                'nom': self.nom,
                'prenom': self.prenom,
                'date_naissance': self.date_naissance,
                'sexe': self.sexe,
                'classement': self.classement,
                'points': self.points,
                }
"""
    def unserialized(serialized_player):
        idjoueur = serialized_player["idjoueur"]
        nom = serialized_player["nom"]
        prenom = serialized_player["prenom"]
        date_naissance = serialized_player["date_naissance"]
        sexe = serialized_player["sexe"]
        classement = serialized_player["classement"]
        points = serialized_player["points"]
        return Joueur(idjoueur, nom, prenom, date_naissance, sexe, classement, points)
"""
    def majClassement(self, newclassement):
        self.classement = newclassement
        print("classement mis à jour.")

    def majPoints(self, pointsgagnes):
        self.points = self.points + pointsgagnes
        print("score mis à jour")


class Tour:
    idtour_counter = itertools.count(1)

    def __init__(self, tournoi, nom):
        self.idtournoi = tournoi.idtournoi
        self.idtour = str(self.idtournoi) + str(next(self.idtour_counter))
        self.nom = nom
        self.dateHeureDebut = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        self.dateHeureFin = ""
        self.etat = "en cours"
        self.matchs = []
        print(self.nom + " crée. ID: " + str(self.idtour))
        db.insert(self)
        print("sauvegardé en base de données")

    def serialize(self):
        return {'idtournoi': self.idtournoi, 'idtour': self.idtour, 'nom': self.nom,
                'dateHeureDebut': self.dateHeureDebut, 'dateHeureFin': self.dateHeureFin,
                'etat': self.etat, 'matchs':self.matchs }

    def addMatch(self,match):
        result_j1 = [match.joueur1, match.score1]
        result_j2 = [match.joueur2, match.score2]
        match_result = (result_j1 , result_j2)
        self.matchs.append(match_result)
        print("Match ajouté au tournoi.")

    def cloturerTour(self):
        self.etat = "Terminé"
        self.dateHeureFin = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        print(self.nom + " cloturé à " + self.dateHeureFin)


class Match:
    idmatch_counter = itertools.count(1)
    def __init__(self, tournoi, tour, joueur1, joueur2, score1=0, score2=0):
        self.idtournoi = tournoi.idtournoi
        self.idtour = tour.idtour
        self.idmatch = str(self.idtournoi) + str(self.idtour) + str(next(self.idmatch_counter))
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.score1 = int(score1)
        self.score2 = int(score2)
        print( "Match "+ str(self.idmatch) + " crée." + str(self.joueur1) + " vs " + str(self.joueur2))
        #db.insert(self)
        print("sauvegardé en base de données")

    def serialize(self):
        return {'idtournoi': self.idtournoi, 'idtour': self.idtour, 'idmatch': self.idmatch,
                'joueur1': self.joueur1, 'joueur2': self.joueur2,
                'score1': self.score1, 'score2':self.score2 }

    def saveScore(self):
        self.score1 = input("Score de " + str(self.joueur1) + " ?")
        self.score2 = input("Score de " + str(self.joueur2) + " ?")
        if self.score1 == self.score2:
            self.joueur1.majPoints(0.5)
            self.joueur2.majPoints(0.5)
            print("EGALITE: +0.5 points")
            print(str(self.joueur1) + " : " + str(self.joueur1.points) + " points.")
            print(str(self.joueur2) + " : " + str(self.joueur2.points) + " points.")
        elif self.score1 > self.score2:
            self.joueur1.majPoints(1)
            print(str(self.joueur1) + " GAGNANT: + 1 point . Total de points: " + str(self.joueur1.points))
        elif self.score2 > self.score1:
            self.joueur2.majPoints(1)
            print(str(self.joueur2) + " GAGNANT: + 1 point . Total de points: " + str(self.joueur2.points))

"""
class Menu:
    @staticmethod
    def creer_tournoi():
        nom = input("Nom du tournoi à créer: ")
        lieu = input("Lieu du tournoi: ")
        debut = input("Date de début: ")
        timecontrol = input("Contrôle du temps (bullet, blitz ou coup rapide?): ")
        description = input("Description: ")
        nom = Tournoi(nom, lieu, debut, timecontrol, description )

    def inscrire_joueur(self):
        pass

    def demarrer_tour(tournoi):
        # créer prochain tour
        # générer les paires (genererPaires)
        # créer les matchs et les enregistrer sur le tour (addMatch)
        # afficher les paires et match
        pass

    def entrer_resultats_tour(tour):
        # pour chaque match:
            # sauvegarde les scores du match (saveScore)
            # maj le score global des joueurs (calculPoints)
        # cloturer le tour (cloturerTour)
        # ajouter le tour sur l'instance tournoi (addTour)

     def cloturer_tournoi(tournoi):
         tournoi.cloturerTournoi()
         # Générer rapport des scores à l'issue du tournoi

    def maj_classement(joueur, newClassement):
        joueur.maj_classement(newClassement)


class Query:
    pass


class Controller:
    def __init__(self):
        self.ui = Menu()
        self.queries = Query()


controller = Controller()
controller.ui.creer_tournoi()
controller.ui.inscrire_joueur(TEST)
"""
# Créer la bdd
#db = TinyDB('echecs_db.json')
db = Database('echecs_db')
print(db)
# Instancier un tournoi
tournoiParis = Tournoi("TournoiParis", "Paris", "10/03/2022", "Blitz", "description")
# Instancier des joueurs
roidesEchecs = Joueur("Echecs", "Roi", "01/08/1986", "Homme", 1)
alex = Joueur("Test", "Alex", "01/12/1995", "Homme", 2)
julie = Joueur("Test", "Julie", "15/08/1975", "Femme", 3)
henri = Joueur("Test", "Henri", "25/08/1965", "Homme", 4)
john = Joueur("Do", "John", "25/08/1985", "Homme", 5)
victor = Joueur("Dodo", "Victor", "14/07/1968", "Homme", 6)
junior = Joueur("Dupont", "Junior", "04/04/1998", "Homme", 7)
alice = Joueur("Vendi", "Alice", "07/10/1995", "Femme", 8)
# Ajouter joueurs au tournoi
tournoiParis.addJoueur(victor)
tournoiParis.addJoueur(alice)
tournoiParis.addJoueur(henri)
tournoiParis.addJoueur(john)
tournoiParis.addJoueur(alex)
tournoiParis.addJoueur(roidesEchecs)
tournoiParis.addJoueur(junior)
tournoiParis.addJoueur(julie)
# Instancier un tour
round1 = Tour(1,"Round 1")
round2 = Tour(1,"Round 2")
# Ajouter tour au tournoi
tournoiParis.addTour(round1)
#tournoiParis.addTour(round2)
# Instancier un match
match1 = Match(1, 11, alice, victor)
match2 = Match(1, 12, junior, alex)
match3 = Match(1, 13, henri, john)
match4 = Match(1, 14, roidesEchecs, julie)
# Ajouter le match au 1er tour
round1.addMatch(match1)
round1.addMatch(match2)
round1.addMatch(match3)
round1.addMatch(match4)
"""
match1.saveScore()
match2.saveScore()
match3.saveScore()
match4.saveScore()
"""
print(round1.matchs)

tournoiParis.genererPaires()









