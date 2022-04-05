import datetime
import random
import itertools
from tinydb import TinyDB, Query


class Database:
    def __init__(self, db_name):
        self.db_ = TinyDB(str(db_name) + '.json')

    def truncate_table(self, table_):
        self.db_.table(table_.capitalize()).truncate()

    def insert(self, table_, dictionnaire):
        self.db_.table(table_.insert(dictionnaire))


class Tournoi:
    """Modèle représentant un tournoi"""
    idtournoi_counter= itertools.count(1)
    def __init__(self, nom, lieu, debut, timecontrol, description, nbtours=4, fin=''):
        self.idtournoi = next(self.idtournoi_counter)
        self.nom = nom
        self.lieu = lieu
        self.debut = debut
        self.fin = fin
        self.tours = []
        self.joueurs = []
        self.timecontrol = timecontrol
        self.description = description
        self.nbtours = int(nbtours)

    def addJoueur(self, joueur):
        self.joueurs.append(joueur)

    def addTour(self, tour):
        self.tours.append(tour)

    def cloturerTournoi(self, datefin):
        self.fin = datetime.datetime.today().strftime('%Y-%m-%d')
        # Générer rapport des scores à l'issue du tournoi

class Joueur:
    """Modèle représentant un Joueur"""
    idjoueur_counter = itertools.count(1)
    def __init__(self, nom, prenom, dateNaissance, sexe, classement, score=0):
        self.idjoueur = next(self.idjoueur_counter)
        self.nom = str(nom)
        self.prenom = str(prenom)
        self.dateNaissance = dateNaissance
        self.sexe = sexe
        self.classement = int(classement)    # entier
        self.score = int(score)    # nb points

    def serialize(self):
        return { 'idjoueur': self.idjoueur,
                'nom': self.nom,
                'prenom': self.prenom,
                'dateNaissance': self.dateNaissance,
                'sexe': self.sexe,
                'classement': self.classement,
                'score': self.score,
                }

    def unserialized(serialized_player):
        idjoueur = serialized_player["idjoueur"]
        nom = serialized_player["nom"]
        prenom = serialized_player["prenom"]
        dateNaissance = serialized_player["dateNaissance"]
        sexe = serialized_player["sexe"]
        classement = serialized_player["classement"]
        score = serialized_player["score"]
        return Joueur(idjoueur, nom, prenom, dateNaissance, sexe, classement, score)

    def majClassement(self, newclassement):
        self.classement = newclassement

    def majScore(self, pointsgagnes):
        self.score = self.score + pointsgagnes


class Tour:
    idtour_counter = itertools.count(1)
    def __init__(self, idtournoi, nom):
        self.idtournoi = str(idtournoi)
        self.idtour = idtournoi + next(self.idtour_counter)
        self.nom = nom
        self.dateHeureDebut = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        self.dateHeureFin = ""
        self.etat = "en cours"
        self.matchs = []

    def addMatch(self, match):
        self.matchs.append(match)

    def cloturerTour(self):
        self.etat = "Terminé"
        self.dateHeureFin = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        print(self.nom + " cloturé à " + self.dateHeureFin)

    def genererPaires(self):  # a coder
        # 1er tour
            # participants triés par classement / 2 => 2 listes ordonnées
            # nouvelle liste de paires
        # tour suivant
            #
        pass


class Match:
    """Modèle représentant un match"""
    def __init__(self, idtournoi, idtour, joueur1, joueur2, score1=0, score2=0):
        self.idtournoi = idtournoi
        self.idtour = idtour
        self.idmatch = str(idtournoi) + str(idtour) + str(joueur1) + str(joueur2)
        self.joueur1 = joueur1
        #self.joueur1 = [joueur1, score1]
        self.joueur2 = joueur2
        self.score1 = int(score1)
        self.score2 = int(score2)

    def serialize(self):
        return {'idtournoi': self.idtournoi, 'idtour': self.idtour, 'idmatch': self.idmatch, 'joueur1': self.joueur1,
                'joueur2': self.joueur2, 'score1': self.score1, 'score2':self.score2 }

    def saveScore(self):
        self.joueur1[1]  = input("Score du joueur " + str(self.joueur1[0].nom) + " " + str(self.joueur1[0].prenom) + " ?")
        self.joueur2[1] = input("Score du joueur " + str(self.joueur2[0].nom) + " " + str(self.joueur2[0].prenom) + " ?")

    def calculPoints(self):
        if score1 := self.score2:
            self.joueur1.majScore(0.5)
        elif self.score1 > self.score2:
            self.joueur1.majScore(1)
        elif self.score2 > self.score1:
            self.joueur2.majScore(1)

class Interface:
    def démarrer_tournoi(self):
        nom = input("Nom du tournoi à créer: ")
        lieu = input ("Lieu du tournoi: ")
        debut = input("Date de début: ")
        fin = input("Date de fin: ")
        timecontrol = input("Contrôle du temps (bullet, blitz ou coup rapide?): ")
        description = input("Description: ")
        self.__init__()
        return "Tournoi "+ self.nom+ " crée. ID: "+self.idtournoi


# Instancier un tournoi
tournoiParis = Tournoi("Tournoi de Paris", "Paris", "10/03/2022", "Blitz", "description")
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
# Instancier un tour
round1 = Tour(1,"Round 1")
# Ajouter tour au tournoi
tournoiParis.addTour(round1)
# Instancier un match
match1 = Match(1, 11, alice, victor)
# Ajouter le match au 1er tour
round1.addMatch(match1)
