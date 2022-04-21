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

    def demarrer_tour(self):
        tour_encours = self.tour_encours()
        tournoi_encours = self.tournoi_encours()
        nb_joueurs = len(tournoi_encours.joueurs)
        mid = int(nb_joueurs / 2)
        liste_joueurs = []
        for j in tournoi_encours.joueurs:
            q = db.query_1('JOUEUR', 'idjoueur', j)[0]
            joueur = Joueur(q['nom'], q['prenom'], q['date_naissance'], q['sexe'], q['classement'],
                            q['points'], q['idjoueur'])
            liste_joueurs.append(joueur)
        # réinitialiser la liste des paires
        paires.clear()
        # tri des joueurs par classement et par points ( points à 0 lors du 1er tour)
        liste_joueurs.sort(key=lambda x: x.classement, reverse=False)
        liste_joueurs.sort(key=lambda x: x.points, reverse=False)
        # génération des paires
        for paire in map(lambda x, y: [x.idjoueur, y.idjoueur], liste_joueurs[0:mid], liste_joueurs[mid:nb_joueurs]):
            # cas des matchs déjà joués à coder
            paires.append(paire)
        # création des matchs
        i = 1
        for p in paires:
            idmatch = str('M'+i)
            match = Match(tour_encours.idtour, p[0], p[1], idmatch)
            db.insert(match)
            tour_encours.addMatch(match)
            db.update(tour_encours)

    def entrer_resultats_tour(self):
        tour_encours = self.tour_encours()
        # pour chaque match:
        # sauvegarde les scores du match (saveScore)
        for match in tour_encours.matchs:
            match.saveScore()
            # db.update(match)
        # cloturer le tour (cloturerTour) et maj
        tour_encours.cloturerTour()
        db.update(tour_encours)
        # Créer le tour suivant
        self.tournoi_encours().addTour(self.tour_encours())

    def maj_classement(self):
        player_lastname = input('Nom du joueur à mettre à jour :').upper()
        player_firstname = input('Prenom du joueur à mettre à jour :').lower()
        q = db.query_2('JOUEUR', 'nom', player_lastname, 'prenom', player_firstname)[0]
        player = Joueur(q['nom'], q['prenom'], q['date_naissance'], q['sexe'], q['classement'],
                        q['points'], q['idjoueur'])
        newclassement = int(input('Nouveau classement du joueur: '))
        player.majClassement(newclassement)
        # db.update(player)

    def terminer_tournoi(self):
        tournoi = self.tournoi_encours()
        tournoi.cloturerTournoi()
        db.update(tournoi)

    def get_all_tournois(self):
        return list(map(lambda x: str(x['idtournoi']) + " - " + x['nom'], db.get_all('tournoi')))

    def get_all_idjoueurs_tournoi(self, idtournoi):
        return db.query_1('TOURNOI', 'idtournoi', idtournoi)[0]['joueurs']

    def get_all_idtours_tournoi(self, idtournoi):
        return db.query_1('TOURNOI', 'idtournoi', idtournoi)[0]['tours']

    def get_all_idmatchs_tournoi(self, idtournoi):
        return db.query_1('TOURNOI', 'idtournoi', idtournoi)[0]['matchs']

    def get_all_joueurs(self):
        players_list = list(map(lambda x: x['nom'] + " " + x['prenom'] + " classement: "
                                          + str(x['classement']), db.get_all('joueur')))
        players_list.sort(reverse=False)  #tri par ordre alphabetique
        return players_list

    def classement_general(self):
        liste_joueurs = []
        for j in db.get_all('JOUEUR'):
            joueur = Joueur(j['nom'], j['prenom'], j['date_naissance'], j['sexe'], j['classement'],
                        j['points'], j['idjoueur'])
            liste_joueurs.append(joueur)
        liste_joueurs.sort(key=lambda x: x.classement, reverse=False)
        return list(map(lambda x: " n°: " + str(x.classement) + " - " + x.nom + " " + x.prenom, liste_joueurs))

    def classement_tournoi(self, idtournoi):
        liste_joueurs = []
        for j in db.query_1('TOURNOI', 'idtournoi', idtournoi)[0]['joueurs']:
            q = db.query_1('JOUEUR', 'idjoueur', j)[0]
            joueur = Joueur(q['nom'], q['prenom'], q['date_naissance'], q['sexe'], q['classement'],
                        q['points'], q['idjoueur'])
            liste_joueurs.append(joueur)
        liste_joueurs.sort(key=lambda x: x.points, reverse=False)
        return list(map(lambda x: "Points: " + str(x.points) + " - " + x.nom + " " + x.prenom, liste_joueurs))