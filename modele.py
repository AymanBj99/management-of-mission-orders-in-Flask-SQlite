from flask import Flask, request, session
from db import db


#User for connection
class User(db.Model):
    __tablename__ = 'users'
    idUser = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    

# Modèle pour le Personnel
class Personnel(db.Model):
    __tablename__ = 'personnels'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    mat = db.Column(db.String(20), unique=True, nullable=False)
    fonction = db.Column(db.String(50), nullable=False)
    direction = db.Column(db.String(50), nullable=False)
    cin = db.Column(db.String(20), unique=True, nullable=False)
    tel = db.Column(db.String(15), nullable=False)
    rib = db.Column(db.String(34), nullable=False)

    def __repr__(self):
        return f'<Personnel {self.nom} {self.prenom}>'


# Modèle pour la Voiture
class Voiture(db.Model):
    __tablename__ = 'voitures'
    
    id = db.Column(db.Integer, primary_key=True)
    matricule = db.Column(db.String(20), unique=True, nullable=False)
    marque = db.Column(db.String(50), nullable=False)
    chauffeur = db.Column(db.String(50), nullable=False)
    montant_gasoil = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Voiture {self.marque} ({self.matricule})>'


# Modèle pour le Projet
class Projet(db.Model):
    __tablename__ = 'projets'
    
    id = db.Column(db.Integer, primary_key=True)
    nom_projet = db.Column(db.String(100), nullable=False)
    chef_projet = db.Column(db.String(50), nullable=False)
    client = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Projet {self.nom_projet}>'


# Modèle pour la Mission
class Mission(db.Model):
    __tablename__ = 'missions'
    
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    personnel_id = db.Column(db.Integer, db.ForeignKey('personnels.id'), nullable=False)
    voiture_id = db.Column(db.Integer, db.ForeignKey('voitures.id'), nullable=False)
    projet_id = db.Column(db.Integer, db.ForeignKey('projets.id'), nullable=False)

    personnel = db.relationship('Personnel', backref='missions')
    voiture = db.relationship('Voiture', backref='missions')
    projet = db.relationship('Projet', backref='missions')

    def __repr__(self):
        return f'<Mission {self.titre} - {self.destination}>'
    

## Modèle pour les utilisateurs
class Utilisateur(db.Model):
    __tablename__ = 'utilisateurs'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    def __repr__(self):
        return f'<Utilisateur {self.username}>'
