import pytest
import pandas as pd
import os
from src.utils.file_utils import load_data

def test_load_data_csv(tmp_path):
    # Création d'un fichier CSV temporaire
    csv_content = "col1,col2\nvalue1,value2"
    csv_path = tmp_path / "test.csv"
    csv_path.write_text(csv_content)

    # Chargement des données
    df = load_data(str(csv_path))

    # Vérifications
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (1, 2)
    assert df.iloc[0, 0] == "value1"

def test_load_data_json(tmp_path):
    # Création d'un fichier JSON temporaire
    json_content = '[{"col1": "value1", "col2": "value2"}]'
    json_path = tmp_path / "test.json"
    json_path.write_text(json_content)

    # Chargement des données
    df = load_data(str(json_path))

    # Vérifications
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (1, 2)
    assert df.iloc[0, 0] == "value1"

def test_load_data_file_not_found():
    # Vérifie que l'erreur est levée si le fichier n'existe pas
    with pytest.raises(FileNotFoundError):
        load_data("non_existent_file.csv")

def test_load_data_unsupported_extension(tmp_path):
    # Création d'un fichier avec une extension non supportée
    unsupported_path = tmp_path / "test.txt"
    unsupported_path.write_text("This is a test.")

    # Vérifie que l'erreur est levée pour les extensions non supportées
    with pytest.raises(ValueError):
        load_data(str(unsupported_path))
