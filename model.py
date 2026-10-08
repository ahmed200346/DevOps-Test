from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

def train_model(X_train, y_train):
    """Entraîner le modèle."""
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    """Évaluer les performances."""
    y_pred = model.predict(X_test)
    print("Précision (Accuracy) :", accuracy_score(y_test, y_pred))
    print("\nRapport de classification :\n", classification_report(y_test, y_pred))

def save_model(model, filename="modele_churn.pkl"):
    """Sauvegarder le modèle entraîné."""
    joblib.dump(model, filename)
    print(f"Modèle sauvegardé avec succès sous le nom : {filename}")

def load_model(filename="modele_churn.pkl"):
    """Charger un modèle sauvegardé."""
    model = joblib.load(filename)
    print(f"Modèle '{filename}' chargé avec succès.")
    return model
