from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from db import db

# Table User
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
    role = db.Column(db.String(50), nullable=False, default="user")

    # Relation avec les missions (responsable)
    missions_responsable = db.relationship('Mission', back_populates='responsable', lazy='dynamic')

    # Relation avec missions via la table de jointure
    missions = db.relationship('MissionUser', back_populates='user')


# Table Mission
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

    # Clé étrangère vers User pour le responsable
    responsable_id = db.Column(db.Integer, db.ForeignKey('user.idUser'), nullable=False)

    # Date d'enregistrement
    date_enregistrement = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relations
    responsable = db.relationship('User', foreign_keys=[responsable_id], back_populates='missions_responsable')
    users = db.relationship('MissionUser', back_populates='mission', cascade='all, delete-orphan')

    # Propriétés calculées
    @property
    def responsable_nom(self):
        # Récupère nom et prénom
        return f"{self.responsable.nom} {self.responsable.prenom}" if self.responsable else "N/A"

    @property
    def fonction_responsable(self):
        # Récupère la fonction
        return self.responsable.fonction if self.responsable else "N/A"

    @property
    def nombre_jours(self):
        # Calcul automatique du nombre de jours entre date_debut et date_fin
        if self.date_debut and self.date_fin:
            return (self.date_fin - self.date_debut).days
        return 0


# Table de jointure entre Mission et User
class MissionUser(db.Model):
    __tablename__ = 'mission_user'
    
    mission_id = db.Column(db.Integer, db.ForeignKey('mission.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.idUser'), primary_key=True)
    
    # Relations inversées
    mission = db.relationship('Mission', back_populates='users')
    user = db.relationship('User', back_populates='missions')
