import pandas as pd
import os

def load_data(file_path: str) -> pd.DataFrame:
    """
    Charge un fichier de données en détectant automatiquement le type de fichier (CSV ou JSON).
    
    Args:
        file_path (str): Le chemin vers le fichier de données.
    
    Returns:
        pd.DataFrame: Le DataFrame contenant les données du fichier.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Le fichier {file_path} est introuvable.")
    
    # Détecter l'extension du fichier
    _, file_extension = os.path.splitext(file_path)
    
    # Charger les données en fonction de l'extension
    try:
        if file_extension.lower() == '.csv':
            return pd.read_csv(file_path, encoding='UTF-8')
        elif file_extension.lower() == '.json':
            return pd.read_json(file_path, encoding='UTF-8')
        else:
            raise ValueError(f"Type de fichier non pris en charge : {file_extension}. Seuls les fichiers CSV et JSON sont supportés.")
    except ValueError as e:
        raise ValueError(f"Erreur lors de la lecture du fichier : {file_path}. {e}")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Le fichier spécifié n'a pas été trouvé : {file_path}. {e}")