import pandas as pd
import numpy as np

# Charger les données
data = pd.read_csv('donnees.csv')

# Spécification des critères à maximiser et à minimiser
minimize_columns = ['Prix', 'Dis_Freinage', 'Acceleration', 'Confort', 'Conso_Moy']
maximize_columns = ['Vitesse_Max', 'Vol_Coffre'] 

# Pour les critères à minimiser, convertir les valeurs de sorte que de plus petites valeurs deviennent de meilleures
for col in minimize_columns:
    data[col] = data[col].max() - data[col] + data[col].min()

# Initialiser le DataFrame pour les scores de Borda de chaque alternative
scores_borda = pd.DataFrame(0, index=data.index, columns=['Points de Borda'])

# Attribuer des points de Borda pour chaque critère
for critere in data.columns:
    # Classer les alternatives pour le critère actuel
    ranks = data[critere].rank(method='max', ascending=False)
    # Convertir les rangs en points de Borda
    scores_borda['Points de Borda'] += (len(data) - ranks)

# Calculer le score total de Borda pour chaque alternative
scores_borda['Score Total de Borda'] = scores_borda['Points de Borda']

# Classement final basé sur le score total de Borda
scores_borda['Classement Final'] = scores_borda['Score Total de Borda'].rank(method='min', ascending=False).astype(int)

# Affichage des résultats
print("Scores de Borda pour chaque alternative :\n", scores_borda[['Points de Borda', 'Score Total de Borda']])
print("\nClassement final basé sur les scores totaux de Borda :\n", scores_borda[['Score Total de Borda', 'Classement Final']].sort_values(by='Score Total de Borda', ascending=False))
