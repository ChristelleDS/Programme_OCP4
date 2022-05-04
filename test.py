from itertools import combinations
from Controller import Controller


ctr = Controller()
liste = []
for j in ctr.get_liste_joueurs():
    liste.append(j.idjoueur)
combinaisons = combinations(liste,2)
for c in combinaisons:
    print(c)

if len(paires_tour) < nb_joueurs / 2:
    manquantes = int(nb_joueurs / 2 - len(paires_tour))
    print(str(manquantes) + " paires manquantes")
    combinaisons = combinations(liste_joueurs, 2)
    for m in range(0, manquantes - 1) \
             and p in combinaisons and p not in matchs_joues \
             and (p[1], p[0]) not in matchs_joues \
             and p not in paires_tour \
             and (p[1], p[0]) not in paires_tour:
        paires_tour.append(p)
        m = m + 1
else:
    pass

"""
combinaisons = combinations(liste_joueurs, 2)
for c in combinaisons and len(paires_tour) < nb_joueurs/2:
    if c in matchs_joues or c in paires_tour:
        continue
    else:
        paires_tour.append(c)
return paires_tour
"""








