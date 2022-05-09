import time


class Menu:
    def __init__(self, controller):
        self.controller = controller

    def quitter_programme(self):
        mess = """
                    Sortie du programme?
                    [O]: OUI
                    [N]: NON
                    """
        print(mess)
        rep = input()
        if rep.upper() == 'O':
            print('Le programme va fermer.')
            time.sleep(3)
            print(exit())
        else:
            self.home()

    def home(self):
        message = """
            Bienvenue sur la page d'accueil\n
            Voici les actions possibles depuis ce menu : \n
            [1]: Créer un nouveau tournoi\n
            [2]: Inscrire un joueur au tournoi\n
            [3]: Démarrer un tour\n
            [4]: Entrer les résultats du tour\n
            [5]: Terminer le tournoi\n
            [6]: Maj le classement d'un joueur\n
            [7]: Accés aux reports\n
            [X]: Sortir de l''application\n
        """
        print(message)
        option = input("Quelle action réaliser ?")
        dicto = {'1': 'self.controller.creer_tournoi()',
                 '2': 'self.controller.inscrire_joueur()',
                 '3': 'self.controller.demarrer_tour()',
                 '4': 'self.controller.entrer_resultats_tour()',
                 '5': 'self.controller.terminer_tournoi()',
                 '6': 'self.controller.maj_classement()',
                 '7': 'self.report()',
                 'X': 'self.quitter_programme()'}
        try:
            eval(dicto[option.upper()])
            time.sleep(3)
        except KeyError:
            print("Instruction non reconnue")
            time.sleep(3)
        self.home()

    def report(self):
        message = """
            Voici la liste des reportings disponibles:
            [1]: Classement général
            [2]: Joueurs par ordre alphabétique
            [3]: Liste des tournois
            [4]: Liste des joueurs d'un tournoi
            [5]: Classement d'un tournoi
            [6]: Liste des matchs d'un tournoi
            [7]: Liste des tours d'un tournoi
            [R]: retour à l'accueil
        """
        print(message)
        option = str(input("Quelle action réaliser ?"))
        dicto = {'1': 'self.controller.classement_general()',
                 '2': 'self.controller.get_all_joueurs()',
                 '3': 'self.controller.get_all_tournois()',
                 '4': 'print(self.controller.get_all_joueurs_tournoi(int(input(\'Id du tournoi?\'))))',
                 '5': 'print(self.controller.classement_tournoi(int(input(\'Id du tournoi?\'))))',
                 '6': 'print(self.controller.get_all_matchs_tournoi(int(input(\'Id du tournoi?\'))))',
                 '7': 'print(self.controller.get_all_idtours_tournoi(int(input(\'Id du tournoi?\'))))',
                 'R': 'self.home()'}
        try:
            eval(dicto[option.upper()])
            time.sleep(3)
        except KeyError:
            print("Instruction non reconnue")
            time.sleep(3)
        self.report()
