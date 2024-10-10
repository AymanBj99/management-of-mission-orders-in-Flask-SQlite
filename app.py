from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDB.db'  # Remplacez par votre URI de base de données
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.secret_key = 'super secret key'

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
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        session['username']= request.form['username']
        session['password']= request.form['password']

        user = User.query.filter_by(username=session['username']).first()

        if user is None or not check_password_hash(user.password_hash, session['password']):
            error = 'Incorrect username or password. Please try again.'
        else:
            session['username'] = user.username
            return redirect(url_for('admin'))

    return render_template('login.html', error=error)




@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username =  request.form['username']
        email = request.form['email']
        password = request.form['password']


        # check if the user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user is None:
            password_hash = generate_password_hash(password)
            new_user = User(username=username,email=email, password_hash=password_hash)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))

        else:
            error = 'The username already exists. Please try again.'

    return render_template('register.html', error=error)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        # Logique pour ajouter une nouvelle mission
        titre = request.form['titre']
        destination = request.form['destination']
        personnel_id = request.form['personnel_id']
        voiture_id = request.form['voiture_id']
        projet_id = request.form['projet_id']

        new_mission = Mission(titre=titre, destination=destination, 
                              personnel_id=personnel_id, voiture_id=voiture_id, projet_id=projet_id)
        db.session.add(new_mission)
        db.session.commit()
        flash('Mission ajoutée avec succès !')
        return redirect(url_for('admin'))

    missions = Mission.query.all()
    personnels = Personnel.query.all()
    voitures = Voiture.query.all()
    projets = Projet.query.all()

    return render_template('admin.html', missions=missions, personnels=personnels, 
                           voitures=voitures, projets=projets)

# Exécution de la création des tables
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crée toutes les tables définies par les modèles
    app.run(debug=True)


