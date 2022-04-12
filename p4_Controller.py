from p4_model import Tournoi, Tour, Joueur, Match
from p4_view import Database


db = Database("db_echecs")

class Menu:
    @staticmethod
    def creer_tournoi():
        nom = input('Nom du tournoi (un seul mot):')
        lieu = input('Lieu du tournoi?')
        debut = input('Date de debut (JJ/MM/AAAA) ?')
        timecontrol = input('Contrôle du temps (bullet, blitz ou coup rapide?): ')
        description = input('Description?')
        t = nom
        t = Tournoi(nom, lieu, debut, timecontrol, description)
        db.insert(t)
        print("sauvegardé en base de données")

    @staticmethod
    def inscrire_joueur():
        tournoi_encours = db.query_1('TOURNOI', 'date_fin', '')[0]['nom']  # A VARIABILISER? A QUEL NIVEAU?
        j_nom = input('Nom du joueur à inscrire:')
        j_prenom = input('Prenom du joueur: ')
        object = db.query_2('JOUEUR', 'nom', j_nom, 'prenom', j_prenom)
        if object :
            tournoi_encours.addJoueur(object)
            db.update(tournoi_encours)
            print('Joueur inscrit au tournoi.')
        else :
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
        newtour = 'Round1' # + str(int(tour_encours[:1]) + 1) # a definir
        newtour = Tour(1, 'TOUR1')
        db.insert(newtour)
        #tournoi_encours.genererPaires()
        # afficher les matchs a jouer

    @staticmethod
    def entrer_resultats_tour():
        tour_encours = db.query_1('TOUR', 'etat', 'en cours')[0]['nom']
        # pour chaque match:
            # sauvegarde les scores du match (saveScore)
        for m in tour_encours.matchs:
            m.saveScore()
        # cloturer le tour (cloturerTour)
        tour_encours.cloturerTour()
        # ajouter le tour sur l'instance tournoi (addTour)
        tournoi_encours = db.query_1('TOURNOI', 'date_fin', '')[0]['nom']
        tournoi_encours.addTour(tour_encours)

    @staticmethod
    def maj_classement():
        Joueur = str(input('Identifiant du joueur à mettre à jour : '))
        Joueur.majClassement(input('Nouveau classement du joueur: '))


class Controller:
    def __init__(self):
        self.ui = Menu()
        # self.edito = Edito()
        # self.queries = Query()



ctr = Controller()
Menu.creer_tournoi()
Menu.inscrire_joueur()
Menu.demarrer_tour()


