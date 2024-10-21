import pandas as pd

def clean_data(df: pd.DataFrame, text_columns: list[str] = None) -> pd.DataFrame:
    """
    Nettoie les colonnes de texte d'un DataFrame en normalisant les valeurs.
    
    Les étapes de nettoyage incluent :
    - Suppression des espaces en début et fin de chaîne.
    - Conversion en minuscules.
    - Suppression des caractères spéciaux, sauf pour les lettres, les chiffres et les espaces.
    
    Args:
        df (pd.DataFrame): Le DataFrame à nettoyer.

    Returns:
        pd.DataFrame: Le DataFrame nettoyé.
    """   
    # Vérifier que les colonnes existent
    if text_columns is not None:
        for col in text_columns:
            if col not in df:
                raise ValueError(f"La colonne {col} n'est pas présente dans le Dataframe.")
    
    # Appliquer les transformations de nettoyage
    df[text_columns] = df[text_columns].apply(
        lambda col: col.str.strip()  # Suppression des espaces en début et fin
                            .str.replace(r'[^\s\w-]', '', regex=True)  # Suppression des caractères spéciaux
    )

    return df

def clean_dates(df: pd.DataFrame, date_columns: list) -> pd.DataFrame:
    """
    Nettoie les colonnes de dates d'un DataFrame en les convertissant dans un format standard (YYYY-MM-DD).
    
    Args:
        df (pd.DataFrame): Le DataFrame contenant les colonnes de dates à nettoyer.
        date_columns (list): Liste des noms de colonnes à traiter comme des dates.
    
    Returns:
        pd.DataFrame: Le DataFrame avec les colonnes de dates normalisées.
    """
    for col in date_columns:
        if col in df.columns:
            # Convertir la colonne en format datetime et gérer les erreurs
            df[col] = pd.to_datetime(df[col], errors='coerce', format="mixed").dt.strftime('%Y-%m-%d')
    
    return df

def fill_missing_ids(df: pd.DataFrame, id_column: str = 'id', prefix: str = "MISSING") -> pd.DataFrame:
    """
    Remplit les valeurs manquantes dans la colonne d'identifiant en générant des IDs personnalisés.
    
    Les IDs sont générés sous la forme "AXX", où "A" est un préfixe personnalisé et "XX" est un nombre incrémental.
    
    Args:
        df (pd.DataFrame): Le DataFrame contenant les données avec potentiellement des IDs manquants.
        id_column (str): Le nom de la colonne d'identifiant. Par défaut, "id".
        prefix (str): Le préfixe utilisé pour générer les nouveaux IDs. Par défaut, "MISSING".
    
    Returns:
        pd.DataFrame: Le DataFrame avec les valeurs d'identifiant manquantes remplies.
    """
    if id_column not in df:
        raise ValueError(f"La colonne {id_column} n'est pas présente dans le Dataframe.")
    # Trouver les lignes où l'ID est manquant ou vide
    missing_id_mask = df[id_column].isna() | (df[id_column].str.strip() == "")
    
    # Générer les nouveaux IDs pour les lignes manquantes
    num_missing = missing_id_mask.sum()
    new_ids = [f"{prefix}{str(i+1).zfill(2)}" for i in range(num_missing)]
    
    # Remplir les IDs manquants avec les nouveaux IDs générés
    df.loc[missing_id_mask, id_column] = new_ids
    
    return df