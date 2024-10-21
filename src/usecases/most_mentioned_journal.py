import pandas as pd

def find_most_mentioned_journal(json_file: str) -> str:
    """
    Trouve le nom du journal qui mentionne le plus de médicaments différents.

    Args:
        json_file (str): Chemin vers le fichier JSON produit par la data pipeline.

    Returns:
        str: Le nom du journal avec le plus de mentions de médicaments différents.
    """
    # Charger le fichier JSON dans un DataFrame
    df = pd.read_json(json_file)

    # Vérifier que les colonnes nécessaires sont présentes
    if 'journal' not in df.columns or 'drug' not in df.columns:
        raise ValueError("Le fichier JSON doit contenir les colonnes 'journal' et 'drug'.")

    # Compter les médicaments uniques par journal
    drug_counts_per_journal = df.groupby('journal')['drug'].nunique()

    # Trouver le journal avec le plus de médicaments uniques
    journal_with_most_drugs = drug_counts_per_journal.idxmax()
    
    return journal_with_most_drugs
