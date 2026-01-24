"""Tests pour le service de gestion des clients."""
import pytest
from fastapi import HTTPException
from banking_api.services import customer_service


def test_get_customers(mock_csv_path):
    """Test de récupération de la liste des clients."""
    result = customer_service.get_customers(page=1, limit=10)

    assert 'page' in result
    assert 'limit' in result
    assert 'total' in result
    assert 'customers' in result

    assert result['page'] == 1
    assert result['limit'] == 10
    assert result['total'] == 4  # 4 clients uniques dans les données de test
    assert len(result['customers']) <= 10


def test_get_customers_pagination(mock_csv_path):
    """Test de la pagination des clients."""
    result = customer_service.get_customers(page=1, limit=2)

    assert len(result['customers']) == 2
    assert result['total'] == 4


def test_get_customer_profile(mock_csv_path):
    """Test de récupération du profil client."""
    profile = customer_service.get_customer_profile('C1231006815')

    assert 'id' in profile
    assert 'transactions_count' in profile
    assert 'avg_amount' in profile
    assert 'total_amount' in profile
    assert 'fraudulent' in profile
    assert 'fraud_count' in profile

    assert profile['id'] == 'C1231006815'
    assert profile['transactions_count'] == 2
    assert profile['avg_amount'] > 0
    assert profile['total_amount'] > 0


def test_get_customer_profile_fraudulent(mock_csv_path):
    """Test de profil pour un client avec fraude."""
    profile = customer_service.get_customer_profile('C1666544295')

    assert profile['fraudulent']
    assert profile['fraud_count'] == 1


def test_get_customer_profile_not_fraudulent(mock_csv_path):
    """Test de profil pour un client sans fraude."""
    profile = customer_service.get_customer_profile('C1231006815')

    assert profile['fraudulent'] is False
    assert profile['fraud_count'] == 0


def test_get_customer_profile_not_found(mock_csv_path):
    """Test de profil pour client inexistant."""
    with pytest.raises(HTTPException) as exc_info:
        customer_service.get_customer_profile('C9999999999')

    assert exc_info.value.status_code == 404
    assert 'non trouvé' in exc_info.value.detail


def test_get_top_customers_by_volume(mock_csv_path):
    """Test du top clients par volume."""
    top = customer_service.get_top_customers(n=3, by='volume')

    assert isinstance(top, list)
    assert len(top) <= 3

    # Vérifier la structure
    for customer in top:
        assert 'customer_id' in customer
        assert 'transaction_count' in customer
        assert 'total_amount' in customer
        assert 'avg_amount' in customer
        assert 'fraud_count' in customer
        assert 'fraudulent' in customer


def test_get_top_customers_by_count(mock_csv_path):
    """Test du top clients par nombre de transactions."""
    top = customer_service.get_top_customers(n=3, by='count')

    assert isinstance(top, list)
    assert len(top) <= 3


def test_get_top_customers_sorted_by_volume(mock_csv_path):
    """Test que les clients sont triés par volume décroissant."""
    top = customer_service.get_top_customers(n=10, by='volume')

    amounts = [c['total_amount'] for c in top]
    assert amounts == sorted(amounts, reverse=True)


def test_get_top_customers_sorted_by_count(mock_csv_path):
    """Test que les clients sont triés par nombre de transactions."""
    top = customer_service.get_top_customers(n=10, by='count')

    counts = [c['transaction_count'] for c in top]
    assert counts == sorted(counts, reverse=True)


def test_get_top_customers_limit(mock_csv_path):
    """Test de la limitation du nombre de clients."""
    top = customer_service.get_top_customers(n=2, by='volume')

    assert len(top) == 2


def test_get_top_customers_fraud_flag(mock_csv_path):
    """Test du flag de fraude dans le top clients."""
    top = customer_service.get_top_customers(n=10, by='volume')

    for customer in top:
        if customer['fraud_count'] > 0:
            assert customer['fraudulent'] is True
        else:
            assert customer['fraudulent'] is False
