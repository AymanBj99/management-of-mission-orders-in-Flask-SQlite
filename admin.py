from flask import Flask, request, render_template, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from modele import User, Mission
from db import db

app = Flask(__name__)

# Insérer les administrateurs manuellement
def insert_admins():
    # Liste des administrateurs à insérer
    admins = [
        {'username': 'admin1', 'email': 'admin5@example.com', 'password_hash': generate_password_hash('password1')},
        {'username': 'admin2', 'email': 'admin4@example.com', 'password_hash': generate_password_hash('password2')}
    ]

    for admin in admins:
        # Vérifier si un utilisateur avec cet email existe déjà
        existing_user = User.query.filter_by(email=admin['email']).first()
        
        if existing_user:
            print(f"L'utilisateur avec l'email {admin['email']} existe déjà, il ne sera pas ajouté.")
        else:
            # Si l'utilisateur n'existe pas, l'ajouter
            new_admin = User(username=admin['username'], email=admin['email'], password_hash=admin['password_hash'])
            db.session.add(new_admin)

    try:
        db.session.commit()
        print("Les administrateurs ont été ajoutés avec succès.")
    except Exception as e:
        db.session.rollback()
        print(f"Une erreur est survenue lors de l'ajout des administrateurs : {e}")




