import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
def prepare_data(filepath="Churn_Modelling.csv"):
    df = pd.read_csv(filepath)
    df = df.drop(['RowNumber', 'CustomerId', 'Surname'], axis=1)
    df = pd.get_dummies(df, drop_first=True)

    X = df.drop('Exited', axis=1)
    y = df['Exited']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Sauvegarde du scaler + des colonnes attendues (ordre important !)
    joblib.dump(scaler, "scaler.pkl")
    joblib.dump(list(X.columns), "colonnes.pkl")

    return X_train, X_test, y_train, y_test
