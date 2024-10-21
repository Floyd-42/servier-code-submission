import pytest
import pandas as pd
from src.data_processing.transform import DataTransformer

@pytest.fixture
def transformer():
    """Fixture pour instancier le DataTransformer."""
    return DataTransformer()

@pytest.fixture
def drugs_df():
    """Fixture pour un DataFrame exemple de médicaments."""
    data = {
        "drug": ["Aspirin", "Paracetamol", ""],
        "atccode": [None, "N02BE01", ""]
    }
    return pd.DataFrame(data)

@pytest.fixture
def pubmed_df():
    """Fixture pour un DataFrame exemple de publications PubMed."""
    data = {
        "title": ["Study of Aspirin effects", "Paracetamol use in children", "Other study"],
        "journal": ["Journal A", "Journal B", None],
        "date": ["2022-01-01", None, "2023-03-15"],
        "id": [None, "PUB123", ""]
    }
    return pd.DataFrame(data)

@pytest.fixture
def clinical_trials_df():
    """Fixture pour un DataFrame exemple d'essais cliniques."""
    data = {
        "scientific_title": ["Clinical trial of Aspirin", "Paracetamol trial", "Another trial"],
        "journal": ["Medical Journal", "Clinical Trials Journal", "Research Journal"],
        "date": ["2021-06-30", "2020-09-01", None],
        "id": [None, "", "CT456"]
    }
    return pd.DataFrame(data)

def test_transform_drugs_data(transformer, drugs_df):
    """Teste la transformation des données de médicaments."""
    transformed_df = transformer.transform_drugs_data(drugs_df)
    assert "drug" in transformed_df.columns
    assert "atccode" in transformed_df.columns
    assert transformed_df["atccode"].isna().sum() == 0  # Tous les atccodes doivent être remplis

def test_transform_pubmed_data(transformer, pubmed_df):
    """Teste la transformation des données PubMed."""
    transformed_df = transformer.transform_pubmed_data(pubmed_df)
    assert "title" in transformed_df.columns
    assert "journal" in transformed_df.columns
    assert "date" in transformed_df.columns

def test_transform_clinical_trials_data(transformer, clinical_trials_df):
    """Teste la transformation des données des essais cliniques."""
    transformed_df = transformer.transform_clinical_trials_data(clinical_trials_df)
    assert "scientific_title" in transformed_df.columns
    assert "journal" in transformed_df.columns
    assert "date" in transformed_df.columns

def test_find_drug_mentions_in_pubmed(transformer, pubmed_df, drugs_df):
    """Teste la recherche de mentions de médicaments dans les publications PubMed."""
    mentions_df = transformer.find_drug_mentions_in_pubmed(pubmed_df, drugs_df)
    assert not mentions_df.empty
    assert "atccode" in mentions_df.columns
    assert "drug" in mentions_df.columns
    assert "title" in mentions_df.columns

def test_find_drug_mentions_in_clinical_trials(transformer, clinical_trials_df, drugs_df):
    """Teste la recherche de mentions de médicaments dans les essais cliniques."""
    mentions_df = transformer.find_drug_mentions_in_clinical_trials(clinical_trials_df, drugs_df)
    assert not mentions_df.empty
    assert "atccode" in mentions_df.columns
    assert "drug" in mentions_df.columns
    assert "title" in mentions_df.columns

def test_find_drug_mentions_in_journals(transformer, drugs_df, pubmed_df, clinical_trials_df):
    """Teste la recherche d'associations entre les médicaments et les journaux."""
    drug_mentions_in_clinical_trials = transformer.find_drug_mentions_in_clinical_trials(clinical_trials_df, drugs_df)
    drug_mentions_in_pubmed = transformer.find_drug_mentions_in_pubmed(pubmed_df, drugs_df)
    journals_df = transformer.find_drug_mentions_in_journals(drugs_df, drug_mentions_in_pubmed, drug_mentions_in_clinical_trials)
    print(journals_df)
    assert not journals_df.empty
    assert "atccode" in journals_df.columns
    assert "drug" in journals_df.columns
    assert "journal" in journals_df.columns
