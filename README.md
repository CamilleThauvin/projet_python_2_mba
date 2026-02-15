# 💳 Banking Transactions API - Analytics Platform

![CI/CD](https://github.com/CamilleThauvin/projet_python_2_mba/workflows/CI/CD%20Pipeline/badge.svg)
![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg)
![Coverage](https://img.shields.io/badge/coverage-84%25-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📊 Métriques du Projet

| Métrique | Valeur |
|----------|--------|
| **Transactions** | 13.3M+ |
| **Endpoints API** | 20+ |
| **Couverture Tests** | 84% |
| **Temps Réponse** | <100ms |
| **Type Conformité** | 100% PEP8 |
| **Tests Passing** | 120+ |

## 🚀 Vue d'Ensemble

API REST haute performance pour l'analyse de transactions bancaires, développée dans le cadre du projet Python MBA.

### 🎯 Caractéristiques Principales

- ⚡ **Performance Optimisée** : Cache LRU automatique, temps de réponse <100ms
- 📊 **Volume Massif** : Traite 13+ millions de transactions
- 🔍 **Détection de Fraude** : Système heuristique de détection
- 📈 **Analytics Avancées** : Statistiques quotidiennes, distribution, top clients
- 🎨 **Dashboard Streamlit** : Interface de visualisation interactive
- 🐳 **Containerisé** : Déploiement Docker + Docker Compose
- ✅ **CI/CD** : Pipeline automatisé avec GitHub Actions
- 📝 **100% Typé** : Validation Pydantic complète

## 🏗️ Architecture

```
banking_api/
├── models/          # Modèles Pydantic
├── routes/          # Endpoints FastAPI (5 routers)
├── services/        # Logique métier
└── main.py          # Application FastAPI

streamlit_app/       # Dashboard de visualisation
tests/               # Suite de tests pytest
tests_unittest/      # Tests unittest complémentaires
```

## 📡 API Endpoints

### 🔹 Transactions (`/api/transactions`)
- `GET /recent` - Transactions récentes
- `POST /search` - Recherche avancée
- `GET /{id}` - Détails d'une transaction
- `GET /by-customer/{id}` - Transactions par client
- `GET /to-customer/{id}` - Transactions vers un client

### 🔹 Clients (`/api/customers`)
- `GET /` - Liste paginée des clients
- `GET /top` - Top clients par activité
- `GET /{id}` - Profil client détaillé

### 🔹 Statistiques (`/api/stats`)
- `GET /overview` - Vue d'ensemble globale
- `GET /by-type` - Stats par type de transaction
- `GET /daily` - Évolution quotidienne
- `GET /amount-distribution` - Distribution des montants

### 🔹 Fraude (`/api/fraud`)
- `GET /summary` - Résumé de la détection
- `GET /by-type` - Taux de fraude par type
- `POST /check` - Vérifier une transaction

### 🔹 Système (`/api`)
- `GET /health` - État de santé
- `GET /info` - Informations système

## 🚀 Démarrage Rapide

### Avec Docker (Recommandé)

```bash
# Lancer l'API et le dashboard Streamlit
docker-compose up

# API disponible sur http://localhost:8000
# Streamlit sur http://localhost:8501
# Documentation sur http://localhost:8000/docs
```

### Installation Locale

```bash
# Cloner le repository
git clone https://github.com/CamilleThauvin/projet_python_2_mba.git
cd projet_python_2_mba

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'API
uvicorn banking_api.main:app --reload

# Dans un autre terminal, lancer Streamlit
streamlit run streamlit_app/app.py
```

## 🧪 Tests

```bash
# Lancer tous les tests
pytest

# Avec couverture
pytest --cov=banking_api --cov-report=html

# Tests unittest
python -m unittest discover tests_unittest

# Linting
flake8 banking_api/ tests/
black --check banking_api/
```

## 📦 Technologies

- **Framework**: FastAPI 0.115.0
- **Data Processing**: Pandas 2.2.0
- **Validation**: Pydantic 2.x
- **Tests**: Pytest 9.0.2, Unittest
- **Linting**: Flake8, Black, isort
- **Type Checking**: Mypy
- **Visualisation**: Streamlit, Plotly
- **Containerisation**: Docker, Docker Compose
- **CI/CD**: GitHub Actions

## 📈 Performance

- **Cache LRU** : Réduction de 95% des temps de chargement
- **Optimisations Pandas** : Opérations vectorisées
- **Pagination** : Limite max 1000 éléments par requête
- **Lazy Loading** : Chargement à la demande

## 🎨 Dashboard Streamlit

Interface interactive avec :
- Vue d'ensemble des transactions
- Analyse des clients
- Détection de fraude
- Statistiques détaillées
- Graphiques interactifs (Plotly)

## 👥 Auteurs

**Groupe MBA Big Data & AI**
- Camille Thauvin
- [Autres membres à ajouter]

## 📄 Licence

MIT License - voir [LICENSE](LICENSE)

## 🤝 Contribution

Ce projet a été développé dans le cadre du cours Python MBA. Les contributions sont les bienvenues via Pull Requests.

## 📚 Documentation

- [API Documentation](http://localhost:8000/docs) - Swagger UI
- [ReDoc](http://localhost:8000/redoc) - Alternative documentation
- [Installation Guide](INSTALL.md) - Guide d'installation détaillé

---

*Projet Python 2 - MBA Big Data & AI*
