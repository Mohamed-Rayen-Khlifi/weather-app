# 🌤️ Weather App - Projet Stage

## 📌 Description
Application web de collecte et d'analyse de données météo, développée en **Python** avec le framework **FastAPI**.

Un collecteur en arrière-plan interroge l'API **Open-Meteo** toutes les 10 minutes, stocke les mesures (température, humidité, vent, pression) dans une base **PostgreSQL**, puis les expose via une API REST et un tableau de bord web.

Ville suivie par défaut : **Tunis** (latitude `36.8065`, longitude `10.1815`).

## 🛠️ Technologies utilisées
- **Python 3.10+**
- **FastAPI** + **Uvicorn** (serveur ASGI)
- **SQLAlchemy 2.0** + **PostgreSQL** (`psycopg2`)
- **API Open-Meteo** (gratuite, sans clé API)
- **APScheduler** (collecte planifiée)
- **Pandas** / **NumPy** (détection d'anomalies)
- **Jinja2** + HTML/CSS/JS (tableau de bord)
- **Git & GitHub**

## ✨ Fonctionnalités
- Collecte automatique des mesures toutes les 10 minutes
- Stockage historique en base PostgreSQL
- API REST : dernière mesure, historique, prévision, détection d'anomalies
- Tableau de bord web responsive
- Journal des exécutions du collecteur (`collector_logs`)

## 📡 Endpoints de l'API
| Méthode | Route                   | Description                                              |
|---------|-------------------------|----------------------------------------------------------|
| `GET`   | `/`                     | Tableau de bord web                                      |
| `GET`   | `/health`               | Vérification d'état du service                           |
| `GET`   | `/measurements/latest`  | Dernière mesure enregistrée                              |
| `GET`   | `/measurements`         | Historique (`metric`, `from_date`, `to_date`, `limit`)  |
| `GET`   | `/forecast`             | Prévision simple par moyenne (`metric`, `n_points`)     |
| `GET`   | `/anomalies`            | Détection d'anomalies par z-score (`metric`, `threshold`) |

Métriques disponibles : `temperature`, `humidity`, `windspeed`, `pressure`.

## ✅ Prérequis
- Python 3.10 ou supérieur
- PostgreSQL 13+ installé et démarré
- Git

## 🚀 Installation

### 1. Cloner le dépôt
```bash
git clone https://github.com/rahmouni-arij/weather-app.git
cd weather-app
```

### 2. Créer et activer un environnement virtuel
```bash
python -m venv .venv
source .venv/bin/activate       # Linux / macOS
# .venv\Scripts\activate        # Windows (PowerShell)
```

### 3. Installer les dépendances
> Le code applicatif se trouve dans le sous-dossier `weather-app/`.
```bash
cd weather-app
pip install -r requirements.txt
```

### 4. Créer la base de données PostgreSQL
```bash
createdb weather_db
# ou dans psql :
# CREATE DATABASE weather_db;
```

### 5. Configurer les variables d'environnement
Créer un fichier `.env` dans le dossier `weather-app/` :
```env
DATABASE_URL=postgresql://postgres:admin123@localhost:5432/weather_db
SECRET_key=ma_clef_secrete_123456
```
> Adapter l'utilisateur, le mot de passe et le port selon votre installation PostgreSQL.
> L'API Open-Meteo ne nécessite **aucune clé**.

## ▶️ Exécution
Depuis le dossier `weather-app/` (celui qui contient `backend/`, `static/` et `templates/`) :
```bash
uvicorn backend.app.main:app --reload
```
Au démarrage, l'application :
1. crée automatiquement les tables (`measurements`, `collector_logs`) ;
2. lance une première collecte immédiate ;
3. planifie la collecte toutes les 10 minutes.

Ouvrir ensuite dans le navigateur :
- Tableau de bord : http://localhost:8000
- Documentation interactive (Swagger) : http://localhost:8000/docs
- État du service : http://localhost:8000/health

## 📂 Structure du projet
```
weather-app/
├── README.md
├── .gitignore
└── weather-app/
    ├── requirements.txt
    ├── backend/
    │   └── app/
    │       ├── main.py        # Application FastAPI + endpoints + scheduler
    │       ├── config.py      # Configuration (DB, API, ville)
    │       ├── database.py    # Moteur SQLAlchemy + session
    │       ├── models.py      # Modèles Measurement, CollectorLog
    │       └── collector.py   # Récupération et stockage des données Open-Meteo
    ├── templates/
    │   └── index.html         # Tableau de bord
    └── static/
        ├── script.js
        └── style.css
```
