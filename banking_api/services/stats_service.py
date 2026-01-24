"""Service de calcul de statistiques sur les transactions."""
import os
from typing import Dict, List, Any
import pandas as pd
import numpy as np
from fastapi import HTTPException


def _get_csv_path() -> str:
    """
    Retourne le chemin vers le fichier CSV de transactions.

    Returns
    -------
    str
        Chemin absolu vers le fichier CSV
    """
    base_dir: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    csv_path: str = os.path.join(base_dir, "data", "transactions_data.csv")
    return csv_path


def get_overview() -> Dict[str, Any]:
    """
    Statistiques globales du dataset.

    Returns
    -------
    Dict[str, Any]
        Dictionnaire contenant :
        - total_transactions : nombre total de transactions
        - fraud_rate : taux de fraude
        - avg_amount : montant moyen
        - most_common_type : type le plus fréquent
    """
    csv_path: str = _get_csv_path()

    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="Fichier de données non trouvé")

    try:
        df: pd.DataFrame = pd.read_csv(csv_path)

        total_transactions: int = len(df)
        fraud_rate: float = df['isFraud'].mean()
        avg_amount: float = df['amount'].mean()
        most_common_type: str = df['type'].mode()[0]

        return {
            "total_transactions": total_transactions,
            "fraud_rate": round(fraud_rate, 5),
            "avg_amount": round(avg_amount, 2),
            "most_common_type": most_common_type
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du calcul: {str(e)}")


def get_amount_distribution(bins: int = 10) -> Dict[str, Any]:
    """
    Histogramme du montant des transactions (en classes de valeurs).

    Parameters
    ----------
    bins : int
        Nombre de classes (défaut: 10)

    Returns
    -------
    Dict[str, Any]
        Dictionnaire contenant :
        - bins : liste des intervalles
        - counts : nombre de transactions par intervalle
    """
    csv_path: str = _get_csv_path()

    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="Fichier de données non trouvé")

    try:
        df: pd.DataFrame = pd.read_csv(csv_path)

        # Créer des bins personnalisés pour avoir des intervalles lisibles
        max_amount: float = df['amount'].max()

        # Définir des bins standards et ne garder que ceux inférieurs au max
        standard_bins: List[float] = [0, 100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 1000000]
        bin_edges: List[float] = [b for b in standard_bins if b <= max_amount]

        # Ajouter le max + 1 pour inclure toutes les valeurs
        bin_edges.append(max_amount + 1)

        # Calculer l'histogramme
        counts, edges = np.histogram(df['amount'], bins=bin_edges)

        # Créer les labels des bins
        bin_labels: List[str] = []
        for i in range(len(edges) - 1):
            if edges[i+1] == max_amount + 1:
                bin_labels.append(f"{int(edges[i])}+")
            else:
                bin_labels.append(f"{int(edges[i])}-{int(edges[i+1])}")

        return {
            "bins": bin_labels,
            "counts": counts.tolist()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du calcul: {str(e)}")


def get_stats_by_type() -> List[Dict[str, Any]]:
    """
    Montant total et nombre moyen de transactions par type.

    Returns
    -------
    List[Dict[str, Any]]
        Liste de dictionnaires contenant pour chaque type :
        - type : type de transaction
        - count : nombre de transactions
        - avg_amount : montant moyen
        - total_amount : montant total
    """
    csv_path: str = _get_csv_path()

    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="Fichier de données non trouvé")

    try:
        df: pd.DataFrame = pd.read_csv(csv_path)

        # Grouper par type
        grouped = df.groupby('type').agg({
            'amount': ['count', 'mean', 'sum']
        }).reset_index()

        # Aplatir les colonnes multi-niveaux
        grouped.columns = ['type', 'count', 'avg_amount', 'total_amount']

        # Convertir en liste de dictionnaires
        results: List[Dict[str, Any]] = []
        for _, row in grouped.iterrows():
            results.append({
                'type': row['type'],
                'count': int(row['count']),
                'avg_amount': round(float(row['avg_amount']), 2),
                'total_amount': round(float(row['total_amount']), 2)
            })

        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du calcul: {str(e)}")


def get_daily_stats() -> List[Dict[str, Any]]:
    """
    Moyenne et volume des transactions par jour (step).

    Returns
    -------
    List[Dict[str, Any]]
        Liste de dictionnaires contenant pour chaque jour :
        - day : numéro du jour (step)
        - count : nombre de transactions
        - avg_amount : montant moyen
        - total_amount : montant total
    """
    csv_path: str = _get_csv_path()

    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="Fichier de données non trouvé")

    try:
        df: pd.DataFrame = pd.read_csv(csv_path)

        # Grouper par step (jour)
        daily_stats = df.groupby('step').agg({
            'amount': ['count', 'mean', 'sum']
        }).reset_index()

        # Aplatir les colonnes
        daily_stats.columns = ['day', 'count', 'avg_amount', 'total_amount']

        # Convertir en liste de dictionnaires
        results: List[Dict[str, Any]] = []
        for _, row in daily_stats.iterrows():
            results.append({
                'day': int(row['day']),
                'count': int(row['count']),
                'avg_amount': round(float(row['avg_amount']), 2),
                'total_amount': round(float(row['total_amount']), 2)
            })

        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du calcul: {str(e)}")
