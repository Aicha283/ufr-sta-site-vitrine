from app import app
from models import db, Activite
from datetime import date

with app.app_context():
    activite1 = Activite(
        titre="Atelier IA Générative",
        date=date(2026, 4, 15),
        lieu="Salle Informatique",
        organisateur="Département Informatique",
        description="Formation destinée aux étudiants de L3 sur l'utilisation de l'IA générative."
    )
    activite2 = Activite(
        titre="Hackathon UFR STA",
        date=date(2026, 5, 20),
        lieu="Amphithéâtre principal",
        organisateur="UFR STA",
        description="Compétition de programmation ouverte à tous les étudiants."
    )
    db.session.add(activite1)
    db.session.add(activite2)
    db.session.commit()
    print("✅ Activités ajoutées avec succès !")