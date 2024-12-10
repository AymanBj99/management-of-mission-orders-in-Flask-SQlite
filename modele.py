from flask import Flask, request, session
from db import db
from datetime import datetime


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
    responsable_id = db.Column(db.Integer, db.ForeignKey('users.idUser'), nullable=False)  # Lié à User
    projet = db.Column(db.String(255), nullable=False)
    chef_de_projet = db.Column(db.String(255), nullable=False)
    date_enregistrement = db.Column(db.DateTime, default=datetime.utcnow)
    chauffeur = db.Column(db.String(255), nullable=False)
    marque_vehicule = db.Column(db.String(255), nullable=False)
    matricule_vehicule = db.Column(db.String(50), nullable=False)

    designation_travaux = db.Column(db.String(255), nullable=False)
    site_client = db.Column(db.String(255), nullable=False)
    ville_depart = db.Column(db.String(100), nullable=False)
    ville_arrivee = db.Column(db.String(100), nullable=False)
    date_debut = db.Column(db.Date, nullable=False)
    date_fin = db.Column(db.Date, nullable=False)
    recharge_gasoil = db.Column(db.Float, default=0.0)

    responsable = db.relationship("User", backref="missions", foreign_keys=[responsable_id])
    equipe = db.relationship("Equipe", back_populates="mission", cascade="all, delete-orphan")

    @property
    def nombre_jours(self):
        if self.date_debut and self.date_fin:
            return (self.date_fin - self.date_debut).days + 1
        return 0



class Equipe(db.Model):
    __tablename__ = 'equipes'
    id = db.Column(db.Integer, primary_key=True)
    mission_id = db.Column(db.Integer, db.ForeignKey('missions.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.idUser'), nullable=False)

    mission = db.relationship("Mission", back_populates="equipe")
    user = db.relationship("User")