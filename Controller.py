from model import Tournoi, Tour, Joueur, Match, Database, datetime
from View import Menu


db = Database("db_echecs")
timecontrol_list = ['bullet', 'blitz', 'coup rapide']
paires = []


class Controller:
    def __init__(self):
        self.menu = Menu()
        # self.edito = Edito()
        self.db = db

    @staticmethod
    def reinitialize():
        db.truncate("JOUEUR")
        db.truncate("MATCH")
        db.truncate("TOURNOI")
        db.truncate("TOUR")

    @staticmethod
    def tournoi_encours():
        try:
            q = db.query_1('TOURNOI', 'date_fin', '')[0]
            tournoi_encours = Tournoi(q['nom'], q['lieu'], q['date_debut'], q['timecontrol'], q['description'], q['tours'],
                                  q['joueurs'], q['idtournoi'], q['nbtours'], q['date_fin'])
            return tournoi_encours
        except IndexError:
            return "Aucun tournoi en cours"

    @staticmethod
    def tour_encours():
        q = db.query_1('TOUR', 'etat', 'en cours')[0]
        tour_encours = Tour(q['idtournoi'], q['nom'], q['matchs'], q['idtour'], q['date_heure_debut'],
                            q['date_heure_fin'], q['etat'])
        return tour_encours

    def creer_tournoi(self):
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
        try:
            idtournoi = max(list(map(lambda x: x['idtournoi'], db.get_all('tournoi')))) + 1
        except ValueError:
            idtournoi = 1
        t = Tournoi(nom, lieu, debut, timecontrol, description, tours, joueurs, idtournoi)
        matchs = []
        round1 = Tour(t.idtournoi, 'round1', matchs)
        db.insert(round1)
        t.addTour(round1)
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
            try:
                j_idjoueur = max(list(map(lambda x: x['idjoueur'], db.get_all('joueur'))))+1
            except ValueError:
                j_idjoueur = 1
            newjoueur = Joueur(j_nom, j_prenom, j_naissance, j_sexe, int(j_classement), 0, j_idjoueur)
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
        newclassement = int(input('Nouveau classement du joueur: '))
        # player.majClassement(newclassement)
        db.update('classement', newclassement, q)

    def terminer_tournoi(self):
        tournoi = self.tournoi_encours()
        tournoi.cloturerTournoi()
        db.update(tournoi)

    def get_all_tournois(self):
        return list(map(lambda x: str(x['idtournoi']) + " - " + x['nom'], db.get_all('tournoi')))

    def get_all_idjoueurs_tournoi(self):
        return db.query_1('TOURNOI', 'idtournoi', self.tournoi_encours().idtournoi)[0]['joueurs']

    def get_all_idtours_tournoi(self):
        return db.query_1('TOURNOI', 'idtournoi', self.tournoi_encours().idtournoi)[0]['tours']

    def get_all_joueurs(self):
        players_list = list(map(lambda x: x['nom'] + " " + x['prenom'] + " classement: "
                                          + str(x['classement']), db.get_all('joueur')))
        players_list.sort(reverse=False)
        return players_list

    def query_double(self):
        # récupération des id joueurs du tournoi en cours
        q1 = self.db.query_1('TOURNOI', 'idtournoi', int(self.tournoi_encours().idtournoi))[0]['joueurs']
        q2 = self.get_all_joueurs()
        for q2['idjoueur'] in q1:
            print(q2['idjoueur'] + " - " + q2['nom'] + " " + q2['prenom'] + " classé: " + q2['classement'])
