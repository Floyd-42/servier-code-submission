import pytest
import pandas as pd
from src.utils.text_utils import clean_data, clean_dates, fill_missing_ids

def test_clean_data():
    # Création d'un DataFrame de test
    data = {'text': ['  Hello World! ', 'TEST123!!', None]}
    df = pd.DataFrame(data)

    # Appel de la fonction avec la colonne "text"
    cleaned_df = clean_data(df, text_columns=['text'])

    # Vérifications
    assert cleaned_df['text'][0] == 'Hello World'
    assert cleaned_df['text'][1] == 'TEST123'
    assert pd.isna(cleaned_df['text'][2])  # Le None d'origine reste inchangé

def test_clean_data_missing_column():
    # Création d'un DataFrame sans la colonne "missing_column"
    data = {'text': ['Test data']}
    df = pd.DataFrame(data)

    # Vérifie que l'erreur est levée si une colonne manquante est spécifiée
    with pytest.raises(ValueError):
        clean_data(df, text_columns=['missing_column'])

def test_clean_dates():
    # Création d'un DataFrame de test avec des dates dans différents formats
    data = {'date': ['2020-01-01', '01/02/2020', 'March 3, 2020', 'Invalid date']}
    df = pd.DataFrame(data)

    # Nettoyage des dates
    cleaned_df = clean_dates(df, date_columns=['date'])

    # Vérifications
    assert cleaned_df['date'][0] == '2020-01-01'
    assert cleaned_df['date'][1] == '2020-01-02'
    assert cleaned_df['date'][2] == '2020-03-03'
    assert pd.isna(cleaned_df['date'][3])  # Les dates invalides sont converties en NaT

def test_fill_missing_ids():
    # Création d'un DataFrame avec des IDs manquants
    data = {'id': [None, '', 'ID003'], 'value': [1, 2, 3]}
    df = pd.DataFrame(data)

    # Remplissage des IDs manquants
    filled_df = fill_missing_ids(df, id_column='id', prefix='TEST')

    # Vérifications
    assert filled_df['id'][0] == 'TEST01'
    assert filled_df['id'][1] == 'TEST02'
    assert filled_df['id'][2] == 'ID003'

def test_fill_missing_ids_no_id_column():
    # Création d'un DataFrame sans la colonne "id"
    data = {'value': [1, 2, 3]}
    df = pd.DataFrame(data)

    # Vérifie que l'erreur est levée si la colonne "id" n'est pas présente
    with pytest.raises(ValueError):
        fill_missing_ids(df, id_column='id')
