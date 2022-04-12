import datetime      # pip install datetime?
import itertools     # pip install itertools?
from tinydb import TinyDB, Query, where         # pip install tinydb


class Tournoi:
    idtournoi_counter = itertools.count(1)
    paires = []

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
        print(self.nom + " crée.")

    def addJoueur(self, joueur):
        self.joueurs.append(joueur)
        return str(joueur) + " inscrit au tournoi."

    def addTour(self, tour):
        self.tours.append(tour)
        print(tour.nom + " ajouté au " + self.nom)

    def cloturerTournoi(self):
        self.fin = datetime.datetime.today().strftime('%Y-%m-%d')
        print(self.nom + " cloturé.")

    def serialize(self):
        return { 'idtournoi': self.idtournoi,
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

    def unserialized(serialized_tournoi):
        idtournoi = serialized_tournoi["idtournoi"]
        nom = serialized_tournoi["nom"]
        lieu = serialized_tournoi["lieu"]
        date_debut = serialized_tournoi["date_debut"]
        date_fin = serialized_tournoi["date_fin"]
        tours = serialized_tournoi["tours"]
        joueurs = serialized_tournoi["joueurs"]
        timecontrol = serialized_tournoi["timecontrol"]
        description = serialized_tournoi["description"]
        nbtours = serialized_tournoi["nbtours"]
        return Joueur(idtournoi, nom, lieu, date_debut, date_fin, tours, joueurs, timecontrol, description, nbtours)

    def genererPaires(self,tour):
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
    idjoueur_counter = itertools.count(1)

    def __init__(self, nom, prenom, naissance, sexe, classement=0, points=0):
        self.idjoueur = next(self.idjoueur_counter)
        self.nom = str(nom)
        self.prenom = str(prenom)
        self.date_naissance = naissance
        self.sexe = sexe
        self.classement = int(classement)    # entier
        self.points = int(points)    # nb points
        print(self.nom + " " + self.prenom + " crée. Référence: " + self.nom[0:3]+self.prenom[0:3])

    def __str__(self):
        return f"{self.nom} {self.prenom}"

    def __repr__(self):
        return f"{self.nom} {self.prenom}, classement : {self.classement}, points : {self.points}"
        # return f"{self.idjoueur}"

    def serialize(self):
        return {'idjoueur': self.idjoueur,
                'nom': self.nom,
                'prenom': self.prenom,
                'date_naissance': self.date_naissance,
                'sexe': self.sexe,
                'classement': self.classement,
                'points': self.points,
                }

    def unserialized(serialized_joueur):
        idjoueur = serialized_joueur["idjoueur"]
        nom = serialized_joueur["nom"]
        prenom = serialized_joueur["prenom"]
        date_naissance = serialized_joueur["Date_naissance"]
        sexe = serialized_joueur["sexe"]
        classement = serialized_joueur["classement"]
        points = serialized_joueur["points"]
        return Joueur(idjoueur, nom, prenom, date_naissance, sexe, classement, points)

    def majClassement(self, newclassement):
        self.classement = newclassement
        print("classement mis à jour.")

    def majPoints(self, pointsgagnes):
        self.points = self.points + pointsgagnes
        print("score mis à jour")


class Tour:
    idtour_counter = itertools.count(1)

    def __init__(self, idtournoi, nomTOUR):
        self.idtournoi = idtournoi
        self.idtour = str(self.idtournoi) + str(next(self.idtour_counter))
        self.nom = nomTOUR
        self.dateHeureDebut = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        self.dateHeureFin = ""
        self.etat = "en cours"
        self.matchs = []
        print(self.nom + " crée. ID: " + str(self.idtour))

    def serialize(self):
        return {'idtournoi': self.idtournoi, 'idtour': self.idtour, 'nom': self.nom,
                'dateHeureDebut': self.dateHeureDebut, 'dateHeureFin': self.dateHeureFin,
                'etat': self.etat, 'matchs': self.matchs}

    def addMatch(self, match):
        result_j1 = [match.joueur1, match.score1]
        result_j2 = [match.joueur2, match.score2]
        match_result = (result_j1, result_j2)
        self.matchs.append(match_result)
        print("Match ajouté au tournoi.")

    def cloturerTour(self):
        self.etat = "Terminé"
        self.dateHeureFin = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        print(self.nom + " cloturé à " + self.dateHeureFin)


class Match:
    idmatch_counter = itertools.count(1)

    def __init__(self, idtournoi, tour, joueur1, joueur2, score1=0, score2=0):
        self.idtournoi = idtournoi
        self.idtour = tour.idtour
        self.idmatch = str(self.idtournoi) + str(self.idtour) + str(next(self.idmatch_counter))
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.score1 = int(score1)
        self.score2 = int(score2)
        print("Match " + str(self.idmatch) + " crée." + str(self.joueur1) + " vs " + str(self.joueur2))

    def serialize(self):
        return {'idtournoi': self.idtournoi, 'idtour': self.idtour, 'idmatch': self.idmatch,
                'joueur1': self.joueur1, 'joueur2': self.joueur2,
                'score1': self.score1, 'score2': self.score2}

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

match1.saveScore()
match2.saveScore()
match3.saveScore()
match4.saveScore()

print(round1.matchs)

tournoiParis.genererPaires()
"""
