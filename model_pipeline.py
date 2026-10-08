# Importation du module de prétraitement des données
from data_processing import prepare_data

# Importation du module de gestion du modèle ML
from model import (
    train_model,
    evaluate_model,
    save_model,
    load_model
)

# Liste des fonctions exposées par la pipeline
__all__ = [
    'prepare_data',
    'train_model',
    'evaluate_model',
    'save_model',
    'load_model'
]
