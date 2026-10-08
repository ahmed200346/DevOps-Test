import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def prepare_data(filepath="Churn_Modelling.csv"):
    """Charger et prétraiter les données."""
    # Chargement
    df = pd.read_csv(filepath)
    
    # Suppression des colonnes inutiles pour le modèle
    df = df.drop(['RowNumber', 'CustomerId', 'Surname'], axis=1)
    
    # Encodage des variables catégorielles (Geography, Gender)
    df = pd.get_dummies(df, drop_first=True)
    
    # Séparation des caractéristiques (X) et de la cible (y)
    X = df.drop('Exited', axis=1)
    y = df['Exited']
    
    # Division en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Normalisation des données
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    return X_train, X_test, y_train, y_test
