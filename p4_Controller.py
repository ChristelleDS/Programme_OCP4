from p4_model import Database, Tournoi, Tour, Joueur, Match
from p4_view import Query


class Menu:
    def creer_tournoi():
        nom = input('Nom du tournoi?')
        lieu = input('Lieu du tournoi?')
        debut = input('Date de debut (JJ/MM/AAAA) ?')
        timecontrol = input('Contrôle du temps (bullet, blitz ou coup rapide?): ')
        description = input('Description?')
        t = nom
        t = Tournoi(nom, lieu, debut, timecontrol, description)
        controller.db.insert(t)
        print("sauvegardé en base de données")

    def creer_joueur():
        newjoueur = input("Identifiant du nouveau joueur ?")
        nom = input("Nom du joueur:")
        prenom = input("Prénom du joueur:")
        naissance = input("Date de naissance:")
        sexe = input("Homme (H) ou Femme (F):")
        classement = input("Classement général (0 par défaut):")
        newjoueur = Joueur(nom, prenom, naissance, sexe, classement)
        controller.db.insert(newjoueur)

    def inscrire_joueur():
        tournoi = input('Nom du tournoi:')
        joueur = input('Identifiant du joueur:')
        # tournoi_courant = TOURNOI.search(where(fin == ''))
        # print('tournoi courant: " + tournoi_courant)
        # tournoi_courant.addJoueur(joueur)

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
        pass

    def maj_classement(joueur, newClassement):
        joueur.maj_classement(newClassement)


class Controller:
    def __init__(self):
        self.ui = Menu()
        self.queries = Query()
        db_name = "db_echecs"
        self.db = Database(db_name)


controller = Controller()
Menu.creer_tournoi()
Menu.creer_joueur()
# Menu.inscrire_joueur()
# controller.ui.inscrire_joueur(TEST)
