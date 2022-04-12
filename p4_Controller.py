from p4_model import Tournoi, Tour, Joueur, Match
from p4_view import Database


tournoi_encours = db.query_1(tournoi,fin,'')
print("Tournoi en cours : " + tournoi_encours)

tour_encours = db.query_1(tournoi,fin,'')
print("Tour en cours : " + tour_encours)

class Menu:
    def creer_tournoi():
        nom = input('Nom du tournoi?')
        lieu = input('Lieu du tournoi?')
        debut = input('Date de debut (JJ/MM/AAAA) ?')
        timecontrol = input('Contrôle du temps (bullet, blitz ou coup rapide?): ')
        description = input('Description?')
        t = nom
        t = Tournoi(nom, lieu, debut, timecontrol, description)
        ctr.db.insert(t)
        print("sauvegardé en base de données")

    def creer_joueur():
        newjoueur = input("Identifiant du nouveau joueur ?")
        nom = input("Nom du joueur:")
        prenom = input("Prénom du joueur:")
        naissance = input("Date de naissance:")
        sexe = input("Homme (H) ou Femme (F):")
        classement = input("Classement général (0 par défaut):")
        newjoueur = Joueur(nom, prenom, naissance, sexe, int(classement))
        ctr.db.insert(newjoueur)

    def inscrire_joueur():
        joueur = input('Identifiant du joueur:')
        tournoi_encours.addJoueur(joueur)
        ctr.db.update(tournoi_encours)

    def demarrer_tour():
        # créer prochain tour
        newtour = nomtour # a definir
        newtour = Tour(tournoi_encours,newtour)
        ctr.db.insert(newtour)
        # générer les paires (genererPaires)
        tournoi_encours.genererPaires()
        # afficher les paires et match
        pass

    def entrer_resultats_tour():
        tour = tour_encours
        # pour chaque match:
            # sauvegarde les scores du match (saveScore)
        for m in tour.matchs:
            m.saveScore()
        # cloturer le tour (cloturerTour)
        tour.cloturerTour
        # ajouter le tour sur l'instance tournoi (addTour)
        tournoi_encours.addTour(tour)

    def maj_classement():
        joueur = input("Identifiant du joueur à mettre à jour : ")
        newClassement = input("Nouveau classement du joueur: ")
        joueur.maj_classement(newClassement)


class Controller:
    def __init__(self):
        self.ui = Menu()
        # self.queries = Query()
        db_name = "db"
        self.db = Database(db_name)


ctr = Controller()
Menu.creer_tournoi()
Menu.creer_joueur()
ctr.db.get_all("TOURNOI")
# Q1 = ctr.db.query_1("TOURNOI","fin",'')
# print(Q1)

# Menu.inscrire_joueur()
# controller.ui.inscrire_joueur(TEST)
