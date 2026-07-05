from flask import Flask, render_template
from models import db, Departement, Formation, Actualite, Activite, Enseignant, Album

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ufr_sta.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ufr-sta-secret-key'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    actualites = Actualite.query.order_by(Actualite.date.desc()).limit(3).all()
    return render_template('index.html', actualites=actualites)

@app.route('/departements')
def departements():
    departements = Departement.query.all()
    return render_template('departements.html', departements=departements)

@app.route('/formations')
def formations():
    formations = Formation.query.all()
    return render_template('formations.html', formations=formations)

@app.route('/actualites')
def actualites():
    actualites = Actualite.query.order_by(Actualite.date.desc()).all()
    return render_template('actualites.html', actualites=actualites)

@app.route('/activites')
def activites():
    activites = Activite.query.order_by(Activite.date.desc()).all()
    return render_template('activités.html', activites=activites)

@app.route('/enseignants')
def enseignants():
    enseignants = Enseignant.query.all()
    return render_template('enseignants.html', enseignants=enseignants)

@app.route('/galerie')
def galerie():
    albums = Album.query.all()
    return render_template('galerie.html', albums=albums)

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)