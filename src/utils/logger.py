import logging

def setup_logger(name: str, log_file: str, level=logging.INFO):
    """
    Configure un logger.

    Args:
        name (str): Nom du logger.
        log_file (str): Chemin du fichier de log.
        level (int): Niveau de log.
    """
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler = logging.FileHandler(log_file, encoding = "UTF-8")
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
