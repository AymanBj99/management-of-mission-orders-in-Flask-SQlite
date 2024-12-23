from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from db import db

class User(db.Model):
    __tablename__ = 'user'
    
    idUser = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    nom = db.Column(db.String(255), nullable=False)
    prenom = db.Column(db.String(255), nullable=False)
    fonction = db.Column(db.String(255), nullable=False)
    direction = db.Column(db.String(255), nullable=False)
    cin = db.Column(db.String(255), unique=True, nullable=False)
    tel = db.Column(db.String(255), nullable=False)
    rib = db.Column(db.String(255), nullable=False)
    
    # Relation avec les missions via la table de jointure MissionUser
    missions = db.relationship('MissionUser', back_populates='user')

class Mission(db.Model):
    __tablename__ = 'mission'
    
    id = db.Column(db.Integer, primary_key=True)
    projet = db.Column(db.String(100), nullable=False)
    chef_de_projet = db.Column(db.String(100), nullable=False)
    chauffeur = db.Column(db.String(100), nullable=False)
    marque_vehicule = db.Column(db.String(50), nullable=False)
    matricule_vehicule = db.Column(db.String(20), nullable=False)
    designation_travaux = db.Column(db.String(200), nullable=False)
    site_client = db.Column(db.String(100), nullable=False)
    ville_depart = db.Column(db.String(50), nullable=False)
    ville_arrivee = db.Column(db.String(50), nullable=False)
    date_debut = db.Column(db.Date, nullable=False)
    date_fin = db.Column(db.Date, nullable=False)
    recharge_gasoil = db.Column(db.Float, nullable=False)
    responsable_id = db.Column(db.Integer, db.ForeignKey('user.idUser'), nullable=False)
    date_enregistrement = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc)) 
    
    # Relation avec les utilisateurs via la table de jointure MissionUser
    users = db.relationship('MissionUser', back_populates='mission')
    responsable = db.relationship('User', foreign_keys=[responsable_id])

    @property
    def fonction_responsable(self):
        return self.responsable.fonction if self.responsable else ""

    @property
    def nombre_jours(self):
        if self.date_debut and self.date_fin:
            return (self.date_fin - self.date_debut).days
        return 0

class MissionUser(db.Model):
    __tablename__ = 'mission_user'
    
    mission_id = db.Column(db.Integer, db.ForeignKey('mission.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.idUser'), primary_key=True)
    
    # Relations inversées
    mission = db.relationship('Mission', back_populates='users')
    user = db.relationship('User', back_populates='missions')
