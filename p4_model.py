import datetime      # pip install datetime?
import itertools     # pip install itertools?
import json
import pprint


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
        self.joueurs.append(joueur.idjoueur)
        return str(joueur) + " inscrit au tournoi."

    def addTour(self, tour):
        self.tours.append(tour.idtour)
        print(tour.nom + " ajouté au " + self.nom)

    def cloturerTournoi(self):
        self.fin = datetime.datetime.today().strftime('%Y-%m-%d')
        print(self.nom + " cloturé.")

    def __getitem__(self, items):
        print(type(items), items)

    def serialize(self):
        # return json.dumps(self.__dict__, lambda o: o.__dict__, indent=4)
        return { 'idtournoi': self.idtournoi, 'nom': self.nom, 'lieu': self.lieu,
                'date_debut': self.debut, 'date_fin': self.fin, 'tours': self.tours,
                'joueurs': self.joueurs, 'timecontrol': self.timecontrol,
                'description': self.description, 'nbtours': self.nbtours
                }

    def unserialized(serialized_tournoi):
        return Tournoi(**json.loads(serialized_tournoi))

    def genererPaires(self, tour):
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

    def __init__(self, nom, prenom, date_naissance, sexe, classement=0, points=0):
        self.idjoueur = next(self.idjoueur_counter)
        self.nom = str(nom)
        self.prenom = str(prenom)
        self.date_naissance = date_naissance
        self.sexe = sexe
        self.classement = int(classement)    # entier
        self.points = int(points)    # nb points
        print(self.nom + " " + self.prenom + " crée. Référence: " + self.nom[0:3]+self.prenom[0:3])

    def __str__(self):
        return f"{self.nom} {self.prenom}"

    def __repr__(self):
        return f"{self.nom} {self.prenom}, classement : {self.classement}, points : {self.points}"
        # return f"{self.idjoueur}"

    def __getitem__(self, items):
        print(type(items), items)

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
        return Joueur(**json.loads(serialized_joueur))

    def majClassement(self, newclassement):
        self.classement = newclassement
        print("classement mis à jour.")

    def majPoints(self, pointsgagnes):
        self.points = self.points + pointsgagnes
        print("score mis à jour")


class Tour:
    idtour_counter = itertools.count(1)

    def __init__(self, idtournoi, nom_tour):
        self.idtournoi = idtournoi
        self.idtour = str(self.idtournoi) + str(next(self.idtour_counter))
        self.nom = nom_tour
        self.date_heure_debut = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        self.date_heure_fin = ""
        self.etat = "en cours"
        self.matchs = []
        print(self.nom + " crée. ID: " + str(self.idtour))

    def __getitem__(self, items):
        print(type(items), items)

    def serialize(self):
        return {'idtournoi': self.idtournoi, 'idtour': self.idtour, 'nom': self.nom,
                'date_heure_debut': self.date_heure_debut, 'date_heure_fin': self.date_heure_fin,
                'etat': self.etat, 'matchs': self.matchs}

    def unserialized(serialized_tour):
        return Tour(**json.loads(serialized_tour))

    def addMatch(self, match):
        result_j1 = [match.joueur1, match.score1]
        result_j2 = [match.joueur2, match.score2]
        match_result = (result_j1, result_j2)
        self.matchs.append(match_result)
        print("Match ajouté au tournoi.")

    def cloturerTour(self):
        self.etat = "Terminé"
        self.date_heure_fin = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        print(self.nom + " cloturé à " + self.date_heure_fin)


class Match:
    idmatch_counter = itertools.count(1)

    def __init__(self, idtour, joueur1, joueur2, score1=0, score2=0):
        self.idtournoi = str(idtour)[0:1]
        self.idtour = idtour
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

    def unserialized(serialized_match):
        return Match(**json.loads(serialized_match))

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

