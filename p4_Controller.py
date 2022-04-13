from p4_model import Tournoi, Tour, Joueur, Match
from p4_view import Database
from pprintpp import pprint as pp

db = Database("db_echecs")


class Menu:
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
        #  t = nom
        t = Tournoi(nom, lieu, debut, timecontrol, description)
        db.insert(t)
        print("sauvegardé en base de données")

    @staticmethod
    def inscrire_joueur():
        tournoi_encours = db.query_1('TOURNOI', 'date_fin', '')[0]['nom']
        # q_tournoi = db.query_1('TOURNOI', 'date_fin', '')[0]    # ['nom']  A VARIABILISER? A QUEL NIVEAU?
        # tournoi_encours = q_tournoi.unserialized().nom
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
        newtour = 'Round1'  # + str(int(tour_encours[:1]) + 1) # a definir
        newtour = Tour(1, 'Round1')
        db.insert(newtour)
        #  tournoi_encours.genererPaires()
        # afficher les matchs a jouer

    @staticmethod
    def entrer_resultats_tour():
        tour_encours = db.query_1('TOUR', 'etat', 'en cours')[0]['nom']
        # pour chaque match:
        # sauvegarde les scores du match (saveScore)
        for match in tour_encours.matchs:
            match.saveScore()
            db.update(match)
        # cloturer le tour (cloturerTour) et maj
        tour_encours.cloturerTour()
        db.update(tour_encours)
        # ajouter le tour sur l'instance tournoi (addTour)
        tournoi_encours = db.query_1('TOURNOI', 'date_fin', '')[0]['nom']
        tournoi_encours.addTour(tour_encours)

    @staticmethod
    def maj_classement():
        object.joueur = input('Identifiant du joueur à mettre à jour : ')
        object.joueur.majClassement(input('Nouveau classement du joueur: '))
        db.update(object.joueur)

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
