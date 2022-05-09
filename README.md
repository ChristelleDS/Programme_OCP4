
# Programme_OCP4

# Invite de commande :

Se positionner dans le répertoire souhaité et y déposer les livrables


# Création et activation de l'environnement virtuel

python -m venv env

# pour Windows:

env/Scripts/Activate.bat

# pour autre système d'exploitation:

source env/bin/activate

# Installation des modules requirements:

pip install -r requirements.txt

# Lancement du programme

python main.py

# Etapes du programme pour gestion du tournoi:
- créer un tournoi
- inscrire les joueurs
- démarrer un tour
- enregistrer les resultats du tour
- démarrer le tour suivant etc...
- en cas de génération incomplète des paires, possibilité de créer manuellement un match
- terminer le tournoi
- accéder aux reports

# Générer rapport d'erreurs Flake8:

flake8

- le fichier setup.cfg détaille les paramètres d'éxécution
- le rapport html est disponible dans le répertoire flake-report(index)
