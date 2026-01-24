"""Service de détection et analyse de fraude."""
import os
from typing import Dict, List, Any
import pandas as pd
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


def get_fraud_summary() -> Dict[str, Any]:
    """
    Vue d'ensemble de la fraude dans le dataset.

    Returns
    -------
    Dict[str, Any]
        Dictionnaire contenant :
        - total_frauds : nombre total de fraudes
        - flagged : nombre de fraudes détectées
        - precision : précision de la détection
        - recall : rappel de la détection
    """
    csv_path: str = _get_csv_path()

    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="Fichier de données non trouvé")

    try:
        df: pd.DataFrame = pd.read_csv(csv_path)

        total_frauds: int = df['isFraud'].sum()
        flagged: int = df['isFlaggedFraud'].sum()

        # Calculer la précision et le rappel
        # Précision = Vrais positifs / (Vrais positifs + Faux positifs)
        # Rappel = Vrais positifs / (Vrais positifs + Faux négatifs)

        true_positives: int = ((df['isFraud'] == 1) & (df['isFlaggedFraud'] == 1)).sum()

        precision: float = 0.0
        if flagged > 0:
            precision = true_positives / flagged

        recall: float = 0.0
        if total_frauds > 0:
            recall = true_positives / total_frauds

        return {
            "total_frauds": int(total_frauds),
            "flagged": int(flagged),
            "precision": round(precision, 2),
            "recall": round(recall, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du calcul: {str(e)}")


def get_fraud_by_type() -> List[Dict[str, Any]]:
    """
    Répartition du taux de fraude par type de transaction.

    Returns
    -------
    List[Dict[str, Any]]
        Liste de dictionnaires contenant pour chaque type :
        - type : type de transaction
        - total_transactions : nombre total de transactions
        - fraud_count : nombre de fraudes
        - fraud_rate : taux de fraude (%)
    """
    csv_path: str = _get_csv_path()

    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="Fichier de données non trouvé")

    try:
        df: pd.DataFrame = pd.read_csv(csv_path)

        # Grouper par type
        fraud_by_type = df.groupby('type').agg({
            'isFraud': ['count', 'sum', 'mean']
        }).reset_index()

        # Aplatir les colonnes
        fraud_by_type.columns = ['type', 'total_transactions', 'fraud_count', 'fraud_rate']

        # Convertir en liste de dictionnaires
        results: List[Dict[str, Any]] = []
        for _, row in fraud_by_type.iterrows():
            results.append({
                'type': row['type'],
                'total_transactions': int(row['total_transactions']),
                'fraud_count': int(row['fraud_count']),
                'fraud_rate': round(float(row['fraud_rate']) * 100, 2)  # Convertir en pourcentage
            })

        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du calcul: {str(e)}")


def predict_fraud(
    transaction_type: str,
    amount: float,
    oldbalance_org: float,
    newbalance_orig: float
) -> Dict[str, Any]:
    """
    Prédiction simple de fraude basée sur des règles heuristiques.

    Parameters
    ----------
    transaction_type : str
        Type de transaction
    amount : float
        Montant de la transaction
    oldbalance_org : float
        Ancien solde de l'émetteur
    newbalance_orig : float
        Nouveau solde de l'émetteur

    Returns
    -------
    Dict[str, Any]
        Dictionnaire contenant :
        - isFraud : prédiction booléenne
        - probability : probabilité estimée de fraude
        - reasons : liste des raisons de la prédiction
    """
    is_fraud: bool = False
    probability: float = 0.0
    reasons: List[str] = []

    # Règle 1 : Transactions TRANSFER ou CASH_OUT avec montant élevé
    if transaction_type in ["TRANSFER", "CASH_OUT"] and amount > 200000:
        probability += 0.4
        reasons.append("Montant élevé pour un TRANSFER/CASH_OUT")

    # Règle 2 : Solde devient exactement 0
    if newbalance_orig == 0.0 and oldbalance_org > 0:
        probability += 0.3
        reasons.append("Solde vidé complètement")

    # Règle 3 : Montant égal au solde initial (vidage de compte)
    if abs(amount - oldbalance_org) < 0.01 and oldbalance_org > 0:
        probability += 0.25
        reasons.append("Montant égal au solde initial")

    # Règle 4 : Incohérence dans les soldes
    expected_balance: float = oldbalance_org - amount
    if abs(newbalance_orig - expected_balance) > 0.01:
        probability += 0.15
        reasons.append("Incohérence dans les soldes")

    # Règle 5 : Montant très faible (test de carte volée)
    if amount < 10 and transaction_type in ["PAYMENT", "DEBIT"]:
        probability += 0.1
        reasons.append("Montant très faible (test potentiel)")

    # Limiter la probabilité à 1.0
    probability = min(probability, 1.0)

    # Décision finale
    if probability >= 0.5:
        is_fraud = True

    return {
        "isFraud": is_fraud,
        "probability": round(probability, 2),
        "reasons": reasons if is_fraud else ["Transaction normale"]
    }
