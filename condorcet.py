import pandas as pd
import numpy as np

# Charger les données
data = pd.read_csv('donnees.csv')

# Spécification des critères à maximiser et à minimiser
minimize_columns = ['Prix', 'Dis_Freinage', 'Acceleration', 'Confort', 'Conso_Moy']
maximize_columns = ['Vitesse_Max', 'Vol_Coffre']

# Initialiser un dictionnaire pour enregistrer les détails des victoires
details_victoires = {}

# Fonction pour comparer deux alternatives pour un critère donné
def compare_alternatives(i, j, critere):
    if critere in minimize_columns:  # Moins c'est mieux
        return data.loc[i, critere] < data.loc[j, critere]
    else:  # Plus c'est mieux
        return data.loc[i, critere] > data.loc[j, critere]

n = len(data)
victoires = np.zeros((n, n))

# Comparer chaque paire d'alternatives pour chaque critère
for critere in data.columns[1:]:  # Exclure la première colonne si elle contient des labels d'alternatives
    for i in range(n):
        for j in range(i + 1, n):
            if compare_alternatives(i, j, critere):
                victoires[i, j] += 1
                details_victoires[(i, j)] = details_victoires.get((i, j), []) + [critere]
            elif compare_alternatives(j, i, critere):
                victoires[j, i] += 1
                details_victoires[(j, i)] = details_victoires.get((j, i), []) + [critere]

# Calculer le nombre total de victoires pour chaque alternative
total_victoires = np.sum(victoires > 0, axis=1) - np.sum(victoires > 0, axis=0)

# Identifier le vainqueur de Condorcet, si existant
vainqueur_condorcet = np.argmax(total_victoires) if np.all(total_victoires >= 0) else None

if vainqueur_condorcet is not None:
    print(f"Le vainqueur de Condorcet est l'alternative {vainqueur_condorcet} avec {total_victoires[vainqueur_condorcet]} victoires.")
else:
    print("Il n'y a pas de vainqueur de Condorcet clair dans cet ensemble de données.")

# Affichage des détails des victoires
for key, value in details_victoires.items():
    print(f"Alternative {key[0]} surclasse Alternative {key[1]} selon les critères: {', '.join(value)}.")
