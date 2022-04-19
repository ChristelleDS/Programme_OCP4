from p4_model import Tournoi, Tour, Joueur, Match
from p4_view import Database
from pprintpp import pprint as pp
import json

db = Database("db_echecs")


class Menu:
    # tournoi_encours = db.get_current_tournament()
    # tour_encours = db.get_current_tour()

    @staticmethod
    def creer_tournoi():
        nom = input('Nom du tournoi (un seul mot):')
        lieu = input('Lieu du tournoi?')
        debut = input('Date de debut (JJ/MM/AAAA) ?')
        timecontrol = input('Contrôle du temps (bullet, blitz ou coup rapide?): ')
        if timecontrol.lower() in ctr.timecontrol_list:
            pass
        else:
            timecontrol = input('Contrôle du temps (bullet, blitz ou coup rapide?): ')
        description = input('Description?')
        t = Tournoi(nom, lieu, debut, timecontrol, description)
        db.insert(t)
        print("sauvegardé en base de données")

    @staticmethod
    def inscrire_joueur():
        j_nom = input('Nom du joueur à inscrire:')
        j_prenom = input('Prenom du joueur: ')
        q_joueur = db.query_2('JOUEUR', 'nom', j_nom, 'prenom', j_prenom)
        if isinstance(q_joueur, Joueur):
            tournoi_encours.addJoueur(q_joueur)
            db.update(tournoi_encours)
            print('Joueur inscrit au tournoi.')
        else:
            j_naissance = input('Date de naissance:')
            j_sexe = input('Homme (H) ou Femme (F):')
            j_classement = int(input('Classement général (0 par défaut, veuillez saisir un nombre entier):'))
            newjoueur = Joueur(j_nom, j_prenom, j_naissance, j_sexe, int(j_classement))
            db.insert(newjoueur)
            tournoi_encours.addJoueur(newjoueur)
            db.update(tournoi_encours)
            print('Nouveau joueur crée et inscrit au tournoi')

    @staticmethod
    def demarrer_tour():
        # créer prochain tour
        newtour = "round"+ current_round[:1]+1
        newtour = 'Round1'  # + str(int(tour_encours[:1]) + 1) # a definir
        newtour = Tour(1, 'Round1')
        db.insert(newtour)
        #  tournoi_encours.genererPaires()
        # afficher les matchs a jouer

    @staticmethod
    def entrer_resultats_tour():
        # pour chaque match:
        current_round ='round1'
        # sauvegarde les scores du match (saveScore)
        for match in current_round.matchs:
            match.saveScore()
            # db.update(match)
        # cloturer le tour (cloturerTour) et maj
        current_round.cloturerTour()
        db.update(current_round)
        # ajouter le tour sur l'instance tournoi (addTour)
        tournoi_encours.addTour(current_round)

    @staticmethod
    def maj_classement():
        player_lastname = input('Nom du joueur à mettre à jour :')
        player_firstname = input('Prenom du joueur à mettre à jour :')
        player = db.query_2('JOUEUR', 'nom', player_lastname, 'prenom', player_firstname)
        player.majClassement(input('Nouveau classement du joueur: '))
        db.update(player)

    @staticmethod
    def terminer_tournoi():
        tournoi_encours.cloturerTournoi()
        db.update(tournoi_encours)

class Controller:
    def __init__(self):
        self.ui = Menu()
        # self.edito = Edito()
        # self.queries = Query()
        self.timecontrol_list = ['bullet', 'blitz', 'coup rapide']


ctr = Controller()
# Menu.creer_tournoi()
# Menu.inscrire_joueur()
# Menu.demarrer_tour()
