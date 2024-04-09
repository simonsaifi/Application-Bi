import pandas as pd
import numpy as np

def lire_donnees(filepath):
    return pd.read_csv(filepath)

def preference_linéaire(a, b, maximiser=True):
    if maximiser:
        return max(0, a - b)
    else:
        return max(0, b - a)

def construire_matrices_preference(data, weights, critere_direction):
    n = len(data)
    matrices = {critere: np.zeros((n, n)) for critere in weights}
    for critere, poids in weights.items():
        for i in range(n):
            for j in range(n):
                # Si le critère doit être maximisé, maximiser=True, sinon False
                matrices[critere][i, j] = preference_linéaire(data.iloc[i][critere], data.iloc[j][critere], 
                                                               maximiser=critere_direction.get(critere, True))
    return matrices

def calculer_flux(matrices_preference, weights, n):
    flux_positif = np.zeros(n)
    flux_negatif = np.zeros(n)
    for critere, matrice in matrices_preference.items():
        for i in range(n):
            for j in range(n):
                if i != j:
                    flux_positif[i] += matrice[i, j] * weights[critere]
                    flux_negatif[i] += matrice[j, i] * weights[critere]
    flux_positif /= (n - 1)
    flux_negatif /= (n - 1)
    return flux_positif, flux_negatif

def classer_alternatives(flux_positif, flux_negatif):
    flux_net = flux_positif - flux_negatif
    classements = np.argsort(-flux_net) + 1  # Ajouter 1 pour commencer le classement à 1
    return flux_net, classements

# Chemin vers le fichier de données
file_path = 'donnees.csv'
data = lire_donnees(file_path)

# Poids attribués à chaque critère
weights = {'Vitesse_Max': 0.2, 'Vol_Coffre': 0.3, 'Prix': 0.25, 'Conso_Moy': 0.15, 'Dis_Freinage': 0.1}

# Direction pour chaque critère : True pour maximiser, False pour minimiser
critere_direction = {'Vitesse_Max': True, 'Vol_Coffre': True, 'Prix': False, 'Conso_Moy': False, 'Dis_Freinage': False}

matrices_preference = construire_matrices_preference(data, weights, critere_direction)
flux_positif, flux_negatif = calculer_flux(matrices_preference, weights, len(data))
flux_net, classements = classer_alternatives(flux_positif, flux_negatif)

data['Flux_Net'] = flux_net
data['Classement'] = classements

data_sorted = data.sort_values(by='Classement')
print(data_sorted[['Prix', 'Vitesse_Max', 'Conso_Moy', 'Dis_Freinage', 'Confort', 'Vol_Coffre', 'Acceleration', 'Classement']])
