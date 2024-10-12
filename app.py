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
    

## Modèle pour les utilisateurs
class Utilisateur(db.Model):
    __tablename__ = 'utilisateurs'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    def __repr__(self):
        return f'<Utilisateur {self.username}>'

    

# Route de connexion
@app.route('/')
def index():
    if 'username' in session:
        # Récupérer l'utilisateur connecté
        username = session['username']
        user = User.query.filter_by(username=username).first()

        # Vérifier si l'utilisateur est un admin (ici, on compare avec des admins définis manuellement)
        admin_users = ['admin1', 'admin2']  # Liste des utilisateurs admins définis manuellement

        if user and username in admin_users:
            # Si c'est un admin, rediriger vers l'interface admin
            return redirect(url_for('admin'))
        elif user:
            # Si c'est un employé, rediriger vers l'interface employé
            return redirect(url_for('employee'))
        else:
            flash('Utilisateur non trouvé', 'error')
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Récupérer l'utilisateur par son nom d'utilisateur
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['username'] = user.username
            flash('Connexion réussie', 'success')
            return redirect(url_for('index'))  # Rediriger vers la page d'accueil après connexion
        else:
            flash('Nom d\'utilisateur ou mot de passe invalide', 'error')
    
    return render_template('login.html')  # Afficher le formulaire de connexion


# Route d'inscription
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Vérifier si l'utilisateur existe déjà
        existing_user = User.query.filter_by(username=username).first()

        if existing_user is None:
            # Hachage du mot de passe
            password_hash = generate_password_hash(password)
            # Créer un nouvel utilisateur
            new_user = User(username=username, email=email, password_hash=password_hash)
            db.session.add(new_user)
            db.session.commit()
            flash('Inscription réussie, vous pouvez vous connecter', 'success')
            return redirect(url_for('login'))
        else:
            flash('Le nom d\'utilisateur existe déjà, veuillez en choisir un autre', 'error')

    return render_template('register.html')


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


@app.route('/admin', methods=['GET'])
def admin():
    missions = Mission.query.all()  # Récupérez toutes les missions de la base de données
    return render_template('admin.html', missions=missions)




@app.route('/employee', methods=['GET'])
def employee():
    missions = Mission.query.all()  # Récupérez toutes les missions de la base de données
    return render_template('employee.html', missions=missions)


# Exécution de la création des tables
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        insert_admins() 
    app.run(debug=True)
