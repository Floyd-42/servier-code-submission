import pytest
from src.data_processing.extract import DataExtractor
import pandas as pd

@pytest.fixture
def data_dir(tmp_path):
    # Crée un répertoire temporaire pour les données
    return tmp_path

def test_load_drugs_data(data_dir):
    # Crée un fichier CSV temporaire pour les médicaments
    csv_content = "atccode,drug\nA01,Paracetamol"
    csv_path = data_dir / "drugs.csv"
    csv_path.write_text(csv_content)

    # Teste le chargement des données
    extractor = DataExtractor(data_dir=str(data_dir))
    df = extractor.load_drugs_data()

    assert isinstance(df, pd.DataFrame)
    assert df.shape == (1, 2)
    assert df.iloc[0, 1] == "Paracetamol"

def test_load_pubmed_data(data_dir):
    # Crée les fichiers CSV et JSON temporaires pour PubMed
    csv_content = "id,title,date,journal\n1,Test PubMed,2020-01-01,Journal A"
    json_content = '[{"id": "2", "title": "Test PubMed 2", "date": "2020-01-02", "journal": "Journal B"}]'
    csv_path = data_dir / "pubmed.csv"
    json_path = data_dir / "pubmed.json"
    csv_path.write_text(csv_content)
    json_path.write_text(json_content)

    # Teste le chargement des données PubMed combinées
    extractor = DataExtractor(data_dir=str(data_dir))
    df = extractor.load_pubmed_data()

    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 4)
    assert "Journal A" in df["journal"].values
    assert "Journal B" in df["journal"].values

def test_load_clinical_trials_data(data_dir):
    # Crée un fichier CSV temporaire pour les essais cliniques
    csv_content = "id,scientific_title,date,journal\n1,Test Trial,2020-01-01,Journal A"
    csv_path = data_dir / "clinical_trials.csv"
    csv_path.write_text(csv_content)

    # Teste le chargement des données des essais cliniques
    extractor = DataExtractor(data_dir=str(data_dir))
    df = extractor.load_clinical_trials_data()

    assert isinstance(df, pd.DataFrame)
    assert df.shape == (1, 4)
    assert df.iloc[0, 1] == "Test Trial"
