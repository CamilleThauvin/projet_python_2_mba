"""Tests pour le service de statistiques."""
from banking_api.services import stats_service


def test_get_overview(mock_csv_path):
    """Test des statistiques globales."""
    overview = stats_service.get_overview()

    assert 'total_transactions' in overview
    assert 'fraud_rate' in overview
    assert 'avg_amount' in overview
    assert 'most_common_type' in overview

    assert overview['total_transactions'] == 5
    assert 0 <= overview['fraud_rate'] <= 1
    assert overview['avg_amount'] > 0


def test_get_amount_distribution(mock_csv_path):
    """Test de la distribution des montants."""
    distribution = stats_service.get_amount_distribution(bins=10)

    assert 'bins' in distribution
    assert 'counts' in distribution
    assert isinstance(distribution['bins'], list)
    assert isinstance(distribution['counts'], list)
    assert len(distribution['bins']) == len(distribution['counts'])


def test_get_stats_by_type(mock_csv_path):
    """Test des statistiques par type."""
    stats = stats_service.get_stats_by_type()

    assert isinstance(stats, list)
    assert len(stats) == 4  # 4 types dans les données de test

    # Vérifier la structure de chaque élément
    for stat in stats:
        assert 'type' in stat
        assert 'count' in stat
        assert 'avg_amount' in stat
        assert 'total_amount' in stat
        assert stat['count'] > 0
        assert stat['avg_amount'] > 0
        assert stat['total_amount'] > 0


def test_get_stats_by_type_payment(mock_csv_path):
    """Test des statistiques pour le type PAYMENT."""
    stats = stats_service.get_stats_by_type()
    payment_stats = [s for s in stats if s['type'] == 'PAYMENT'][0]

    assert payment_stats['count'] == 2
    assert payment_stats['avg_amount'] > 0


def test_get_daily_stats(mock_csv_path):
    """Test des statistiques quotidiennes."""
    daily = stats_service.get_daily_stats()

    assert isinstance(daily, list)
    assert len(daily) == 3  # 3 jours (steps) dans les données de test

    # Vérifier la structure
    for day_stat in daily:
        assert 'day' in day_stat
        assert 'count' in day_stat
        assert 'avg_amount' in day_stat
        assert 'total_amount' in day_stat
        assert day_stat['count'] > 0


def test_get_daily_stats_order(mock_csv_path):
    """Test que les stats quotidiennes sont ordonnées par jour."""
    daily = stats_service.get_daily_stats()

    days = [d['day'] for d in daily]
    assert days == sorted(days)


def test_get_daily_stats_day_1(mock_csv_path):
    """Test des statistiques pour le jour 1."""
    daily = stats_service.get_daily_stats()
    day_1 = [d for d in daily if d['day'] == 1][0]

    assert day_1['count'] == 2  # 2 transactions au step 1
    assert day_1['avg_amount'] > 0
    assert day_1['total_amount'] > 0
