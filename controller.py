from model import Tournoi, Tour, Joueur, Match, Database


db = Database("db_echecs")
timecontrol_list = ['bullet', 'blitz', 'coup rapide']


class Controller:
    def __init__(self):
        self.db = db

    def reinitialize(self):
        self.db.truncate("JOUEUR")
        self.db.truncate("MATCH")
        self.db.truncate("TOURNOI")
        self.db.truncate("TOUR")

    def tournoi_encours(self):
        try:
            q = self.db.query_1('TOURNOI', 'date_fin', '')[0]
            tournoi_encours = Tournoi(q['nom'], q['lieu'],
                                      q['date_debut'], q['timecontrol'],
                                      q['description'], q['tours'],
                                      q['joueurs'], q['idtournoi'],
                                      q['nbtours'], q['date_fin'])
            return tournoi_encours
        except IndexError:
            return "Aucun tournoi en cours"

    def tour_encours(self):
        q = self.db.query_1('TOUR', 'etat', 'en cours')[0]
        tour_encours = Tour(q['idtournoi'], q['nom'], q['matchs'],
                            q['idtour'], q['date_debut'],
                            q['date_fin'], q['etat'])
        return tour_encours

    def creer_tournoi(self):
        # verifier si tournoi en cours, sinon créer un tournoi
        try:
            self.db.query_1('TOURNOI', 'date_fin', '')[0]
            print("Veuillez terminer le tournoi en cours.")
        except IndexError:
            nom = input('Nom du tournoi:')
            lieu = input('Lieu du tournoi?')
            debut = input('Date de debut (JJ/MM/AAAA) ?')
            timecontrol = input('Bullet, blitz ou coup rapide?: ')
            if timecontrol.lower() in timecontrol_list:
                pass
            else:
                timecontrol = input('Bullet, blitz ou coup rapide?: ')
            description = input('Description?')
            tours = []
            joueurs = []
            # identification de l'id tournoi
            try:
                idtournoi = max(list(map(lambda x: x['idtournoi'],
                                         self.db.get_all('tournoi')))) + 1
            except ValueError:    # création du 1er tournoi
                idtournoi = 1
            t = Tournoi(nom, lieu, debut, timecontrol, description,
                        tours, joueurs, idtournoi)
            matchs = []
            # initialiser le tour 1
            idtour = str(t.idtournoi)+'T1'
            round1 = Tour(t.idtournoi, 'round1', matchs, idtour)
            self.db.insert(round1)
            t.addTour(round1)
            self.db.insert(t)
            print("Nouveau tournoi crée.")

    def inscrire_joueur(self):
        tournoi = self.tournoi_encours()
        # vérification si place encore disponible:
        if len(tournoi.joueurs) < tournoi.nbtours*2:
            j_nom = input('Nom du joueur à inscrire:').upper()
            j_prenom = input('Prenom du joueur: ').lower()
            # joueur déjà connu en base de données ?
            try:
                q = self.db.query_2('JOUEUR', 'nom', j_nom,
                                    'prenom', j_prenom)[0]
                if q['idjoueur'] in tournoi.joueurs:
                    print('Ce joueur est déjà inscrit au tournoi.')
                else:
                    # inscrire le joueur et remettre ses points à zero
                    joueur = Joueur(q['nom'], q['prenom'],
                                    q['date_naissance'], q['sexe'],
                                    q['classement'], 0, q['idjoueur'])
                    tournoi.addJoueur(joueur)
                    self.db.update_item('TOURNOI', 'joueurs', tournoi.joueurs,
                                        'idtournoi', tournoi.idtournoi)
                    self.db.update_item('JOUEUR', 'points', joueur.points,
                                        'idjoueur', joueur.idjoueur)
                    print(str(joueur) + " inscrit au tournoi.")
            # joueur à créer:
            except IndexError:
                j_naissance = input('Date de naissance:')
                j_sexe = input('Homme (H) ou Femme (F):')
                j_classement = int(input('Classement général:'))
                try:
                    j_idjoueur = max(list(map(lambda x: x['idjoueur'],
                                              self.db.get_all('joueur')))
                                     )+1
                except ValueError:  # cas du 1er joueur crée
                    j_idjoueur = 1
                newjoueur = Joueur(j_nom, j_prenom, j_naissance, j_sexe,
                                   int(j_classement), 0, j_idjoueur)
                self.db.insert(newjoueur)
                tournoi.addJoueur(newjoueur)
                self.db.update_item('TOURNOI', 'joueurs', tournoi.joueurs,
                                    'idtournoi', tournoi.idtournoi)
                print('Nouveau joueur crée et inscrit au tournoi')
        else:
            print('Tournoi complet, nouvelle inscription impossible.')

    def get_liste_joueurs(self):
        # Renvoit la liste triée des instances de joueur du tournoi en cours
        tournoi_encours = self.tournoi_encours()
        liste_joueurs = []
        # recréer les instances de joueur et alimenter la liste
        for j in tournoi_encours.joueurs:
            q = self.db.query_1('JOUEUR', 'idjoueur', j)[0]
            joueur = Joueur(q['nom'], q['prenom'], q['date_naissance'],
                            q['sexe'], q['classement'],
                            q['points'], q['idjoueur'])
            liste_joueurs.append(joueur)
        # Trier par classement, puis par points
        liste_joueurs.sort(key=lambda x: x.classement, reverse=False)
        liste_joueurs.sort(key=lambda x: x.points, reverse=True)
        return liste_joueurs

    def creer_matchs_tour(self, paires_tour):
        i = 1
        tour_encours = self.tour_encours()
        print('Liste des matchs à jouer: ')
        for p in paires_tour:
            try:
                idmatch = max(list(map(lambda x: x['idmatch'],
                                       self.db.get_all('match')))) + 1
            except ValueError:
                idmatch = 1
            match = Match(tour_encours.idtour, p[0], p[1], idmatch)
            self.db.insert(match)
            i = i + 1
            print('Joueur ' + str(p[0]) + ' vs ' + str(p[1]))

    def creer_match_tour_manuel(self):
        j1 = input('Id du joueur 1:')
        j2 = input('Id du joueur 2:')
        if j1 == j2:
            print("Saisie invalide")
        else:
            paire = [[j1, j2]]
            self.creer_matchs_tour(paire)

    def get_first_paires(self, liste_joueurs):
        # Génère les paires pour le 1er tour
        paires_tour = []
        nb_joueurs = len(liste_joueurs)
        mid = int(nb_joueurs / 2)
        meilleurs = liste_joueurs[0:mid]
        moins_bons = liste_joueurs[mid:nb_joueurs]
        for paire in map(lambda x, y: [x.idjoueur, y.idjoueur],
                         meilleurs, moins_bons):
            paires_tour.append(paire)
        return paires_tour

    def get_next_paires(self, tournoi):
        # Génère les paires pour les tours suivants
        paires_tour = []
        matchs_joues = self.get_paires_jouees(tournoi.idtournoi)
        liste_joueurs = self.get_liste_joueurs()
        nb_joueurs = len(liste_joueurs)
        lj = []  # liste des joueurs déjà associés
        for i in range(0, nb_joueurs - 1):
            j1 = liste_joueurs[i].idjoueur
            j2 = liste_joueurs[i + 1].idjoueur
            # vérifier si les joueurs n'ont pas déjà été associé
            if j1 in list(set(lj)):
                continue
            elif j2 in list(set(lj)):
                # identifier le joueur suivant qui n'est pas associé
                r = i + 2
                while r in range(i + 2, nb_joueurs - 1) and \
                        liste_joueurs[r].idjoueur in list(set(lj)):
                    r = r + 1
                j2 = liste_joueurs[r].idjoueur
            else:
                pass
            paire = [j1, j2]
            paire_reverse = [j2, j1]
            # cette paire a t'elle déjà été joué
            if paire in matchs_joues \
                    or paire_reverse in matchs_joues:
                pass
            else:
                paires_tour.append(paire)
                lj.append(j1)
                lj.append(j2)
        return paires_tour

    def demarrer_tour(self):
        # vérifier le nombre d'inscrits au tournoi
        tournoi_encours = self.tournoi_encours()
        liste_joueurs = self.get_liste_joueurs()
        nb_joueurs = len(liste_joueurs)
        if nb_joueurs == tournoi_encours.nbtours*2:
            if self.db.query_3('MATCH', 'idtour', self.tour_encours().idtour,
                               'score1', 0, 'score2', 0):
                print('veuillez entrer les résultats du tour précédent.')
            else:
                # génération des paires lors du 1er tour
                if self.tour_encours().nom == 'round1':
                    paires_tour = self.get_first_paires(liste_joueurs)
                else:
                    # génération des paires lors des tours suivants
                    paires_tour = self.get_next_paires(tournoi_encours)
                # création des matchs
                self.creer_matchs_tour(paires_tour)
        else:
            print("Pas assez de joueurs inscrits")

    def entrer_resultats_tour(self):
        tour_encours = self.tour_encours()
        list_matchs = db.query_1('MATCH', 'idtour', tour_encours.idtour)
        # pour chaque match du tour:
        # sauvegarde les scores
        for m in list_matchs:
            # reconstituer l'objet match
            match = Match(m['idtour'], m['joueur1'], m['joueur2'],
                          m['idmatch'], m['score1'], m['score2'])
            # reconstituer les objets joueur
            j1 = self.db.query_1('JOUEUR', 'idjoueur', match.joueur1)[0]
            j2 = self.db.query_1('JOUEUR', 'idjoueur', match.joueur2)[0]
            player1 = Joueur(j1['nom'], j1['prenom'], j1['date_naissance'],
                             j1['sexe'], j1['classement'], j1['points'],
                             j1['idjoueur'])
            player2 = Joueur(j2['nom'], j2['prenom'], j2['date_naissance'],
                             j2['sexe'], j2['classement'], j2['points'],
                             j2['idjoueur'])
            # maj les scores sur l'objet match
            match.saveScore(player1, player2)
            self.db.update_item('MATCH', 'score1', match.score1,
                                'idmatch', match.idmatch)
            self.db.update_item('MATCH', 'score2', match.score2,
                                'idmatch', match.idmatch)
            # sauvegarder le match sur l'instance du tour
            tour_encours.addMatch(match)
            # maj les points des joueurs en base
            self.db.update_item('JOUEUR', 'points', player1.points,
                                'idjoueur', match.joueur1)
            self.db.update_item('JOUEUR', 'points', player2.points,
                                'idjoueur', match.joueur2)
        # maj les matchs sur l'instance du tour
        self.db.update_item('TOUR', 'matchs', tour_encours.matchs,
                            'idtour', tour_encours.idtour)
        # cloturer le tour et maj en base
        tour_encours.cloturerTour()
        self.db.update_item('TOUR', 'etat', tour_encours.etat,
                            'idtour', tour_encours.idtour)
        self.db.update_item('TOUR', 'date_fin',
                            tour_encours.date_fin,
                            'idtour', tour_encours.idtour)
        # Créer le tour suivant
        tournoi_encours = self.tournoi_encours()
        indice_tour = int(tour_encours.idtour[2:])+1
        if indice_tour <= tournoi_encours.nbtours:
            nom_tour = 'round' + str(indice_tour)
            idtour = str(tournoi_encours.idtournoi) +\
                'T' + str(indice_tour)
            matchs = []
            newtour = Tour(tournoi_encours.idtournoi, nom_tour,
                           matchs, idtour)
            self.db.insert(newtour)
            tournoi_encours.addTour(newtour)
            self.db.update_item('TOURNOI', 'tours', tournoi_encours.tours,
                                'idtournoi', tournoi_encours.idtournoi)
            print(newtour.nom + " à démarrer.")
        else:
            print("Tous les tours ont été joués, terminez le tournoi.")

    def maj_classement(self):
        lastname = input('Nom du joueur à mettre à jour :').upper()
        firstname = input('Prenom du joueur à mettre à jour :').lower()
        try:
            j_id = self.db.query_2('JOUEUR', 'nom', lastname,
                                   'prenom', firstname)[0].get('idjoueur')
            newclassement = int(input('Nouveau classement du joueur: '))
            self.db.update_item('JOUEUR', 'classement', newclassement,
                                'idjoueur', j_id)
        except IndexError:
            print('Joueur inconnu')

    def terminer_tournoi(self):
        tournoi = self.tournoi_encours()
        tournoi.cloturerTournoi()
        self.db.update_item('TOURNOI', 'date_fin', tournoi.date_fin,
                            'idtournoi', tournoi.idtournoi)

    def get_all_tournois(self):
        print('liste des tournois:')
        print("\n".join(list(map(lambda x: str(x['idtournoi'])
                                 + " - " + x['nom'],
                                 self.db.get_all('tournoi')))))

    def get_all_idtours_tournoi(self, idtournoi):
        print('Liste des tours du tournoi:')
        return self.db.query_1('TOURNOI', 'idtournoi', idtournoi)[0]['tours']

    def get_all_joueurs_tournoi(self, idtournoi):
        print('Liste des joueurs du tournoi:')
        return self.db.query_1('TOURNOI', 'idtournoi', idtournoi)[0]['joueurs']

    def get_all_matchs_tournoi(self, idtournoi):
        print('Liste des matchs pour le tournoi: ' + str(idtournoi))
        q = list(map(lambda x: x['idtour'] + " " + x['idmatch'] +
                     " - Joueur " + str(x['joueur1']) +
                     " vs " + str(x['joueur2']) +
                     " Score: " + str(x['score1']) +
                     "/" + str(x['score2']),
                     self.db.query_1('MATCH', 'idtournoi', str(idtournoi))))
        print("\n".join(q))

    def get_all_joueurs(self):
        print('Liste des joueurs par ordre alphabétique:')
        players_list = list(map(lambda x: x['nom'] + " " + x['prenom'] +
                                " (id:" + str(x['idjoueur']) +
                                ") classement: " + str(x['classement']),
                                self.db.get_all('joueur')))
        players_list.sort(reverse=False)  # tri par ordre alphabetique
        print("\n".join(players_list))

    def classement_general(self):
        print('Classement général:')
        liste = []
        for j in self.db.get_all('JOUEUR'):
            joueur = Joueur(j['nom'], j['prenom'], j['date_naissance'],
                            j['sexe'], j['classement'],
                            j['points'], j['idjoueur'])
            liste.append(joueur)
        liste.sort(key=lambda x: x.classement, reverse=False)
        print("\n".join(list(map(lambda x: " n°:" + str(x.classement) + " "
                                           + x.nom + " " + x.prenom +
                                           " (id: " + str(x.idjoueur) + ")",
                                 liste))))

    def classement_tournoi(self, idtournoi):
        print('Classement du tournoi' + str(idtournoi))
        liste = []
        for j in self.db.query_1('TOURNOI', 'idtournoi',
                                 idtournoi)[0]['joueurs']:
            q = self.db.query_1('JOUEUR', 'idjoueur', j)[0]
            joueur = Joueur(q['nom'], q['prenom'],
                            q['date_naissance'],
                            q['sexe'], q['classement'],
                            q['points'], q['idjoueur'])
            liste.append(joueur)
        liste.sort(key=lambda x: x.classement, reverse=False)
        liste.sort(key=lambda x: x.points, reverse=True)
        print("\n".join(list(map(lambda x: "Points: " +
                                           str(x.points) +
                                           " - " + x.nom +
                                           " " + x.prenom,
                                 liste))))

    def get_paires_jouees(self, idtournoi):
        return list(map(lambda x: [x['joueur1'], x['joueur2']],
                        self.db.query_1('MATCH', 'idtournoi',
                                        str(idtournoi))))
