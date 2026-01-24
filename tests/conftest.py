"""Configuration Pytest et fixtures partagées."""
import os
import pytest
import pandas as pd
from fastapi.testclient import TestClient
from banking_api.main import app


@pytest.fixture
def client(mock_csv_path) -> TestClient:
    """
    Fixture pour le client de test FastAPI.

    Parameters
    ----------
    mock_csv_path : str
        Mock du chemin CSV (appliqué automatiquement)

    Returns
    -------
    TestClient
        Client de test pour l'API
    """
    return TestClient(app)


@pytest.fixture
def sample_csv_path(tmp_path):
    """
    Crée un fichier CSV de test avec des données fictives.

    Parameters
    ----------
    tmp_path : Path
        Chemin temporaire fourni par pytest

    Returns
    -------
    str
        Chemin vers le fichier CSV de test
    """
    csv_path = tmp_path / "transactions_data.csv"

    # Données de test
    data = {
        'step': [1, 1, 2, 2, 3],
        'type': ['PAYMENT', 'TRANSFER', 'CASH_OUT', 'DEBIT', 'PAYMENT'],
        'amount': [9839.64, 181.00, 181.00, 52.95, 1234.56],
        'nameOrig': ['C1231006815', 'C1666544295', 'C1305486145', 'C840083671', 'C1231006815'],
        'oldbalanceOrg': [170136.00, 181.00, 181.00, 41720.00, 168902.36],
        'newbalanceOrig': [160296.36, 0.00, 0.00, 41667.05, 167667.80],
        'nameDest': ['M1979787155', 'C1900366749', 'C840083671', 'C1634788479', 'M1234567890'],
        'oldbalanceDest': [0.00, 0.00, 21182.00, 41898.00, 0.00],
        'newbalanceDest': [0.00, 0.00, 21182.00, 41950.95, 0.00],
        'isFraud': [0, 1, 0, 0, 0],
        'isFlaggedFraud': [0, 0, 0, 0, 0]
    }

    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)

    return str(csv_path)


@pytest.fixture
def mock_csv_path(monkeypatch, sample_csv_path):
    """
    Mock le chemin CSV pour utiliser le fichier de test.

    Parameters
    ----------
    monkeypatch : MonkeyPatch
        Fixture pytest pour le mocking
    sample_csv_path : str
        Chemin vers le CSV de test
    """
    def mock_get_csv_path():
        return sample_csv_path

    # Mock dans tous les services
    from banking_api.services import transactions_service, stats_service, fraud_detection_service, customer_service

    monkeypatch.setattr(transactions_service, '_get_csv_path', mock_get_csv_path)
    monkeypatch.setattr(stats_service, '_get_csv_path', mock_get_csv_path)
    monkeypatch.setattr(fraud_detection_service, '_get_csv_path', mock_get_csv_path)
    monkeypatch.setattr(customer_service, '_get_csv_path', mock_get_csv_path)

    return sample_csv_path
