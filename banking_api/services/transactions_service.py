import csv
import os
import pandas as pd
from fastapi import HTTPException


def get_paginated_transactions(page: int, limit: int):
    """
    Retourne une liste paginée de transactions.
    
    Parameters
    ----------
    page : int
        Numéro de la page
    limit : int
        Nombre de transactions par page
        
    Returns
    -------
    dict
        Dictionnaire contenant le statut et les données
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    csv_path = os.path.join(base_dir, "data", "transactions_data.csv")

    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="Fichier non trouvé")

    transactions = []
    try:
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            start_index = (page - 1) * limit
            for i, row in enumerate(reader):
                if i < start_index:
                    continue
                if len(transactions) < limit:
                    transactions.append(row)
                else:
                    break
        return {"status": "success", "data": transactions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_global_stats():
    """
    Calcule les statistiques globales du dataset.
    
    Returns
    -------
    dict
        Statistiques globales
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    csv_path = os.path.join(base_dir, "data", "transactions_data.csv")

    try:
        count = 0
        with open(csv_path, 'rb') as f:
            for _ in f:
                count += 1
        return {
            "total_transactions": count - 1,
            "file_size": f"{round(os.path.getsize(csv_path) / (1024**3), 2)} Go"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_transaction_by_id(transaction_id: str):
    """
    Récupère une transaction par son ID.
    
    Parameters
    ----------
    transaction_id : str
        L'identifiant de la transaction
        
    Returns
    -------
    dict or None
        La transaction trouvée ou None
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    csv_path = os.path.join(base_dir, "data", "transactions_data.csv")
    
    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="Fichier non trouvé")
    
    try:
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if str(i) == transaction_id:
                    return row
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_transaction_types():
    """
    Retourne la liste des types de transactions uniques.
    
    Returns
    -------
    list
        Liste des types de transactions
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    csv_path = os.path.join(base_dir, "data", "transactions_data.csv")
    
    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="Fichier non trouvé")
    
    try:
        df = pd.read_csv(csv_path)
        return df['type'].unique().tolist()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_recent_transactions(n: int = 10):
    """
    Retourne les N dernières transactions.
    
    Parameters
    ----------
    n : int
        Nombre de transactions à retourner
        
    Returns
    -------
    list
        Liste des dernières transactions
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    csv_path = os.path.join(base_dir, "data", "transactions_data.csv")
    
    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="Fichier non trouvé")
    
    try:
        df = pd.read_csv(csv_path)
        recent = df.tail(n).to_dict('records')
        return recent
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))