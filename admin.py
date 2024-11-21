from flask import Flask, request, render_template, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from modele import User, Mission
from db import db

app = Flask(__name__)

from werkzeug.security import generate_password_hash

def insert_admins():
    # Liste des administrateurs à insérer avec les champs obligatoires
    admins = [
        {
            'username': 'admin1',
            'email': 'admin5@example.com',
            'password_hash': generate_password_hash('password1'),
            'nom': 'Admin',
            'prenom': 'One',
            'fonction': 'Responsable IT',
            'direction': 'Informatique',
            'cin': 'ABC123456',
            'tel': '0612345678',
            'rib': '9876543210'
        },
        {
            'username': 'admin2',
            'email': 'admin4@example.com',
            'password_hash': generate_password_hash('password2'),
            'nom': 'Admin',
            'prenom': 'Two',
            'fonction': 'Responsable RH',
            'direction': 'Ressources Humaines',
            'cin': 'DEF789012',
            'tel': '0612345679',
            'rib': '1234567890'
        }
    ]

    for admin in admins:
        # Vérifier si un utilisateur avec cet email existe déjà
        existing_user = User.query.filter_by(email=admin['email']).first()
        
        if existing_user:
            print(f"L'utilisateur avec l'email {admin['email']} existe déjà, il ne sera pas ajouté.")
        else:
            # Si l'utilisateur n'existe pas, l'ajouter avec tous les champs requis
            new_admin = User(
                username=admin['username'],
                email=admin['email'],
                password_hash=admin['password_hash'],
                nom=admin['nom'],
                prenom=admin['prenom'],
                fonction=admin['fonction'],
                direction=admin['direction'],
                cin=admin['cin'],
                tel=admin['tel'],
                rib=admin['rib']
            )
            db.session.add(new_admin)

    try:
        db.session.commit()
        print("Les administrateurs ont été ajoutés avec succès.")
    except Exception as e:
        db.session.rollback()
        print(f"Une erreur est survenue lors de l'ajout des administrateurs : {e}")
