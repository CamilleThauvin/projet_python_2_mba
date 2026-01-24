"""API REST pour les transactions bancaires."""
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from banking_api.services import transactions_service

app = FastAPI(title="Banking Transactions API", version="1.0.0")


# ==================== MODELS ====================

class SearchRequest(BaseModel):
    """Modèle pour la recherche de transactions."""
    type: Optional[str] = None
    isFraud: Optional[int] = None
    amount_range: Optional[List[float]] = None


# ==================== SYSTEM ROUTES ====================

@app.get("/api/system/health", tags=["System"])
def get_health() -> Dict[str, Any]:
    """
    Vérifie l'état de santé de l'API.

    Returns
    -------
    Dict[str, Any]
        Statut de l'API et disponibilité des données
    """
    dataset_exists: bool = os.path.exists("data/transactions_data.csv")
    return {"status": "ok", "dataset_loaded": dataset_exists}


@app.get("/api/system/metadata", tags=["System"])
def get_metadata() -> Dict[str, str]:
    """
    Retourne les métadonnées du service.

    Returns
    -------
    Dict[str, str]
        Version et date de mise à jour
    """
    return {
        "version": "1.0.0",
        "last_update": "2025-12-20T22:00:00Z"
    }


# ==================== TRANSACTIONS ROUTES ====================

@app.get("/api/transactions", tags=["Transactions"])
def read_transactions(
    page: int = 1,
    limit: int = 10,
    type: Optional[str] = None,
    isFraud: Optional[int] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None
) -> Dict[str, Any]:
    """
    Liste paginée des transactions avec filtres optionnels.

    Parameters
    ----------
    page : int
        Numéro de page (défaut: 1)
    limit : int
        Nombre de résultats par page (défaut: 10)
    type : Optional[str]
        Filtrer par type de transaction
    isFraud : Optional[int]
        Filtrer par fraude (0 ou 1)
    min_amount : Optional[float]
        Montant minimum
    max_amount : Optional[float]
        Montant maximum

    Returns
    -------
    Dict[str, Any]
        Transactions paginées avec métadonnées
    """
    return transactions_service.get_paginated_transactions(
        page, limit, type, isFraud, min_amount, max_amount
    )


@app.get("/api/transactions/{transaction_id}", tags=["Transactions"])
def get_transaction(transaction_id: str) -> Dict[str, Any]:
    """
    Récupère une transaction par son ID.

    Parameters
    ----------
    transaction_id : str
        L'identifiant de la transaction

    Returns
    -------
    Dict[str, Any]
        La transaction trouvée
    """
    transaction: Optional[Dict[str, Any]] = transactions_service.get_transaction_by_id(transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction non trouvée")
    return transaction


@app.post("/api/transactions/search", tags=["Transactions"])
def search_transactions(request: SearchRequest) -> Dict[str, Any]:
    """
    Recherche multicritère de transactions (POST avec corps JSON).

    Parameters
    ----------
    request : SearchRequest
        Critères de recherche

    Returns
    -------
    Dict[str, Any]
        Liste des transactions correspondantes
    """
    amount_min: Optional[float] = None
    amount_max: Optional[float] = None

    if request.amount_range and len(request.amount_range) == 2:
        amount_min = request.amount_range[0]
        amount_max = request.amount_range[1]

    results: List[Dict[str, Any]] = transactions_service.search_transactions(
        type_filter=request.type,
        is_fraud=request.isFraud,
        amount_min=amount_min,
        amount_max=amount_max
    )

    return {"count": len(results), "transactions": results}


@app.get("/api/transactions/types", tags=["Transactions"])
def get_types() -> Dict[str, List[str]]:
    """
    Liste des types de transactions disponibles.

    Returns
    -------
    Dict[str, List[str]]
        Liste des types uniques
    """
    types: List[str] = transactions_service.get_transaction_types()
    return {"types": types}


@app.get("/api/transactions/recent", tags=["Transactions"])
def get_recent(n: int = 10) -> Dict[str, List[Dict[str, Any]]]:
    """
    Retourne les N dernières transactions.

    Parameters
    ----------
    n : int
        Nombre de transactions (défaut: 10)

    Returns
    -------
    Dict[str, List[Dict[str, Any]]]
        Liste des transactions récentes
    """
    transactions: List[Dict[str, Any]] = transactions_service.get_recent_transactions(n)
    return {"transactions": transactions}


@app.delete("/api/transactions/{transaction_id}", tags=["Transactions"])
def delete_transaction(transaction_id: str) -> Dict[str, str]:
    """
    Supprime une transaction fictive (utilisée uniquement en mode test).

    Parameters
    ----------
    transaction_id : str
        Identifiant de la transaction

    Returns
    -------
    Dict[str, str]
        Message de confirmation
    """
    return transactions_service.delete_transaction(transaction_id)


@app.get("/api/transactions/by-customer/{customer_id}", tags=["Transactions"])
def get_transactions_by_customer(customer_id: str) -> Dict[str, Any]:
    """
    Liste des transactions associées à un client (origine).

    Parameters
    ----------
    customer_id : str
        Identifiant du client émetteur

    Returns
    -------
    Dict[str, Any]
        Transactions du client
    """
    transactions: List[Dict[str, Any]] = transactions_service.get_transactions_by_customer(customer_id)
    return {"customer_id": customer_id, "count": len(transactions), "transactions": transactions}


@app.get("/api/transactions/to-customer/{customer_id}", tags=["Transactions"])
def get_transactions_to_customer(customer_id: str) -> Dict[str, Any]:
    """
    Liste des transactions reçues par un client (destination).

    Parameters
    ----------
    customer_id : str
        Identifiant du client destinataire

    Returns
    -------
    Dict[str, Any]
        Transactions reçues
    """
    transactions: List[Dict[str, Any]] = transactions_service.get_transactions_to_customer(customer_id)
    return {"customer_id": customer_id, "count": len(transactions), "transactions": transactions}
