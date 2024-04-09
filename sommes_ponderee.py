import pandas as pd

def normaliser_donnees(data, minimize_columns, maximize_columns):
    for col in data.columns:
        if col in minimize_columns:
            data[col] = (data[col].max() - data[col]) / (data[col].max() - data[col].min())
        elif col in maximize_columns:
            data[col] = (data[col] - data[col].min()) / (data[col].max() - data[col].min())
    return data

def calculer_score(data, weights):
    data['Score'] = sum(data[col] * weights[col] for col in weights.keys())
    return data

# Simuler les données chargées à partir de votre fichier
file_path = 'donnees.csv'
data = pd.read_csv(file_path)

minimize_columns = ['Prix', 'Dis_Freinage', 'Acceleration', 'Confort', 'Conso_Moy']
maximize_columns = ['Vitesse_Max', 'Vol_Coffre']

data = normaliser_donnees(data, minimize_columns, maximize_columns)

weights = {
    'Prix': 0.3,
    'Vitesse_Max': 0.2,
    'Conso_Moy': 0.1,
    'Dis_Freinage': 0.1,
    'Confort': 0.1,
    'Vol_Coffre': 0.15,
    'Acceleration': 0.05
}

assert sum(weights.values()) == 1, "La somme des poids doit être égale à 1"

data = calculer_score(data, weights)

data_sorted = data.sort_values(by='Score', ascending=False)
print(data_sorted[['Prix', 'Vitesse_Max', 'Conso_Moy', 'Dis_Freinage', 'Confort', 'Vol_Coffre', 'Acceleration', 'Score']])
