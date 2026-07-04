from app import app
from models import db, Departement, Formation, Module, Actualite, Activite, Enseignant, Album, Photo

with app.app_context():

    # ===== DÉPARTEMENTS =====
    dept_info = Departement(
        nom="Département Informatique",
        description="Département dédié aux sciences informatiques",
        responsable="Dr.Amadou Dahirou gueye",
        contact="info@ufr-sta.edu"
    )
    dept_math = Departement(
        nom="Département Mathématiques",
        description="Département des mathématiques pures et appliquées",
        responsable="Dr. thierno Sow",
        contact="math@ufr-sta.edu"
    )
    dept_phy = Departement(
        nom="Département physique",
        description="Département de physique pures et appliquées",
        responsable="Dr. Makha Ndaow",
        contact="phy@ufr-sta.edu"
    )
    db.session.add(dept_info)
    db.session.add(dept_math)
    db.session.add(dept_phy)
    db.session.commit()

    # ===== FORMATIONS =====
    licence_info = Formation(
        nom="Licence Informatique",
        niveau="Licence",
        duree="3 ans",
        conditions_admission="Baccalauréat série S ou équivalent",
        debouches="Développeur, Technicien réseau, Analyste , ingenieur en iot",
        departement_id=dept_info.id
    )
    licence_MATH = Formation(
        nom="Licence MATHEMATIQUE",
        niveau="Licence",
        duree="3 ans",
        conditions_admission="Baccalauréat série S ou équivalent",
        debouches="",
        departement_id=dept_math.id
    )
    licence_phy = Formation(
        nom="Licence PHYSIQUE",
        niveau="Licence",
        duree="3 ans",
        conditions_admission="Baccalauréat série S ou équivalent",
        debouches="",
        departement_id=dept_phy.id
    )
    master_info = Formation(
        nom="Master Informatique",
        niveau="Master",
        duree="2 ans",
        conditions_admission="Licence Informatique ou équivalent",
        debouches="Ingénieur logiciel, Chef de projet, Chercheur",
        departement_id=dept_info.id
    )
    master_MATH = Formation(
        nom="Master Informatique",
        niveau="Master",
        duree="2 ans",
        conditions_admission="Licence mathematique ou  ou équivalent",
        debouches="",
        departement_id=dept_math.id
    )
    master_phy = Formation(
        nom="Master physique",
        niveau="Master",
        duree="2 ans",
        conditions_admission="Licence physique ou équivalent",
        debouches="",
        departement_id=dept_info.id
    )
    db.session.add(licence_info)
    db.session.add(licence_MATH)
    db.session.add(licence_phy)
    db.session.add(master_info)
    db.session.add(master_MATH)
    db.session.add(master_phy)
    db.session.commit()

    # ===== MODULES =====
    db.session.add(Module(nom="Algorithmique", semestre=1, formation_id=licence_info.id))
    db.session.add(Module(nom="Python", semestre=1, formation_id=licence_info.id))
    db.session.add(Module(nom="cyber securite", semestre=1, formation_id=licence_info.id))
    db.session.add(Module(nom="POO", semestre=1, formation_id=licence_info.id))
    db.session.add(Module(nom="Base de données", semestre=1, formation_id=licence_info.id))
    db.session.add(Module(nom="Systeme des object connecte", semestre=2, formation_id=licence_info.id))
    db.session.add(Module(nom="data science", semestre=2, formation_id=licence_info.id))
    db.session.add(Module(nom="systeme resseaux", semestre=2, formation_id=licence_info.id))
    db.session.add(Module(nom="genie logiciel", semestre=2, formation_id=licence_info.id))
    db.session.add(Module(nom="developpement web", semestre=1, formation_id=licence_info.id))

    db.session.add(Module(nom="Algebre1", semestre=1, formation_id=licence_MATH.id))
    db.session.add(Module(nom="Analyse1", semestre=1, formation_id=licence_MATH.id))
    db.session.add(Module(nom="Analyse numerique matricielle", semestre=1, formation_id=licence_MATH.id))
    db.session.add(Module(nom="Algebre2", semestre=2, formation_id=licence_MATH.id))
    db.session.add(Module(nom="Analyse2", semestre=2, formation_id=licence_MATH.id))

    db.session.add(Module(nom="electricite", semestre=1, formation_id=licence_phy.id))
    db.session.add(Module(nom="optique numerique", semestre=1, formation_id=licence_phy.id))
    db.session.add(Module(nom="mecanique generale", semestre=2, formation_id=licence_phy.id))
    db.session.add(Module(nom="mecanique quantique", semestre=2, formation_id=licence_phy.id))
    db.session.commit()

    # ===== ACTUALITÉS =====
    from datetime import date
    db.session.add(Actualite(
        titre="Ouverture des inscriptions 2026-2027",
        date=date(2026, 7, 1),
        description="Les inscriptions pour l'année académique 2026-2027 sont ouvertes.",
        photo="default.jpg"
    ))
    db.session.add(Actualite(
        titre="Soutenance de thèse — Dr. DIENG",
        date=date(2026, 6, 15),
        description="Soutenance de thèse de doctorat en informatique.",
        photo="default.jpg"
    ))
    db.session.commit()

    # ===== ENSEIGNANTS =====
    db.session.add(Enseignant(
        nom="Dr. Amadou Dahirou Gueye",
        grade=" Professeur et Maître de Conférences",
        email="dahirou.gueye@uam.edu.sn",
        domaines_recherche="data science et java avance",
        photo="enseignant1.jpg",
        departement_id=dept_info.id
    ))
    db.session.add(Enseignant(
        nom="Dr. Lamine yade",
        grade=" Professeur ",
        email="lameyade9@gmail.com",
        domaines_recherche="developpement web",
        photo="enseignant2.jpg",
        departement_id=dept_info.id
    ))
    db.session.add(Enseignant(
        nom="Dr. Sada Anne",
        grade=" Professeur ",
        email="sada.anne@uabd.edu.sn",
        domaines_recherche="systeme resseaux",
        photo="enseignant3.jpg",
        departement_id=dept_info.id
    ))
    db.session.add(Enseignant(
        nom="Dr.  Sow",
        grade="Professeur Titulaire",
        email="a.sow@ufr-sta.edu",
        domaines_recherche="Algèbre",
        photo="enseignant4.jpg",
        departement_id=dept_math.id
    ))
    db.session.add(Enseignant(
        nom="Dr.  coulibaly",
        grade="Professeur Titulaire",
        email="a.sow@ufr-sta.edu",
        domaines_recherche=" Analyse",
        photo="enseignant5.jpg",
        departement_id=dept_math.id
    ))
    db.session.add(Enseignant(
        nom="Dr.  Sow",
        grade="Professeur Titulaire",
        email="a.sow@ufr-sta.edu",
        domaines_recherche="mecanique quantique",
        photo="enseignant6.jpg",
        departement_id=dept_phy.id
    ))
    db.session.commit()

    # ===== ALBUM ET PHOTOS =====
    album = Album(
        titre="Journée scientifique 2026",
        description="Photos de la journée scientifique annuelle",
        date=date(2026, 5, 10)
    )
    db.session.add(album)
    db.session.commit()

    db.session.add(Photo(chemin="photo1.jpg", album_id=album.id))
    db.session.add(Photo(chemin="photo2.jpg", album_id=album.id))
    db.session.commit()

    print("✅ Données de test insérées avec succès !")