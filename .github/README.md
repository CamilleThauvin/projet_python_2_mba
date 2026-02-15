# 🏦 Banking Transactions API

##  Application Web Streamlit

Interface web métier développée séparément.

📦 **Repository Streamlit** : [banking-api-streamlit](https://github.com/payebie/banking-api-streamlit)

# CI/CD Configuration

Ce dossier contient les workflows GitHub Actions pour automatiser les tests, la qualité du code et le déploiement.

## 📋 Workflows disponibles

### 1. `tests.yml` - Tests automatisés
**Déclenché sur** : Push et Pull Request sur `main`, `develop`, et branches `feature/*`

**Actions** :
- ✅ Installation de Python 3.11
- ✅ Cache des dépendances pip
- ✅ Installation des requirements
- ✅ Linting avec flake8
- ✅ Exécution des tests avec pytest
- ✅ Génération du rapport de couverture
- ✅ Upload du rapport de couverture en artifact

**Commande équivalente locale** :
```bash
pytest tests/ -v --cov=banking_api --cov-report=html
```

---

### 2. `lint.yml` - Qualité du code
**Déclenché sur** : Push et Pull Request sur `main`, `develop`, et branches `feature/*`

**Actions** :
- ✅ Vérification du formatage avec Black
- ✅ Vérification du tri des imports avec isort
- ✅ Linting avec flake8
- ✅ Vérification de types avec mypy

**Commandes équivalentes locales** :
```bash
black --check banking_api/
isort --check-only banking_api/
flake8 banking_api/
mypy banking_api --ignore-missing-imports
```

---

### 3. `deploy.yml` - Déploiement
**Déclenché sur** : Push sur `main` ou création d'un tag `v*`

**Actions** :
- ✅ Tests avant déploiement
- ✅ Build Docker (optionnel)
- ✅ Notification de déploiement

---

## 🚀 Comment ça marche ?

### Workflow de développement

1. **Créer une branche feature**
   ```bash
   git checkout -b feature/ma-nouvelle-fonctionnalite
   ```

2. **Développer et tester localement**
   ```bash
   pytest tests/
   ```

3. **Push la branche**
   ```bash
   git push origin feature/ma-nouvelle-fonctionnalite
   ```

4. **GitHub Actions s'exécute automatiquement**
   - Tests sur la branche feature
   - Linting du code
   - Résultats visibles dans l'onglet "Actions"

5. **Créer une Pull Request**
   - Les checks doivent passer avant merge
   - Revue de code par l'équipe

6. **Merge vers main**
   - Tests re-exécutés
   - Déploiement automatique (si configuré)

---

## 📊 Badges de statut

Ajouter ces badges dans votre README.md principal :

```markdown
![Tests](https://github.com/VOTRE-USERNAME/projet_python_2_mba/workflows/Tests/badge.svg)
![Code Quality](https://github.com/VOTRE-USERNAME/projet_python_2_mba/workflows/Code%20Quality/badge.svg)
```

---

## 🔧 Configuration

### Variables d'environnement (secrets)

Si vous avez besoin de secrets (API keys, tokens, etc.) :

1. Aller dans Settings > Secrets and variables > Actions
2. Ajouter vos secrets
3. Les utiliser dans les workflows :
   ```yaml
   env:
     API_KEY: ${{ secrets.API_KEY }}
   ```

### Cache des dépendances

Le cache pip est configuré pour accélérer les builds :
```yaml
- uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
```

---

## 📈 Rapport de couverture

Après chaque exécution de tests, un rapport de couverture HTML est généré et disponible dans les artifacts :

1. Aller dans Actions > Workflow exécuté
2. Télécharger "coverage-report"
3. Ouvrir `htmlcov/index.html` dans un navigateur

---

## ⚙️ Personnalisation

### Modifier les branches surveillées

Dans `tests.yml` et `lint.yml`, modifier :
```yaml
on:
  push:
    branches: [ main, develop, feature/* ]  # ← Ajouter/retirer des branches
```

### Ajouter d'autres versions de Python

Dans `tests.yml`, modifier :
```yaml
strategy:
  matrix:
    python-version: ["3.10", "3.11", "3.12"]  # ← Tester plusieurs versions
```

### Désactiver un workflow

Renommer le fichier avec l'extension `.yml.disabled` :
```bash
mv .github/workflows/deploy.yml .github/workflows/deploy.yml.disabled
```

---

## 🆘 Dépannage

### Les tests échouent sur GitHub mais passent localement

**Cause** : Différence d'environnement

**Solutions** :
1. Vérifier que `requirements.txt` contient toutes les dépendances
2. Ajouter `PYTHONPATH` dans le workflow :
   ```yaml
   env:
     PYTHONPATH: ${{ github.workspace }}
   ```

### Le workflow ne se déclenche pas

**Causes possibles** :
1. Le fichier YAML a une erreur de syntaxe
2. La branche ne correspond pas aux patterns configurés
3. Le workflow est désactivé dans Settings > Actions

**Solution** :
```bash
# Valider la syntaxe YAML
yamllint .github/workflows/tests.yml
```

### Timeout sur les tests

**Cause** : Les tests prennent trop de temps (chargement du CSV)

**Solution** : Ajouter un timeout :
```yaml
- name: Run tests
  timeout-minutes: 10  # ← Augmenter si nécessaire
  run: pytest tests/
```

---

## 📚 Ressources

- [Documentation GitHub Actions](https://docs.github.com/actions)
- [Marketplace GitHub Actions](https://github.com/marketplace?type=actions)
- [Pytest Documentation](https://docs.pytest.org/)
- [Black Code Formatter](https://black.readthedocs.io/)

---

**Note** : Ces workflows sont configurés pour tourner sur Ubuntu. Pour Windows ou macOS, modifier `runs-on` dans les fichiers YAML.
