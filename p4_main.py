import datetime
import itertools
from tinydb import TinyDB, Query


class Database:
    # db = TinyDB('echecs_db.json')
    def __init__(self, db_name):
        self.db_ = TinyDB(str(db_name) + '.json')

    def truncate_table(self, table_):
        self.db_.table(table_.capitalize()).truncate()

    def insert(self, table_, dictionnaire):
        self.db_.table(table_.insert(dictionnaire))


class Tournoi:
    idtournoi_counter = itertools.count(1)
    # all_joueurs = []

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

    def addJoueur(self, joueur):
        self.joueurs.append(joueur)
        # all_joueurs.append(joueur)
        return joueur.nom + " " + joueur.prenom + " inscrit."

    def addTour(self, tour):
        self.tours.append(tour)

    def cloturerTournoi(self):
        self.fin = datetime.datetime.today().strftime('%Y-%m-%d')

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

    def genererPaires(self):  # a coder
        paires = {}  # dict avec les paires : match / JOUEUR1 / JOUEUR2
        # 1er tour
        joueurs_sorted = sorted(self.joueurs, key=lambda t: t[6])
        print(joueurs_sorted)
        nb_joueurs = len(joueurs_sorted)
        mid = nb_joueurs/2
        meilleurs = joueurs_sorted[0:mid]
        mauvais = joueurs_sorted[mid:nb_joueurs]
        for v in map(lambda x, y : x +"/"+ y, meilleurs, mauvais):
            print(v)

"""
        if not self.tours:
        else:
            #
            pass
"""

class Joueur:
    idjoueur_counter = itertools.count(1)
    all_joueurs = []

    def __init__(self, nom, prenom, naissance, sexe, classement, score=0):
        self.idjoueur = next(self.idjoueur_counter)
        self.nom = str(nom)
        self.prenom = str(prenom)
        self.date_naissance = naissance
        self.sexe = sexe
        self.classement = int(classement)    # entier
        self.score = int(score)    # nb points
        Joueur.all_joueurs.append(self)
        print(self.nom + " " + self.prenom + " crée. ID:" + str(self.idjoueur))

    def __str__(self):
        return f"{self.nom} {self.prenom}"

    def __repr__(self):
        return f"{self.idjoueur} {self.nom} {self.prenom}, classement : {self.classement}"

    def serialize(self):
        return {'idjoueur': self.idjoueur,
                'nom': self.nom,
                'prenom': self.prenom,
                'date_naissance': self.date_naissance,
                'sexe': self.sexe,
                'classement': self.classement,
                'score': self.score,
                }

    def unserialized(serialized_player):
        idjoueur = serialized_player["idjoueur"]
        nom = serialized_player["nom"]
        prenom = serialized_player["prenom"]
        date_naissance = serialized_player["date_naissance"]
        sexe = serialized_player["sexe"]
        classement = serialized_player["classement"]
        score = serialized_player["score"]
        return Joueur(idjoueur, nom, prenom, date_naissance, sexe, classement, score)

    def majClassement(self, newclassement):
        self.classement = newclassement

    def majScore(self, pointsgagnes):
        self.score = self.score + pointsgagnes
        return "score mis à jour"


class Tour:
    idtour_counter = itertools.count(0)

    def __init__(self, idtournoi, nom):
        self.idtournoi = idtournoi
        self.idtour = idtournoi + next(self.idtour_counter)
        self.nom = nom
        self.dateHeureDebut = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        self.dateHeureFin = ""
        self.etat = "en cours"
        self.matchs = []
        print(self.nom + " crée. ID: " + str(self.idtour))

    def addMatch(self, match):
        self.matchs.append(match)

    def cloturerTour(self):
        self.etat = "Terminé"
        self.dateHeureFin = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        print(self.nom + " cloturé à " + self.dateHeureFin)


class Match:
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
        return {'idtournoi': self.idtournoi, 'idtour': self.idtour, 'idmatch': self.idmatch,
                'joueur1': self.joueur1, 'joueur2': self.joueur2,
                'score1': self.score1, 'score2':self.score2 }

    def saveScore(self):
        self.joueur1[1] = input("Score de " + str(self.joueur1[0].nom) + " " +
                                 str(self.joueur1[0].prenom) + " ?")
        self.joueur2[1] = input("Score de " + str(self.joueur2[0].nom) + " " +
                                str(self.joueur2[0].prenom) + " ?")

    def calculPoints(self):
        if self.score1 == self.score2:
            self.joueur1.majScore(0.5)
        elif self.score1 > self.score2:
            self.joueur1.majScore(1)
        elif self.score2 > self.score1:
            self.joueur2.majScore(1)

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
db = TinyDB('echecs_db.json')
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
# Ajouter tour au tournoi
tournoiParis.addTour(round1)
# Instancier un match
match1 = Match(1, 11, alice, victor)
# Ajouter le match au 1er tour
round1.addMatch(match1)
print(Joueur.all_joueurs)
tournoiParis.genererPaires()





