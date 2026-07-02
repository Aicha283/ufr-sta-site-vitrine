from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Departement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    responsable = db.Column(db.String(100))
    contact = db.Column(db.String(100))
    formations = db.relationship('Formation', backref='departement', lazy=True)
    enseignants = db.relationship('Enseignant', backref='departement', lazy=True)

class Formation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(150), nullable=False)
    niveau = db.Column(db.String(50))
    duree = db.Column(db.String(50))
    conditions_admission = db.Column(db.Text)
    debouches = db.Column(db.Text)
    departement_id = db.Column(db.Integer, db.ForeignKey('departement.id'), nullable=False)
    modules = db.relationship('Module', backref='formation', lazy=True)

class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(150), nullable=False)
    semestre = db.Column(db.Integer)
    formation_id = db.Column(db.Integer, db.ForeignKey('formation.id'), nullable=False)

class Actualite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text)
    photo = db.Column(db.String(200))

class Activite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    lieu = db.Column(db.String(150))
    organisateur = db.Column(db.String(150))
    description = db.Column(db.Text)
    photos = db.relationship('Photo', backref='activite', lazy=True)

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.Date)
    photos = db.relationship('Photo', backref='album', lazy=True)

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chemin = db.Column(db.String(200), nullable=False)
    activite_id = db.Column(db.Integer, db.ForeignKey('activite.id'), nullable=True)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=True)

class Enseignant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.String(100))
    email = db.Column(db.String(150))
    domaines_recherche = db.Column(db.Text)
    photo = db.Column(db.String(200))
    departement_id = db.Column(db.Integer, db.ForeignKey('departement.id'), nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    sujet = db.Column(db.String(200))
    contenu = db.Column(db.Text, nullable=False)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)