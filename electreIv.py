import pandas as pd
import numpy as np

# Charger les données
data = pd.read_csv('donnees.csv')

# Spécification des critères à maximiser et à minimiser
minimize_columns = ['Prix', 'Dis_Freinage', 'Acceleration', 'Confort', 'Conso_Moy']
maximize_columns = ['Vitesse_Max', 'Vol_Coffre']

# Calcul de la matrice de concordance et capture des critères de concordance
def calcule_concordance(df, minimize_columns, maximize_columns):
    n = len(df)
    concordance = np.zeros((n, n))
    concordance_details = {}
    for i in range(n):
        for j in range(n):
            score = 0
            details = []
            for critere in df.columns:
                if critere in maximize_columns and df.iloc[i][critere] >= df.iloc[j][critere]:
                    score += 1
                    details.append(critere)
                elif critere in minimize_columns and df.iloc[i][critere] <= df.iloc[j][critere]:
                    score += 1
                    details.append(critere)
            concordance[i, j] = score / len(df.columns)
            concordance_details[(i, j)] = details
    return concordance, concordance_details

# Calcul de la matrice de discordance et capture des critères de discordance
def calcule_discordance(df, minimize_columns, maximize_columns):
    n = len(df)
    discordance = np.zeros((n, n))
    discordance_details = {}
    for i in range(n):
        for j in range(n):
            discordances = []
            details = {}
            for critere in df.columns:
                diff = df.iloc[j][critere] - df.iloc[i][critere] if critere in maximize_columns else df.iloc[i][critere] - df.iloc[j][critere]
                if max(0, diff) > 0:  # Ne considère que les discordances positives
                    discordances.append(diff)
                    details[critere] = diff
            discordance[i, j] = max(discordances) if discordances else 0
            discordance_details[(i, j)] = details
    discordance_max = discordance.max() if discordance.max() > 0 else 1  # Évite la division par zéro
    return discordance / discordance_max, discordance_details  # Normalisation

# Application des seuils pour le surclassement et enregistrement des détails
def applique_seuils(concordance, discordance, concordance_details, discordance_details, seuil_concordance=0.5, seuil_discordance=0.5):
    n = concordance.shape[0]
    surclassement = np.zeros((n, n))
    surclassement_details = {}
    for i in range(n):
        for j in range(n):
            if i != j:
                if concordance[i, j] > seuil_concordance and discordance[i, j] < seuil_discordance:
                    surclassement[i, j] = 1
                    surclassement_details[(i, j)] = {
                        'concordance': concordance_details[(i, j)],
                        'discordance': discordance_details[(i, j)]
                    }
    return surclassement, surclassement_details

# Analyse du graphe de surclassement pour déterminer un classement basé sur les scores de surclassement
def analyse_surclassement(surclassement):
    scores = np.sum(surclassement, axis=1) - np.sum(surclassement, axis=0)
    classement = np.argsort(-scores)
    return classement, scores

# Exécution
concordance, concordance_details = calcule_concordance(data, minimize_columns, maximize_columns)
discordance, discordance_details = calcule_discordance(data, minimize_columns, maximize_columns)
surclassement, surclassement_details = applique_seuils(concordance, discordance, concordance_details, discordance_details, 0.5, 0.5)
classement, scores = analyse_surclassement(surclassement)

# Affichage des résultats
print("Classement des alternatives :", classement)
print("Scores de surclassement :", scores)

i, j = 0, 1
if (i, j) in surclassement_details:
    print(f"Détails de surclassement pour {i} surclassant {j}:")
    print("Critères de concordance:", surclassement_details[(i, j)]['concordance'])
    print("Critères contribuant à la discordance:", surclassement_details[(i, j)]['discordance'])
else:
    print(f"Pas de surclassement direct de {i} sur {j}.")