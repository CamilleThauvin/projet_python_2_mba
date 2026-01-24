"""Tests pour le service de détection de fraude."""
from banking_api.services import fraud_detection_service


def test_get_fraud_summary(mock_csv_path):
    """Test du résumé de fraude."""
    summary = fraud_detection_service.get_fraud_summary()

    assert 'total_frauds' in summary
    assert 'flagged' in summary
    assert 'precision' in summary
    assert 'recall' in summary

    assert summary['total_frauds'] == 1
    assert summary['flagged'] >= 0
    assert 0 <= summary['precision'] <= 1
    assert 0 <= summary['recall'] <= 1


def test_get_fraud_by_type(mock_csv_path):
    """Test de la répartition de la fraude par type."""
    fraud_stats = fraud_detection_service.get_fraud_by_type()

    assert isinstance(fraud_stats, list)
    assert len(fraud_stats) == 4  # 4 types dans les données de test

    for stat in fraud_stats:
        assert 'type' in stat
        assert 'total_transactions' in stat
        assert 'fraud_count' in stat
        assert 'fraud_rate' in stat
        assert stat['total_transactions'] > 0
        assert stat['fraud_count'] >= 0
        assert 0 <= stat['fraud_rate'] <= 100


def test_get_fraud_by_type_transfer(mock_csv_path):
    """Test des stats de fraude pour TRANSFER."""
    fraud_stats = fraud_detection_service.get_fraud_by_type()
    transfer_stats = [s for s in fraud_stats if s['type'] == 'TRANSFER'][0]

    assert transfer_stats['fraud_count'] == 1
    assert transfer_stats['fraud_rate'] == 100.0


def test_predict_fraud_high_amount_transfer(mock_csv_path):
    """Test de prédiction pour montant élevé TRANSFER."""
    prediction = fraud_detection_service.predict_fraud(
        transaction_type='TRANSFER',
        amount=250000,
        oldbalance_org=250000,
        newbalance_orig=0
    )

    assert 'isFraud' in prediction
    assert 'probability' in prediction
    assert 'reasons' in prediction
    assert prediction['isFraud'] is True
    assert prediction['probability'] > 0.5


def test_predict_fraud_normal_payment(mock_csv_path):
    """Test de prédiction pour paiement normal."""
    prediction = fraud_detection_service.predict_fraud(
        transaction_type='PAYMENT',
        amount=100,
        oldbalance_org=1000,
        newbalance_orig=900
    )

    assert prediction['isFraud'] is False
    assert prediction['probability'] < 0.5


def test_predict_fraud_account_emptying(mock_csv_path):
    """Test de prédiction pour vidage de compte."""
    prediction = fraud_detection_service.predict_fraud(
        transaction_type='CASH_OUT',
        amount=10000,
        oldbalance_org=10000,
        newbalance_orig=0
    )

    assert prediction['probability'] > 0


def test_predict_fraud_balance_inconsistency(mock_csv_path):
    """Test de prédiction avec incohérence de solde."""
    prediction = fraud_detection_service.predict_fraud(
        transaction_type='TRANSFER',
        amount=1000,
        oldbalance_org=5000,
        newbalance_orig=5000  # Le solde n'a pas changé malgré le transfer
    )

    assert prediction['probability'] > 0


def test_predict_fraud_low_amount_test(mock_csv_path):
    """Test de prédiction pour petit montant (test de carte)."""
    prediction = fraud_detection_service.predict_fraud(
        transaction_type='PAYMENT',
        amount=5,
        oldbalance_org=1000,
        newbalance_orig=995
    )

    assert prediction['probability'] > 0


def test_predict_fraud_probability_capped(mock_csv_path):
    """Test que la probabilité ne dépasse pas 1.0."""
    # Cumule plusieurs règles pour tester le cap
    prediction = fraud_detection_service.predict_fraud(
        transaction_type='TRANSFER',
        amount=500000,
        oldbalance_org=500000,
        newbalance_orig=10  # Incohérence
    )

    assert prediction['probability'] <= 1.0


def test_predict_fraud_reasons_provided(mock_csv_path):
    """Test que les raisons sont fournies."""
    prediction = fraud_detection_service.predict_fraud(
        transaction_type='TRANSFER',
        amount=300000,
        oldbalance_org=300000,
        newbalance_orig=0
    )

    assert isinstance(prediction['reasons'], list)
    assert len(prediction['reasons']) > 0
