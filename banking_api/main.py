from fastapi import FastAPI, HTTPException
import os
from banking_api.services import transactions_service

app = FastAPI(title="Banking Transactions API")


# ==================== SYSTEM ROUTES ====================

@app.get("/api/system/health", tags=["System"])
def get_health():
    """Vérifie l'état de santé de l'API."""
    dataset_exists = os.path.exists("data/transactions_data.csv")
    return {"status": "ok", "dataset_loaded": dataset_exists}


@app.get("/api/system/metadata", tags=["System"])
def get_metadata():
    """
    Retourne les métadonnées du service.
    
    Returns
    -------
    dict
        Version et date de mise à jour
    """
    return {
        "version": "1.0.0",
        "last_update": "2025-12-20T22:00:00Z"
    }


# ==================== TRANSACTIONS ROUTES ====================

@app.get("/api/transactions/types", tags=["Transactions"])
def get_types():
    """
    Liste des types de transactions disponibles.
    
    Returns
    -------
    dict
        Liste des types
    """
    return {"types": transactions_service.get_transaction_types()}


@app.get("/api/transactions/recent", tags=["Transactions"])
def get_recent(n: int = 10):
    """
    Retourne les N dernières transactions.
    
    Parameters
    ----------
    n : int
        Nombre de transactions (défaut: 10)
        
    Returns
    -------
    dict
        Liste des transactions récentes
    """
    return {"transactions": transactions_service.get_recent_transactions(n)}


@app.get("/api/transactions/{transaction_id}", tags=["Transactions"])
def get_transaction(transaction_id: str):
    """
    Récupère une transaction par son ID.
    
    Parameters
    ----------
    transaction_id : str
        L'identifiant de la transaction
        
    Returns
    -------
    dict
        La transaction trouvée
    """
    transaction = transactions_service.get_transaction_by_id(transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction non trouvée")
    return transaction


@app.get("/api/transactions", tags=["Transactions"])
def read_transactions(page: int = 1, limit: int = 10):
    """
    Liste paginée des transactions.
    
    Parameters
    ----------
    page : int
        Numéro de page (défaut: 1)
    limit : int
        Nombre de résultats par page (défaut: 10)
        
    Returns
    -------
    dict
        Transactions paginées
    """
    return transactions_service.get_paginated_transactions(page, limit)


# ==================== STATS ROUTES ====================

@app.get("/api/transactions/stats", tags=["Statistiques"])
def read_stats():
    """
    Statistiques globales du dataset.
    
    Returns
    -------
    dict
        Statistiques générales
    """
    return transactions_service.get_global_stats()