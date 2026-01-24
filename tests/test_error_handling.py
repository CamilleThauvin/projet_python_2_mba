"""Tests pour la gestion d'erreurs et les cas limites."""
import pytest
import os
from fastapi import HTTPException
from banking_api.services import transactions_service, stats_service, fraud_detection_service, customer_service


def test_transactions_service_missing_csv(monkeypatch):
    """Test quand le fichier CSV n'existe pas."""
    def mock_get_csv_path():
        return "/nonexistent/path/to/file.csv"

    monkeypatch.setattr(transactions_service, '_get_csv_path', mock_get_csv_path)

    with pytest.raises(HTTPException) as exc_info:
        transactions_service.get_paginated_transactions(page=1, limit=10)

    assert exc_info.value.status_code == 404
    assert "non trouvé" in exc_info.value.detail


def test_stats_service_missing_csv(monkeypatch):
    """Test stats avec CSV manquant."""
    def mock_get_csv_path():
        return "/nonexistent/path/to/file.csv"

    monkeypatch.setattr(stats_service, '_get_csv_path', mock_get_csv_path)

    with pytest.raises(HTTPException) as exc_info:
        stats_service.get_overview()

    assert exc_info.value.status_code == 404


def test_fraud_service_missing_csv(monkeypatch):
    """Test fraud avec CSV manquant."""
    def mock_get_csv_path():
        return "/nonexistent/path/to/file.csv"

    monkeypatch.setattr(fraud_detection_service, '_get_csv_path', mock_get_csv_path)

    with pytest.raises(HTTPException) as exc_info:
        fraud_detection_service.get_fraud_summary()

    assert exc_info.value.status_code == 404


def test_customer_service_missing_csv(monkeypatch):
    """Test customer avec CSV manquant."""
    def mock_get_csv_path():
        return "/nonexistent/path/to/file.csv"

    monkeypatch.setattr(customer_service, '_get_csv_path', mock_get_csv_path)

    with pytest.raises(HTTPException) as exc_info:
        customer_service.get_customers()

    assert exc_info.value.status_code == 404


def test_get_transaction_types_missing_csv(monkeypatch):
    """Test types avec CSV manquant."""
    def mock_get_csv_path():
        return "/nonexistent/path/to/file.csv"

    monkeypatch.setattr(transactions_service, '_get_csv_path', mock_get_csv_path)

    with pytest.raises(HTTPException) as exc_info:
        transactions_service.get_transaction_types()

    assert exc_info.value.status_code == 404


def test_get_recent_transactions_missing_csv(monkeypatch):
    """Test recent avec CSV manquant."""
    def mock_get_csv_path():
        return "/nonexistent/path/to/file.csv"

    monkeypatch.setattr(transactions_service, '_get_csv_path', mock_get_csv_path)

    with pytest.raises(HTTPException) as exc_info:
        transactions_service.get_recent_transactions()

    assert exc_info.value.status_code == 404


def test_search_transactions_missing_csv(monkeypatch):
    """Test search avec CSV manquant."""
    def mock_get_csv_path():
        return "/nonexistent/path/to/file.csv"

    monkeypatch.setattr(transactions_service, '_get_csv_path', mock_get_csv_path)

    with pytest.raises(HTTPException) as exc_info:
        transactions_service.search_transactions()

    assert exc_info.value.status_code == 404


def test_get_transactions_by_customer_missing_csv(monkeypatch):
    """Test by customer avec CSV manquant."""
    def mock_get_csv_path():
        return "/nonexistent/path/to/file.csv"

    monkeypatch.setattr(transactions_service, '_get_csv_path', mock_get_csv_path)

    with pytest.raises(HTTPException) as exc_info:
        transactions_service.get_transactions_by_customer('C123')

    assert exc_info.value.status_code == 404


def test_get_transactions_to_customer_missing_csv(monkeypatch):
    """Test to customer avec CSV manquant."""
    def mock_get_csv_path():
        return "/nonexistent/path/to/file.csv"

    monkeypatch.setattr(transactions_service, '_get_csv_path', mock_get_csv_path)

    with pytest.raises(HTTPException) as exc_info:
        transactions_service.get_transactions_to_customer('C123')

    assert exc_info.value.status_code == 404


def test_get_amount_distribution_missing_csv(monkeypatch):
    """Test distribution avec CSV manquant."""
    def mock_get_csv_path():
        return "/nonexistent/path/to/file.csv"

    monkeypatch.setattr(stats_service, '_get_csv_path', mock_get_csv_path)

    with pytest.raises(HTTPException) as exc_info:
        stats_service.get_amount_distribution()

    assert exc_info.value.status_code == 404


def test_get_stats_by_type_missing_csv(monkeypatch):
    """Test stats by type avec CSV manquant."""
    def mock_get_csv_path():
        return "/nonexistent/path/to/file.csv"

    monkeypatch.setattr(stats_service, '_get_csv_path', mock_get_csv_path)

    with pytest.raises(HTTPException) as exc_info:
        stats_service.get_stats_by_type()

    assert exc_info.value.status_code == 404


def test_get_daily_stats_missing_csv(monkeypatch):
    """Test daily stats avec CSV manquant."""
    def mock_get_csv_path():
        return "/nonexistent/path/to/file.csv"

    monkeypatch.setattr(stats_service, '_get_csv_path', mock_get_csv_path)

    with pytest.raises(HTTPException) as exc_info:
        stats_service.get_daily_stats()

    assert exc_info.value.status_code == 404


def test_get_fraud_by_type_missing_csv(monkeypatch):
    """Test fraud by type avec CSV manquant."""
    def mock_get_csv_path():
        return "/nonexistent/path/to/file.csv"

    monkeypatch.setattr(fraud_detection_service, '_get_csv_path', mock_get_csv_path)

    with pytest.raises(HTTPException) as exc_info:
        fraud_detection_service.get_fraud_by_type()

    assert exc_info.value.status_code == 404


def test_get_top_customers_missing_csv(monkeypatch):
    """Test top customers avec CSV manquant."""
    def mock_get_csv_path():
        return "/nonexistent/path/to/file.csv"

    monkeypatch.setattr(customer_service, '_get_csv_path', mock_get_csv_path)

    with pytest.raises(HTTPException) as exc_info:
        customer_service.get_top_customers()

    assert exc_info.value.status_code == 404
