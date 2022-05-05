
# Programme_OCP4

# Invite de commande : 
Se positionner dans le répertoire souhaité et y déposer les livrables

cd <répertoire>

# Création et activation de l'environnement virtuel
python -m venv env

#Windows:

env/Scripts/Activate.bat

#Autre:

source env/bin/activate

# Installation des modules requirements:
pip install -r requirements.txt

# Lancement du programme
python main.py

# Générer rapport d'erreurs Flake8:
# le fichier setup.cfg détaille les paramètres d'éxécution
 flake8
# le rapport html est disponible dans le répertoire flake-report(index)