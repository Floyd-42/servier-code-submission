import json
import os
import pandas as pd

class DataLoader:
    """Classe pour le chargement des données transformées."""

    @staticmethod
    def save_to_json(df: pd.DataFrame, output_file: str):
        """
        Enregistre les données transformées au format JSON.

        Args:
            df (pd.DataFrame): Le DataFrame à enregistrer.
            output_file (str): Le chemin du fichier de sortie.
        """
        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Convertir le DataFrame en liste de dictionnaires
        data = df.to_dict(orient='records')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
