import argparse

from src.config import DATA_DIR, OUTPUT_FILE
from src.utils.logger import setup_logger
from src.data_processing.extract import DataExtractor
from src.data_processing.transform import DataTransformer
from src.data_processing.load import DataLoader
from src.usecases.most_mentioned_journal import find_most_mentioned_journal

def parse_arguments():
    """Parse les arguments de la ligne de commande."""
    parser = argparse.ArgumentParser(description="Exécuter le pipeline de traitement de données.")
    parser.add_argument("--debug", action="store_true", help="Activer le mode debug pour le logging.")
    return parser.parse_args()

def main():
    # Parse les arguments
    args = parse_arguments()

    # Configure le logger avec le niveau approprié
    log_level = "DEBUG" if args.debug else "INFO"
    logger = setup_logger(name="data_pipeline_logger", log_file="pipeline.log", level=log_level)
    
    try:
        # Instanciation de l'ETL
        extractor = DataExtractor(DATA_DIR)
        transformer = DataTransformer()
        loader = DataLoader()

        # Chargement des données
        drugs_df = extractor.load_drugs_data()
        pubmed_df = extractor.load_pubmed_data()
        clinical_trials_df = extractor.load_clinical_trials_data()

        drugs_df = transformer.transform_drugs_data(drugs_df)
        pubmed_df = transformer.transform_pubmed_data(pubmed_df)
        clinical_trials_df = transformer.transform_clinical_trials_data(clinical_trials_df)

        
        # Aperçus des données chargées
        logger.info(f"Taille des données de drugs : {len(drugs_df)}\n")
        logger.info(f"Taille des données de PubMed : {len(pubmed_df)}\n")
        logger.info(f"Taille des données de clinical_trials : {len(clinical_trials_df)}\n")

        logger.debug(f"Aperçu des données de drugs :\n{drugs_df}\n")
        logger.debug(f"Aperçu des données de PubMed :\n{pubmed_df}\n")
        logger.debug(f"Aperçu des données de clinical_trials :\n{clinical_trials_df}\n")

        # Recherche des mentions de drugs dans les publications
        drug_mentions_in_pubmed = transformer.find_drug_mentions_in_pubmed(pubmed_df, drugs_df)
        logger.debug(f"Apercu des mentions de drug dans les publications :\n{drug_mentions_in_pubmed}\n")

        # Recherche des mentions de drugs dans les essais cliniques
        drug_mentions_in_clinical_trials = transformer.find_drug_mentions_in_clinical_trials(clinical_trials_df, drugs_df)
        logger.debug(f"Apercu des mentions de drug dans les essais cliniques :\n{drug_mentions_in_clinical_trials}\n")

        # Recherche des mentions de drugs dans les journaux
        drug_mentions_in_journal = transformer.find_drug_mentions_in_journals(drugs_df, drug_mentions_in_pubmed, drug_mentions_in_clinical_trials)
        logger.debug(f"Apercu des mentions de drug dans les journaux :\n{drug_mentions_in_journal}\n")

        loader.save_to_json(drug_mentions_in_journal, OUTPUT_FILE)

    except Exception as e:
        logger.error(f"Erreur lors de l'exécution du pipeline: {e}")
        raise

    # A la suite de la pipeline, on répond à la question "quel journal mentionne le plus de médicaments différents ?"
    try:
        most_mentioned_journal = find_most_mentioned_journal(OUTPUT_FILE)
        logger.info(f"Le journal qui mentionne le plus de médicament est : {most_mentioned_journal}")

    except Exception as e:
        logger.error(f"Erreur lors de l'exécution des usecases: {e}")
        raise

if __name__ == "__main__":
    main()
 