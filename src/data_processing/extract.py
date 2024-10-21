from src.utils.file_utils import load_data
import pandas as pd
import os

class DataExtractor:
    """Classe pour gérer l'extraction des différentes sources de données spécifiques."""

    def __init__(self, data_dir: str):
        """
        Initialise l'extracteur de données avec un répertoire de base.
        
        Args:
            data_dir (str): Chemin du répertoire contenant les fichiers de données.
        """
        self.data_dir = data_dir

    def load_drugs_data(self) -> pd.DataFrame:
        """
        Charge les données des médicaments à partir du fichier drugs.csv.
        
        Returns:
            pd.DataFrame: DataFrame des médicaments.
        """
        drugs_path = os.path.join(self.data_dir, 'drugs.csv')
        return load_data(drugs_path)

    def load_pubmed_data(self) -> pd.DataFrame:
        """
        Charge et combine les données de PubMed à partir des fichiers pubmed.csv et pubmed.json.
        
        Returns:
            pd.DataFrame: DataFrame combiné des données PubMed.
        """
        pubmed_csv_path = os.path.join(self.data_dir, 'pubmed.csv')
        pubmed_json_path = os.path.join(self.data_dir, 'pubmed.json')
        pubmed_csv = load_data(pubmed_csv_path)
        pubmed_json = load_data(pubmed_json_path)
        combined_pubmed = pd.concat([pubmed_csv, pubmed_json], ignore_index=True)
        return combined_pubmed

    def load_clinical_trials_data(self) -> pd.DataFrame:
        """
        Charge les données des essais cliniques à partir de clinical_trials.csv.
        
        Returns:
            pd.DataFrame: DataFrame des essais cliniques.
        """
        clinical_trials_path = os.path.join(self.data_dir, 'clinical_trials.csv')
        return load_data(clinical_trials_path)
