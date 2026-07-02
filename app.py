from flask import Flask
from models import db

app = Flask(__name__)

# Configuration de la base de données SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ufr_sta.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ufr-sta-secret-key'

# Initialiser la base de données avec l'application
db.init_app(app)

# Créer toutes les tables au démarrage
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "Bienvenue sur le site de l'UFR STA"

if __name__ == '__main__':
    app.run(debug=True)