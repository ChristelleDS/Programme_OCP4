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
        self.joueurs.append(joueur)
    def addTour(self, tour):
        self.tours.append(tour)
    def saveTournoi(self):
        return "SaveTournoi?"

class Tour:
    def __init__(self, nom, dateHeureDebut, dateHeureFin, etat):
        self.nom = nom
        self.dateHeureDebut = dateHeureDebut
        self.dateHeureFin = dateHeureFin
        self.etat = etat
        self.matchs = []
    def addMatch(selfself,match):
        self.matchs.append(match)

class Joueur:
    def __init__(self, nom, prenom, naissance, sexe, classement):
        self.nom = nom
        self.prenom = prenom
        self.naissance = naissance
        self.sexe = sexe
        self.classement = classement
    def majClassement(self, classement):
        self.classement = classement

class Match:
    def __init__(self, tour, joueur1, joueur2, match="a jouer", score1="a jouer", score2="a jouer"):
        self.tour = tour
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.match = match
        self.score1 = score1
        self.score2 = score2
    def saveScore(self):
        self.score1 = input("Score du joueur "+self.joueur1+" ?")
        resultat1 = [self.joueur1, self.score1]
        self.score2 = input("Score du joueur "+self.joueur2+" ?")
        resultat2 = [self.joueur2, self.score2]
        self.match = (resultat1, resultat2)
        print(self.match)
      #  self.calculPoints()

"""
    def calculPoints(self, score1, score2, joueur1, joueur2):
        if self.score1 := self.score2:
            joueur1.classement = joueur1.classement+0.5
            joueur2.classement = joueur2.classement+0.5
        elif self.score1 > self.score2:
            joueur1.classement = joueur1.classement+1
        elif self.score2 > self.score1:
            joueur2.classement = joueur2.classement+1
"""

tournoiParis = Tournoi("Tournoi de Paris","Paris","10/03/2022","10/03/2022","Blitz","description")
roidesEchecs = Joueur("Roi", "Echecs", "01/08/1986", "Homme", 1)
challenger = Joueur("Alex", "Challenger", "01/12/1995", "Homme", 2)
julie = Joueur("Julie","Test","15/08/1975","Femme",3)
henri = Joueur("Henri","Test","25/08/1965","Homme",4)
john = Joueur("John","Do","25/08/1985","Homme",5)
victor = Joueur("Victor","Do","14/07/1968","Homme",6)
junior = Joueur("Junior","Dupont","04/04/1998","Homme",7)
alice = Joueur("Alice","Vendi","07/10/1995","Femme",8)

