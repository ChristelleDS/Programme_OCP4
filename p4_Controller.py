from p4_model import Tournoi, Tour, Joueur, Match
from p4_view import Database


db = Database("db_echecs")
tournoi_encours = db.query_1('TOURNOI', 'date_fin', '')[0]['nom']
tour_encours = db.query_1('TOUR', 'etat', 'en cours')[0]['nom']


class Menu:
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

    def creer_joueur():
        nom = input('Nom du joueur:')
        prenom = input('Prénom du joueur:')
        newjoueur = nom[0:3] + prenom[0:3]
        naissance = input('Date de naissance:')
        sexe = input('Homme (H) ou Femme (F):')
        classement = int(input('Classement général (0 par défaut, veuillez saisir un nombre entier):'))
        newjoueur = Joueur(nom, prenom, naissance, sexe, int(classement))
        db.insert(newjoueur)

    def inscrire_joueur():
        joueur = input('Référence du joueur:')
        tournoi_encours.addJoueur(joueur)
        db.update(tournoi_encours)

    def demarrer_tour():
        # créer prochain tour
        newtour = 'Round1' # + str(int(tour_encours[:1]) + 1) # a definir
        newtour = Tour(1, 'TOUR1')
        db.insert(newtour)
        #tournoi_encours.genererPaires()
        # afficher les matchs a jouer

    def entrer_resultats_tour():
        tour = tour_encours
        # pour chaque match:
            # sauvegarde les scores du match (saveScore)
        for m in tour.matchs:
            m.saveScore()
        # cloturer le tour (cloturerTour)
        tour.cloturerTour()
        # ajouter le tour sur l'instance tournoi (addTour)
        tournoi_encours.addTour(tour)

    def maj_classement():
        Joueur = input('Identifiant du joueur à mettre à jour : ')
        Joueur.majClassement(input('Nouveau classement du joueur: '))


class Controller:
    def __init__(self):
        self.ui = Menu()
        # self.edito = Edito()
        # self.queries = Query()


ctr = Controller()
Menu.creer_tournoi()
Menu.creer_joueur()
Menu.creer_joueur()
Menu.creer_joueur()
Menu.creer_joueur()
Menu.creer_joueur()
Menu.creer_joueur()
Menu.creer_joueur()
Menu.creer_joueur()
Menu.demarrer_tour()
# Menu.maj_classement()
# Q1 = ctr.db.query_1("TOURNOI","fin",'')
# print(Q1)

# Menu.inscrire_joueur()
# controller.ui.inscrire_joueur(TEST)
