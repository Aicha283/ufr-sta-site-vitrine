from flask import Flask, render_template, session, redirect, url_for, request, flash
from models import db, Departement, Formation, Actualite, Activite, Enseignant, Album, Admin
from werkzeug.security import generate_password_hash, check_password_hash
import functools

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ufr_sta.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ufr-sta-secret-key'

db.init_app(app)

with app.app_context():
    db.create_all()

# ===== DÉCORATEUR PROTECTION ADMIN =====
def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# ===== ROUTES PUBLIQUES =====
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
    return render_template('activites.html', activites=activites)

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

# ===== ROUTES ADMIN =====
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    erreur = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password, password):
            session['admin_id'] = admin.id
            return redirect(url_for('admin_dashboard'))
        else:
            erreur = "Identifiants incorrects"
    return render_template('admin/login.html', erreur=erreur)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_id', None)
    return redirect(url_for('home'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    return render_template('admin/dashboard.html')
# ===== CRUD ACTUALITÉS =====
@app.route('/admin/actualites')
@login_required
def admin_actualites():
    actualites = Actualite.query.order_by(Actualite.date.desc()).all()
    return render_template('admin/actualites.html', actualites=actualites)

@app.route('/admin/actualites/ajouter', methods=['GET', 'POST'])
@login_required
def admin_actualite_ajouter():
    if request.method == 'POST':
        from datetime import datetime
        nouvelle = Actualite(
            titre=request.form['titre'],
            date=datetime.strptime(request.form['date'], '%Y-%m-%d').date(),
            description=request.form['description']
        )
        db.session.add(nouvelle)
        db.session.commit()
        return redirect(url_for('admin_actualites'))
    return render_template('admin/actualite_form.html', titre_page="Ajouter une actualité", actu=None)

@app.route('/admin/actualites/modifier/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_actualite_modifier(id):
    actu = Actualite.query.get_or_404(id)
    if request.method == 'POST':
        from datetime import datetime
        actu.titre = request.form['titre']
        actu.date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        actu.description = request.form['description']
        db.session.commit()
        return redirect(url_for('admin_actualites'))
    return render_template('admin/actualite_form.html', titre_page="Modifier une actualité", actu=actu)

@app.route('/admin/actualites/supprimer/<int:id>')
@login_required
def admin_actualite_supprimer(id):
    actu = Actualite.query.get_or_404(id)
    db.session.delete(actu)
    db.session.commit()
    return redirect(url_for('admin_actualites'))

if __name__ == '__main__':
    app.run(debug=True)