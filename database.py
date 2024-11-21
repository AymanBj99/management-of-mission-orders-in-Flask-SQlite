from db import db
from modele import User
from admin import insert_admins  # Pas d'appels directs aux fonctions ici
from app import app  # Assure-toi d'importer l'application Flask

# Ouvre un contexte d'application
with app.app_context():
    # Recréer la base de données (cela supprimera les données actuelles)
    db.drop_all()
    db.create_all()

    # Ajoute des utilisateurs après avoir recréé la base de données
    insert_admins()
