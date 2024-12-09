from flask import Flask, request, session
from db import db


#User for connection
class User(db.Model):
    __tablename__ = 'users'
    idUser = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    fonction = db.Column(db.String(50), nullable=False)
    direction = db.Column(db.String(50), nullable=False)
    cin = db.Column(db.String(40), unique=True, nullable=False)
    tel = db.Column(db.String(20), nullable=False)
    rib = db.Column(db.String(34), nullable=False)

    def __repr__(self):
        return f'<User {self.nom} {self.prenom}>'
        



class Mission(db.Model):
    __tablename__ = 'missions'
    
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(100), nullable=False)
    date_depart = db.Column(db.Date, nullable=False)
    date_retour = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.idUser'), nullable=False)

    # Attributs de l'ancienne table Transport
    matricule = db.Column(db.String(20), unique=True, nullable=False)
    marque = db.Column(db.String(50), nullable=False)
    chauffeur = db.Column(db.String(50), nullable=False)
    montant_gasoil = db.Column(db.Float, nullable=False)

    # Attributs de l'ancienne table Projet
    nom_projet = db.Column(db.String(100), nullable=False)
    chef_projet = db.Column(db.String(50), nullable=False)
    etat = db.Column(db.String(50), nullable=False, default="En attente")
    # Relations
    user = db.relationship('User', backref='missions')

    def __repr__(self):
        return f'<Mission {self.titre} - {self.destination} - {self.etat}>'



