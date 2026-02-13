"""Configuration pytest et fixtures."""
import pytest
from fastapi.testclient import TestClient
from banking_api.main import app


@pytest.fixture
def client():
    """
    Fixture pour le client de test FastAPI.
    
    Permet de faire des requêtes HTTP à l'API sans la lancer.
    """
    return TestClient(app)


@pytest.fixture
def sample_fraud_data():
    """Données de test pour la prédiction de fraude."""
    return {
        "type": "Online Transaction",
        "amount": 15000.0,
        "merchant_city": "New York",
        "merchant_state": "NY"
    }


@pytest.fixture
def sample_normal_transaction():
    """Données de test pour une transaction normale."""
    return {
        "type": "Chip Transaction",
        "amount": 50.0,
        "merchant_city": "Paris",
        "merchant_state": "FR"
    }
