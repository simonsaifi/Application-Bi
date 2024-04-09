import pandas as pd
import numpy as np

# Charger les données
data = pd.read_csv('donnees.csv')  # Assurez-vous que le chemin est correct

# Adapter les valeurs pour les critères à minimiser
minimize_columns = ['Prix', 'Dis_Freinage', 'Acceleration', 'Confort', 'Conso_Moy']
for col in minimize_columns:
    data[col] = data[col].max() - data[col] + data[col].min()

# Calculer les votes négatifs initiaux
votes_negatifs = pd.DataFrame(index=data.index)
for col in data.columns:
    votes_negatifs[col] = data[col].rank(method='min', ascending=True) == 1
votes_negatifs['Total'] = votes_negatifs.sum(axis=1)

# Boucle d'élimination avec enregistrement des détails
while len(data) > 1:
    max_votes_neg = votes_negatifs['Total'].max()
    alternatives_eliminees = votes_negatifs[votes_negatifs['Total'] == max_votes_neg].index
    
    # Afficher les détails de l'élimination
    for alt in alternatives_eliminees:
        crits = votes_negatifs.loc[alt, votes_negatifs.columns != 'Total']
        crits = crits.index[crits == 1].tolist()
        print(f"Alternative {alt} éliminée. Critères les plus impopulaires : {', '.join(crits)}")
    
    data.drop(alternatives_eliminees, inplace=True)
    votes_negatifs.drop(alternatives_eliminees, inplace=True)
    
    if len(data) == 1 or max_votes_neg == 0:
        break  # Arrêter si une seule alternative reste ou si aucune n'est clairement la plus impopulaire
    
    # Recalculer les votes négatifs pour les alternatives restantes
    for col in data.columns:
        votes_negatifs[col] = data[col].rank(method='min', ascending=True) == 1
    votes_negatifs['Total'] = votes_negatifs.sum(axis=1)

# Affichage de l'alternative restante
print("Alternative(s) la/les moins impopulaire(s) :", data.index.tolist())
