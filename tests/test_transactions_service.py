"""Tests pour le service de gestion des transactions."""
import pytest
from banking_api.services import transactions_service


def test_get_paginated_transactions(mock_csv_path):
    """Test de la pagination des transactions."""
    result = transactions_service.get_paginated_transactions(page=1, limit=2)

    assert result['page'] == 1
    assert result['limit'] == 2
    assert result['total'] == 5
    assert len(result['transactions']) == 2


def test_get_paginated_transactions_with_type_filter(mock_csv_path):
    """Test de la pagination avec filtre de type."""
    result = transactions_service.get_paginated_transactions(
        page=1,
        limit=10,
        type_filter='PAYMENT'
    )

    assert result['total'] == 2
    assert all(t['type'] == 'PAYMENT' for t in result['transactions'])


def test_get_paginated_transactions_with_fraud_filter(mock_csv_path):
    """Test de la pagination avec filtre de fraude."""
    result = transactions_service.get_paginated_transactions(
        page=1,
        limit=10,
        is_fraud=1
    )

    assert result['total'] == 1
    assert all(t['isFraud'] == 1 for t in result['transactions'])


def test_get_paginated_transactions_with_amount_range(mock_csv_path):
    """Test de la pagination avec filtre de montant."""
    result = transactions_service.get_paginated_transactions(
        page=1,
        limit=10,
        min_amount=100,
        max_amount=200
    )

    assert result['total'] == 2
    assert all(100 <= t['amount'] <= 200 for t in result['transactions'])


def test_get_transaction_by_id(mock_csv_path):
    """Test de récupération d'une transaction par ID."""
    transaction = transactions_service.get_transaction_by_id('0')

    assert transaction is not None
    assert transaction['type'] == 'PAYMENT'
    assert transaction['amount'] == 9839.64


def test_get_transaction_by_id_not_found(mock_csv_path):
    """Test de récupération d'une transaction inexistante."""
    transaction = transactions_service.get_transaction_by_id('999')

    assert transaction is None


def test_get_transaction_by_id_invalid(mock_csv_path):
    """Test de récupération avec ID invalide."""
    transaction = transactions_service.get_transaction_by_id('abc')

    assert transaction is None


def test_get_transaction_types(mock_csv_path):
    """Test de récupération des types de transactions."""
    types = transactions_service.get_transaction_types()

    assert isinstance(types, list)
    assert len(types) == 4
    assert 'PAYMENT' in types
    assert 'TRANSFER' in types
    assert 'CASH_OUT' in types
    assert 'DEBIT' in types


def test_get_recent_transactions(mock_csv_path):
    """Test de récupération des transactions récentes."""
    recent = transactions_service.get_recent_transactions(n=3)

    assert len(recent) == 3
    assert recent[0]['step'] == 2  # Avant-dernière transaction
    assert recent[-1]['step'] == 3  # Dernière transaction


def test_search_transactions_by_type(mock_csv_path):
    """Test de recherche par type."""
    results = transactions_service.search_transactions(type_filter='PAYMENT')

    assert len(results) == 2
    assert all(t['type'] == 'PAYMENT' for t in results)


def test_search_transactions_by_fraud(mock_csv_path):
    """Test de recherche par fraude."""
    results = transactions_service.search_transactions(is_fraud=1)

    assert len(results) == 1
    assert results[0]['isFraud'] == 1


def test_search_transactions_by_amount_range(mock_csv_path):
    """Test de recherche par montant."""
    results = transactions_service.search_transactions(
        amount_min=50,
        amount_max=200
    )

    assert len(results) == 3
    assert all(50 <= t['amount'] <= 200 for t in results)


def test_search_transactions_multiple_filters(mock_csv_path):
    """Test de recherche avec plusieurs filtres."""
    results = transactions_service.search_transactions(
        type_filter='PAYMENT',
        is_fraud=0,
        amount_min=1000
    )

    assert len(results) == 2
    assert all(t['type'] == 'PAYMENT' for t in results)
    assert all(t['isFraud'] == 0 for t in results)
    assert all(t['amount'] >= 1000 for t in results)


def test_get_transactions_by_customer(mock_csv_path):
    """Test de récupération des transactions par client."""
    transactions = transactions_service.get_transactions_by_customer('C1231006815')

    assert len(transactions) == 2
    assert all(t['nameOrig'] == 'C1231006815' for t in transactions)


def test_get_transactions_by_customer_not_found(mock_csv_path):
    """Test avec client inexistant."""
    transactions = transactions_service.get_transactions_by_customer('C9999999999')

    assert len(transactions) == 0


def test_get_transactions_to_customer(mock_csv_path):
    """Test de récupération des transactions reçues."""
    transactions = transactions_service.get_transactions_to_customer('C840083671')

    assert len(transactions) == 1
    assert transactions[0]['nameDest'] == 'C840083671'


def test_get_transactions_to_customer_not_found(mock_csv_path):
    """Test avec destinataire inexistant."""
    transactions = transactions_service.get_transactions_to_customer('C9999999999')

    assert len(transactions) == 0


def test_delete_transaction(mock_csv_path):
    """Test de suppression de transaction (mode test)."""
    result = transactions_service.delete_transaction('0')

    assert 'message' in result
    assert '0' in result['message']
