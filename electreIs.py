import pandas as pd
import numpy as np

# Charger les données
data = pd.read_csv('donnees.csv')  # Modifiez le chemin selon votre emplacement de fichier

# Spécification des critères à maximiser et à minimiser
minimize_columns = ['Prix', 'Dis_Freinage', 'Acceleration', 'Confort', 'Conso_Moy']
maximize_columns = ['Vitesse_Max', 'Vol_Coffre']

# Définir les seuils de veto pour chaque critère (exemple)
seuil_veto = {'Conso_Moy': 5, 'Dis_Freinage': 4}

# Calcul de la matrice de concordance, enregistrant les critères contribuant
def calcule_concordance(df):
    n = len(df)
    concordance = np.zeros((n, n))
    concordance_details = {}
    for i in range(n):
        for j in range(n):
            details = []
            for critere in df.columns:
                if critere in maximize_columns and df.iloc[i][critere] >= df.iloc[j][critere]:
                    details.append(critere)
                elif critere in minimize_columns and df.iloc[i][critere] <= df.iloc[j][critere]:
                    details.append(critere)
            concordance[i, j] = len(details) / len(df.columns)
            concordance_details[(i, j)] = details
    return concordance, concordance_details

# Calcul de la matrice de discordance, enregistrant les critères contribuant
def calcule_discordance(df):
    n = len(df)
    discordance = np.zeros((n, n))
    discordance_details = {}
    for i in range(n):
        for j in range(n):
            max_discordance = 0
            max_critere = None
            for critere in df.columns:
                diff = abs(df.iloc[j][critere] - df.iloc[i][critere])
                if diff > max_discordance:
                    max_discordance = diff
                    max_critere = critere
            discordance[i, j] = max_discordance
            discordance_details[(i, j)] = {max_critere: max_discordance} if max_critere else {}
    discordance_max = discordance.max() if discordance.max() > 0 else 1
    return discordance / discordance_max, discordance_details  # Normalisation

# Application des seuils et vérification des vetos, avec enregistrement des détails
def applique_seuils_et_veto(concordance, discordance, concordance_details, discordance_details, seuil_concordance=0.5, seuil_discordance=0.5):
    n = concordance.shape[0]
    surclassement = np.zeros((n, n))
    surclassement_details = {}
    for i in range(n):
        for j in range(n):
            if concordance[i, j] > seuil_concordance and discordance[i, j] < seuil_discordance:
                veto_applique = False
                veto_details = {}
                for critere, diff in discordance_details[(i, j)].items():
                    if diff > seuil_veto.get(critere, float('inf')):
                        veto_applique = True
                        veto_details[critere] = diff
                        break
                if not veto_applique:
                    surclassement[i, j] = 1
                    surclassement_details[(i, j)] = {
                        'concordance': concordance_details[(i, j)],
                        'discordance': discordance_details[(i, j)],
                        'veto': veto_details
                    }
    return surclassement, surclassement_details

# Analyse du graphe de surclassement pour déterminer le classement
def analyse_surclassement(surclassement):
    scores = np.sum(surclassement, axis=1) - np.sum(surclassement, axis=0)
    classement = np.argsort(-scores)
    return classement, scores

# Exécution de la méthode ELECTRE Is
concordance, concordance_details = calcule_concordance(data)
discordance, discordance_details = calcule_discordance(data)
surclassement, surclassement_details = applique_seuils_et_veto(concordance, discordance, concordance_details, discordance_details, 0.5, 0.5)
classement, scores = analyse_surclassement(surclassement)

# Affichage des résultats
print("Classement des alternatives :", classement)
print("Scores de surclassement :", scores)

# Affichage détaillé des raisons de surclassement pour chaque paire d'alternatives
for key, value in surclassement_details.items():
    i, j = key
    if surclassement[i, j] == 1:
        print(f"\nAlternative {i} surclasse Alternative {j} parce que :")
        print("  - Critères de Concordance:", value['concordance'])
        if value['discordance']:
            print("  - Discordance la plus élevée sur le critère:", value['discordance'])
        if value.get('veto'):
            print("  - Un veto a été appliqué en raison de:", value['veto'])