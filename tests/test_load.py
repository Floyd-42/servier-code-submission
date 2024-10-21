import pytest
import pandas as pd
import os
import json
from src.data_processing.load import DataLoader

@pytest.fixture
def sample_df():
    """Fixture pour un DataFrame exemple."""
    data = [
        {"id": 1, "name": "Aspirin", "date": "2022-01-01"},
        {"id": 2, "name": "Paracetamol", "date": "2021-12-31"},
    ]
    return pd.DataFrame(data)

def test_save_to_json(sample_df, tmp_path):
    """Teste la sauvegarde du DataFrame en JSON."""
    output_file = tmp_path / "output.json"
    DataLoader.save_to_json(sample_df, str(output_file))
    
    # Vérifier si le fichier a été créé
    assert output_file.exists()

    # Vérifier le contenu du fichier
    with open(output_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        assert len(data) == len(sample_df)
        assert data[0]["name"] == "Aspirin"
