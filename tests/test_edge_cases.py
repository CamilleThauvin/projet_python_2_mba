"""Tests pour les cas limites et edge cases."""
import pytest
from banking_api.services import transactions_service, customer_service, fraud_detection_service


def test_get_recent_transactions_more_than_available(mock_csv_path):
    """Test de récupération de plus de transactions que disponibles."""
    # On a 5 transactions, on demande 100
    recent = transactions_service.get_recent_transactions(n=100)

    assert len(recent) == 5  # Devrait retourner seulement les 5 disponibles


def test_get_paginated_transactions_page_out_of_range(mock_csv_path):
    """Test de pagination avec page hors limites."""
    # Page très grande
    result = transactions_service.get_paginated_transactions(page=1000, limit=10)

    assert result['page'] == 1000
    assert len(result['transactions']) == 0  # Aucune transaction sur cette page


def test_get_customer_profile_calculations(mock_csv_path):
    """Test des calculs dans le profil client."""
    profile = customer_service.get_customer_profile('C1231006815')

    # Vérifie que les calculs sont cohérents
    assert profile['avg_amount'] > 0
    assert profile['total_amount'] > 0
    assert profile['transactions_count'] > 0
    # total_amount devrait être environ avg_amount * count
    expected_total = profile['avg_amount'] * profile['transactions_count']
    assert abs(profile['total_amount'] - expected_total) < 1  # Tolérance d'arrondi


def test_fraud_prediction_all_rules(mock_csv_path):
    """Test de prédiction avec plusieurs règles simultanées."""
    prediction = fraud_detection_service.predict_fraud(
        transaction_type='CASH_OUT',
        amount=500000,  # Règle 1: montant élevé
        oldbalance_org=500000,  # Règle 3: montant égal au solde
        newbalance_orig=0  # Règle 2: solde à 0
    )

    # Devrait déclencher plusieurs règles
    assert prediction['isFraud'] is True
    assert prediction['probability'] > 0.5
    assert len(prediction['reasons']) > 1


def test_search_transactions_no_results(mock_csv_path):
    """Test de recherche sans résultats."""
    results = transactions_service.search_transactions(
        type_filter='NONEXISTENT_TYPE',
        is_fraud=1,
        amount_min=1000000
    )

    assert len(results) == 0


def test_get_customers_edge_pagination(mock_csv_path):
    """Test de pagination à la limite."""
    # Page 1 avec limite exacte
    result = customer_service.get_customers(page=1, limit=4)

    assert result['total'] == 4
    assert len(result['customers']) == 4


def test_fraud_summary_calculations(mock_csv_path):
    """Test des calculs dans le résumé de fraude."""
    summary = fraud_detection_service.get_fraud_summary()

    # Vérifie que precision et recall sont entre 0 et 1
    assert 0 <= summary['precision'] <= 1
    assert 0 <= summary['recall'] <= 1


def test_get_top_customers_default_parameters(mock_csv_path):
    """Test du top clients avec paramètres par défaut."""
    top = customer_service.get_top_customers()  # n=10, by='volume' par défaut

    assert isinstance(top, list)
    assert len(top) <= 10


def test_pagination_first_page(mock_csv_path):
    """Test de la première page de pagination."""
    result = transactions_service.get_paginated_transactions(page=1, limit=3)

    assert result['page'] == 1
    assert len(result['transactions']) == 3


def test_pagination_last_page(mock_csv_path):
    """Test de la dernière page de pagination."""
    # On a 5 transactions total, page 2 avec limit 3 devrait avoir 2 transactions
    result = transactions_service.get_paginated_transactions(page=2, limit=3)

    assert result['page'] == 2
    assert len(result['transactions']) == 2


def test_search_with_only_min_amount(mock_csv_path):
    """Test de recherche avec seulement montant minimum."""
    results = transactions_service.search_transactions(amount_min=100)

    assert all(t['amount'] >= 100 for t in results)


def test_search_with_only_max_amount(mock_csv_path):
    """Test de recherche avec seulement montant maximum."""
    results = transactions_service.search_transactions(amount_max=1000)

    assert all(t['amount'] <= 1000 for t in results)


def test_get_transaction_by_id_boundary(mock_csv_path):
    """Test de récupération par ID aux limites."""
    # ID 0 (premier)
    transaction = transactions_service.get_transaction_by_id('0')
    assert transaction is not None

    # ID 4 (dernier dans notre jeu de test de 5 transactions)
    transaction = transactions_service.get_transaction_by_id('4')
    assert transaction is not None


def test_fraud_prediction_edge_probabilities(mock_csv_path):
    """Test des probabilités limites."""
    # Très faible probabilité
    prediction = fraud_detection_service.predict_fraud(
        transaction_type='PAYMENT',
        amount=50,
        oldbalance_org=1000,
        newbalance_orig=950
    )
    assert 0 <= prediction['probability'] <= 1
