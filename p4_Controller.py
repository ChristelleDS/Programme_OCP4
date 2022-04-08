from p4_model import Database, Tournoi, Tour, Joueur, Match
from p4_view import Query

db = Database('projet4_db')
db.create('Tournoi')
db.create('Joueur')
db.create('Tour')
db.create('Match')

class Menu:
    def creer_tournoi():
        nom = input('Nom du tournoi?')
        lieu = input('Lieu du tournoi?')
        debut = input('Date de debut (JJ/MM/AAAA) ?')
        timecontrol = input('Contrôle du temps (bullet, blitz ou coup rapide?): ')
        description = input('Description?')
        name = nom
        name = Tournoi(nom, lieu, debut, timecontrol, description )
        db.insert(name)
        print("sauvegardé en base de données")

    def inscrire_joueur():
        tournoi = input('Nom du tournoi:')
        joueur = input('Identifiant du joueur:')
        tournoi.addJoueur(joueur)
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
        pass

    def maj_classement(joueur, newClassement):
        joueur.maj_classement(newClassement)


class Controller:
    def __init__(self):
        self.ui = Menu()
        self.queries = Query()

controller = Controller()
Menu.creer_tournoi()
# controller.ui.inscrire_joueur(TEST)