from model import Tournoi, Tour, Joueur, Match, Database, datetime
from View import Menu


db = Database("db_echecs")
timecontrol_list = ['bullet', 'blitz', 'coup rapide']

class Controller:
    def __init__(self):
        self.ui = Menu()
        # self.edito = Edito()
        # self.queries = Query()
        self.db = db

    @staticmethod
    def reinitialize():
        db.truncate("JOUEUR")
        db.truncate("MATCH")
        db.truncate("TOURNOI")
        db.truncate("TOUR")

    @staticmethod
    def tournoi_encours():
        q = db.query_1('TOURNOI', 'date_fin', '')[0]
        tournoi_encours = Tournoi(q['nom'], q['lieu'], q['date_debut'], q['timecontrol'], q['description'], q['tours'],
                                  q['joueurs'], q['idtournoi'], q['nbtours'], q['date_fin'])
        return tournoi_encours

    @staticmethod
    def tour_encours():
        q = db.query_1('TOUR', 'etat', 'en cours')[0]
        tour_encours = Tour(q['idtournoi'], q['nom'], q['matchs'], q['idtour'], q['date_heure_debut'],
                            q['date_heure_fin'], q['etat'])
        return tour_encours

    @staticmethod
    def creer_tournoi():
        nom = input('Nom du tournoi (un seul mot):')
        lieu = input('Lieu du tournoi?')
        debut = input('Date de debut (JJ/MM/AAAA) ?')
        timecontrol = input('Contrôle du temps (bullet, blitz ou coup rapide?): ')
        if timecontrol.lower() in timecontrol_list:
            pass
        else:
            timecontrol = input('Contrôle du temps (bullet, blitz ou coup rapide?): ')
        description = input('Description?')
        tours = []
        joueurs = []
        t = Tournoi(nom, lieu, debut, timecontrol, description, tours, joueurs)
        matchs = []
        round1 = Tour(t.idtournoi, 'round1', matchs)
        db.insert(round1)
        db.insert(t)

    def inscrire_joueur(self):
        tournoi = self.tournoi_encours()
        j_nom = input('Nom du joueur à inscrire:').upper()
        j_prenom = input('Prenom du joueur: ').lower()
        try:
            q = db.query_2('JOUEUR', 'nom', j_nom, 'prenom', j_prenom)[0]
            joueur = Joueur(q['nom'], q['prenom'], q['date_naissance'], q['sexe'], q['idjoueur'],
                            q['classement'], q['points'])
            tournoi.addJoueur(joueur)
            db.update(tournoi)
            print('Joueur inscrit au tournoi.')
        except IndexError:
            j_naissance = input('Date de naissance:')
            j_sexe = input('Homme (H) ou Femme (F):')
            j_classement = int(input('Classement général (0 par défaut, veuillez saisir un nombre entier):'))
            newjoueur = Joueur(j_nom, j_prenom, j_naissance, j_sexe, int(j_classement))
            db.insert(newjoueur)
            tournoi.addJoueur(newjoueur)
            db.update(tournoi)
            print('Nouveau joueur crée et inscrit au tournoi')

    def entrer_resultats_tour(self):
        # pour chaque match:
        # sauvegarde les scores du match (saveScore)
        for match in self.tour_encours().matchs:
            match.saveScore()
            # db.update(match)
        # cloturer le tour (cloturerTour) et maj
        self.tour_encours().cloturerTour()
        db.update(self.tour_encours())
        # ajouter le tour sur l'instance tournoi (addTour)
        self.tournoi_encours().addTour(self.tour_encours())

    def maj_classement(self):
        player_lastname = input('Nom du joueur à mettre à jour :').upper()
        player_firstname = input('Prenom du joueur à mettre à jour :').lower()
        q = db.query_2('JOUEUR', 'nom', player_lastname, 'prenom', player_firstname)[0]
        player = Joueur(q['nom'], q['prenom'], q['date_naissance'], q['sexe'], q['classement'],
                        q['points'], q['idjoueur'])
        player.majClassement(input('Nouveau classement du joueur: '))
        db.update(player)