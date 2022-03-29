import datetime


class Tournoi:
    def __init__(self, nom, lieu, debut, fin, timecontrol, description, nbtours=4):
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
        joueur = [joueur, 0]   # joueur + son nombre de points dans le tournoi initialisé à 0
        self.joueurs.append(joueur)

    def addTour(self, tour):
        self.tours.append(tour)

    def saveTournoi(self):  # a coder
        return "SaveTournoi"


class Joueur:
    def __init__(self, nom, prenom, naissance, sexe, classement):
        self.nom = nom
        self.prenom = prenom
        self.naissance = naissance
        self.sexe = sexe
        self.classement = classement

    def majClassement(self, newclassement):
        self.classement = newclassement


class Tour:
    def __init__(self, nom):
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
        print("générerPaires")


class Match:
    def __init__(self, joueur1, joueur2):
        self.resultat1 = [joueur1, 0]
        self.resultat2 = [joueur2, 0]
        # self.match = (resultat1, resultat2)

    def saveScore(self):
        score1 = input("Score du joueur " + str(self.resultat1[0].nom) + " " + str(self.resultat1[0].prenom) + " ?")
        resultat1 = [str(self.resultat1[0].nom) + " " + str(self.resultat1[0].prenom), score1]
        score2 = input("Score du joueur " + str(self.resultat2[0].nom) + " " + str(self.resultat2[0].prenom) + " ?")
        resultat2 = [str(self.resultat2[0].nom) + " " + str(self.resultat2[0].prenom), score2]
        self.match = (resultat1, resultat2)
        print(self.match)
        """
        # maj des points
        if score1 := score2:
            self.joueur1.majClassement(self.joueur1.classement+0.5)
        elif score1 > score2:
            self.joueur1.majClassement(self.joueur1.classement+1)
        elif score2 > score1:
            self.joueur2.majClassement(self.joueur2.classement + 1)
        """
    def majPoints(self):  # a coder
        # if self.match(1)[2] := self.match(2)[2]:
        print("calculPoints")


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


