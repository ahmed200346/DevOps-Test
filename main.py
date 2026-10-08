import argparse
from model_pipeline import (
    prepare_data,
    train_model,
    evaluate_model,
    save_model,
    load_model
)

def main():
    fichier_donnees = 'Churn_Modelling.csv'
    fichier_modele = 'modele_churn.pkl'

    parser = argparse.ArgumentParser(description="Pipeline MLOps - Modèle Churn")

    # Définition des options par nom de fonction
    parser.add_argument('--prepare', action='store_true', help="Exécuter uniquement la préparation des données")
    parser.add_argument('--train', action='store_true', help="Exécuter uniquement l'entraînement du modèle")
    parser.add_argument('--evaluate', action='store_true', help="Exécuter uniquement l'évaluation du modèle")
    parser.add_argument('--save', action='store_true', help="Exécuter uniquement la sauvegarde du modèle")
    parser.add_argument('--load', action='store_true', help="Exécuter uniquement le chargement du modèle")
    parser.add_argument('--all', action='store_true', help="Exécuter tout le pipeline")

    args = parser.parse_args()

    # Si aucune option n'est spécifiée, exécuter tout par défaut
    if not (args.prepare or args.train or args.evaluate or args.save or args.load or args.all):
        args.all = True

    if args.all:
        print("--- 1. Préparation des données ---")
        X_train, X_test, y_train, y_test = prepare_data(fichier_donnees)
        print("Données préparées avec succès.")
        
        print("\n--- 2. Entraînement du modèle ---")
        modele = train_model(X_train, y_train)
        print("Entraînement terminé.")
        
        print("\n--- 3. Évaluation du modèle ---")
        evaluate_model(modele, X_test, y_test)
        
        print("\n--- 4. Sauvegarde du modèle ---")
        save_model(modele, fichier_modele)
        
        print("\n--- 5. Test du chargement du modèle ---")
        modele_charge = load_model(fichier_modele)
        return

    if args.prepare:
        print("--- 1. Préparation des données ---")
        X_train, X_test, y_train, y_test = prepare_data(fichier_donnees)
        print("Données préparées avec succès.")

    if args.train:
        X_train, X_test, y_train, y_test = prepare_data(fichier_donnees)
        print("--- 2. Entraînement du modèle ---")
        modele = train_model(X_train, y_train)
        print("Entraînement terminé.")

    if args.evaluate:
        X_train, X_test, y_train, y_test = prepare_data(fichier_donnees)
        modele = train_model(X_train, y_train)
        print("--- 3. Évaluation du modèle ---")
        evaluate_model(modele, X_test, y_test)

    if args.save:
        X_train, X_test, y_train, y_test = prepare_data(fichier_donnees)
        modele = train_model(X_train, y_train)
        print("--- 4. Sauvegarde du modèle ---")
        save_model(modele, fichier_modele)

    if args.load:
        print("--- 5. Test du chargement du modèle ---")
        modele_charge = load_model(fichier_modele)

if __name__ == "__main__":
    main()
