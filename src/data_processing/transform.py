from src.utils.text_utils import clean_data, clean_dates, fill_missing_ids
import pandas as pd
import re

class DataTransformer:
    """Classe pour gérer les transformations des données extraites."""

    def __init__(self):
        pass

    def transform_drugs_data(self, drugs_df: pd.DataFrame) -> pd.DataFrame:
        """
        Transforme les données des médicaments en les normalisant.
        
        Args:
            drugs_df (pd.DataFrame): DataFrame des données des médicaments.
        
        Returns:
            pd.DataFrame: DataFrame transformé des médicaments.
        """
        drugs_df = clean_data(drugs_df, text_columns = ["drug"])
        drugs_df = fill_missing_ids(drugs_df, id_column='atccode')
        return drugs_df
 
    def transform_pubmed_data(self, pubmed_df: pd.DataFrame) -> pd.DataFrame:
        """
        Transforme les données des publications en les normalisant.
        
        Args:
            pubmed_df (pd.DataFrame): DataFrame des publications.
        
        Returns:
            pd.DataFrame: DataFrame transformé des publications.
        """
        pubmed_df = clean_data(pubmed_df, text_columns=["title", "journal"])
        pubmed_df = clean_dates(pubmed_df, date_columns=["date"])
        pubmed_df = fill_missing_ids(pubmed_df, id_column='id')
        return pubmed_df
 
    def transform_clinical_trials_data(self, clinical_trials_df: pd.DataFrame) -> pd.DataFrame:
        """
        Transforme les données des essais cliniques en les normalisant.
        
        Args:
            clinical_trials_df (pd.DataFrame): DataFrame des essais cliniques.
        
        Returns:
            pd.DataFrame: DataFrame transformé des essais cliniques.
        """
        clinical_trials_df = clean_data(clinical_trials_df, text_columns=["scientific_title", "journal"])
        clinical_trials_df = clean_dates(clinical_trials_df, date_columns=["date"])
        return clinical_trials_df

    def find_drug_mentions_in_pubmed(self, pubmed_df: pd.DataFrame, drugs_df: pd.DataFrame) -> pd.DataFrame:
        """
        Filtre les publications qui mentionnent des médicaments dans leur titre.
        
        Args:
            pubmed_df (pd.DataFrame): DataFrame des publications.
            drugs_df (pd.DataFrame): DataFrame des médicaments.
        
        Returns:
            pd.DataFrame: DataFrame filtré des publications avec les médicaments mentionnés.
        """
        mentions = []
        for _, drug_row in drugs_df.iterrows():
            drug_name = drug_row['drug']
            matched_publications_df = pubmed_df[pubmed_df['title'].str.contains(fr'\b{re.escape(drug_name)}\b', na=False, case=False)]
            for _, pub_row in matched_publications_df.iterrows():
                mentions.append({
                    'atccode': drug_row['atccode'],
                    'drug': drug_name,
                    'pubmed_id': pub_row['id'],
                    'title': pub_row['title'],
                    'date': pub_row['date'],
                    'journal': pub_row['journal']
                })
        return pd.DataFrame(mentions)

    def find_drug_mentions_in_clinical_trials(self, clinical_trials_df: pd.DataFrame, drugs_df: pd.DataFrame) -> pd.DataFrame:
        """
        Filtre les essais cliniques qui mentionnent des médicaments dans leur titre.
        
        Args:
            clinical_trials_df (pd.DataFrame): DataFrame des essais cliniques.
            drugs_df (pd.DataFrame): DataFrame des médicaments.
        
        Returns:
            pd.DataFrame: DataFrame filtré des essais cliniques avec les médicaments mentionnés.
        """
        mentions = []
        for _, drug_row in drugs_df.iterrows():
            drug_name = drug_row['drug']
            matched_clinical_trials_df = clinical_trials_df[clinical_trials_df['scientific_title'].str.contains(fr'\b{re.escape(drug_name)}\b', na=False, case=False)]
            for _, clinical_row in matched_clinical_trials_df.iterrows():
                mentions.append({
                    'atccode': drug_row['atccode'],
                    'drug': drug_name,
                    'clinical_trials_id': clinical_row['id'],
                    'title': clinical_row['scientific_title'],
                    'date': clinical_row['date'],
                    'journal': clinical_row['journal']
                })
        return pd.DataFrame(mentions)

    def find_drug_mentions_in_journals(self, drugs_df: pd.DataFrame, pubmed_df: pd.DataFrame, clinical_trials_df: pd.DataFrame) -> pd.DataFrame:
        """
        Associe les médicaments aux journaux en fonction des mentions dans les publications et essais cliniques.
        
        Args:
            mentions_df (pd.DataFrame): DataFrame des mentions de médicaments dans les publications et essais cliniques.
        
        Returns:
            pd.DataFrame: DataFrame des associations entre les médicaments et les journaux.
        """
        drugs_in_pubmed = pubmed_df[['atccode', 'drug', 'journal', 'date']]
        drugs_in_clinical_trials = clinical_trials_df[['atccode', 'drug', 'journal', 'date']]
        combined_journals = pd.concat([drugs_in_pubmed, drugs_in_clinical_trials], ignore_index=True).drop_duplicates()

        return combined_journals
