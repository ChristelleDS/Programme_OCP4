import datetime

nbtoursparam = 4


class Tournoi:
    def __init__(self, idtournoi, nom, lieu, debut, fin, timecontrol, description, nbtours=nbtoursparam):
        self.idtournoi = idtournoi # générer l'id? self?
        self.nom = nom
        self.lieu = lieu
        self.debut = debut
        self.fin = fin
        self.tours = []
        self.joueurs = []
        self.timecontrol = timecontrol
        self.description = description
        self.nbtours = nbtours

    def addJoueur(self, joueur):
        self.joueurs.append(joueur)

    def addTour(self, tour):
        self.tours.append(tour)


class Joueur:
    def __init__(self, idjoueur, nom, prenom, naissance, sexe, classement, nbpoints=0):
        self.idjoueur = idjoueur # générer l'id?
        self.nom = nom
        self.prenom = prenom
        self.naissance = naissance
        self.sexe = sexe
        self.classement = classement
        self.nbpoints = nbpoints

    def majClassement(self, newclassement):
        self.classement = newclassement

    def majPoints(self, pointsgagnes):
        self.nbpoints = self.nbpoints + pointsgagnes


class Tour:
    def __init__(self, idtour, nom):
        self.idtour = idtour # générer l'id?
        self.nom = nom
        self.dateHeureDebut = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        self.dateHeureFin = ""
        self.etat = "en cours"
        self.matchs = []

    def addMatch(self, match):
        self.matchs.append(match)

    def cloturerTour(self):
        self.etat = "Terminé"
        self.dateHeureFin = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        print(self.nom + " cloturé à " + self.dateHeureFin)

    def genererPaires(self):  # a coder
        # 1er tour
            # participants triés par classement / 2 => 2 listes ordonnées
            # nouvelle liste de paires
        # tour suivant
            #
        pass


class Match:
    def __init__(self, idmatch, joueur1, joueur2, score1=0, score2=0):
        self.idmatch = idmatch  # générer l'id?
        self.joueur1 = [joueur1, 0]
        self.joueur2 = [joueur2, 0]
        self.score1 = score1
        self.score2 = score2

    def saveScore(self):
        self.joueur1[1]  = input("Score du joueur " + str(self.joueur1[0].nom) + " " + str(self.joueur1[0].prenom) + " ?")
        self.joueur2[1] = input("Score du joueur " + str(self.joueur2[0].nom) + " " + str(self.joueur2[0].prenom) + " ?")

    def majPointsJoueur(self):
        if self.joueur1[1] := self.joueur2[1]:
            self.joueur1.majPoints(0.5)
        elif self.joueur1[1] > self.joueur2[1]:
            self.joueur1.majPoints(1)
        elif self.joueur2[1] > self.joueur1[1]:
            self.joueur2.majPoints(1)

# Instancier un tournoi
tournoiParis = Tournoi("Tournoi de Paris", "Paris", "10/03/2022", "10/03/2022", "Blitz", "description")
# Instancier des joueurs
roidesEchecs = Joueur("Echecs", "Roi", "01/08/1986", "Homme", 1)
alex = Joueur("Test", "Alex", "01/12/1995", "Homme", 2)
julie = Joueur("Test", "Julie", "15/08/1975", "Femme", 3)
henri = Joueur("Test", "Henri", "25/08/1965", "Homme", 4)
john = Joueur("Do", "John", "25/08/1985", "Homme", 5)
victor = Joueur("Dodo", "Victor", "14/07/1968", "Homme", 6)
junior = Joueur("Dupont", "Junior", "04/04/1998", "Homme", 7)
alice = Joueur("Vendi", "Alice", "07/10/1995", "Femme", 8)
# Ajouter joueurs au tournoi
tournoiParis.addJoueur(victor)
tournoiParis.addJoueur(alice)
tournoiParis.addJoueur(henri)
tournoiParis.addJoueur(john)
# Instancier un tour
round1 = Tour("Round 1")
# Ajouter tour au tournoi
tournoiParis.addTour(round1)
# Instancier un match
match1 = Match(alice, victor)
# Ajouter le match au 1er tour
round1.addMatch(match1)
