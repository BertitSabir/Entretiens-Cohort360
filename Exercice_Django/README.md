Exercice Django — API REST Patients, Médicaments & Prescriptions

Présentation
------------
Projet Django + Django REST Framework pour gérer des Patients, des Médicaments
et des Prescriptions médicamenteuses.

L'exercice consiste à implémenter la ressource Prescription — voir [Issue-Prescriptions-001.md](Issue-Prescriptions-001.md).


Prérequis
---------
Python 3.10. Il est recommandé d'utiliser [pyenv](https://github.com/pyenv/pyenv) pour gérer la version Python.

```bash
# Installation de pyenv (si pas déjà installé)
brew install pyenv           # macOS
# ou voir https://github.com/pyenv/pyenv#installation pour Linux

pyenv install 3.10.14
pyenv local 3.10.14
```


Installation
------------

```bash
make install    # crée le venv et installe les dépendances dev
make migrate    # applique les migrations
make seed       # génère les données de démonstration
make run        # lance le serveur sur http://127.0.0.1:8000
```


Tests
-----

```bash
make test       # lance les tests
make coverage   # tests + rapport de couverture (seuil 80%)
```


Endpoints
---------

```
GET  /Patient       — liste des patients
GET  /Medication    — liste des médicaments

GET    /Prescription
POST   /Prescription
GET    /Prescription/{id}
PATCH  /Prescription/{id}
PUT    /Prescription/{id}
```

Filtres disponibles sur `/Prescription` :

| Paramètre | Description |
|---|---|
| `patient` | ID du patient |
| `medicament` | ID du médicament |
| `status` | `valide` · `en_attente` · `suppr` |
| `date_debut` | date de début exacte |
| `date_debut__apres` | date de début >= |
| `date_debut__avant` | date de début <= |
| `date_fin` | date de fin exacte |
| `date_fin__apres` | date de fin >= |
| `date_fin__avant` | date de fin <= |

Les filtres peuvent être combinés.


Exemples
--------

```bash
curl "http://127.0.0.1:8000/Patient?nom=Martin"
curl "http://127.0.0.1:8000/Medication?status=actif"
curl "http://127.0.0.1:8000/Prescription?status=valide&date_debut__apres=2024-01-01"
curl "http://127.0.0.1:8000/Prescription?patient=1&medicament=3"
```
