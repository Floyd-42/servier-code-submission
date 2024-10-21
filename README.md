## Data Pipeline Servier 
Ce projet implémente une pipeline de traitement de données en Python pour extraire, transformer et charger (ETL) des données à partir de fichiers sources (CSV et JSON).

## Installation
1. Cloner le projet : `git clone <url_du_projet>`
2. Installer les dépendances : `pip install -r requirements.txt`

## Utilisation
1. Placer les fichiers de données dans le dossier `data/`.
2. Exécuter la pipeline : `python main.py`

## Tests
Les tests unitaires se trouvent dans le dossier `tests/`. Exécutez les tests avec : `pytest`

## Pour aller plus loin

### Quels sont les éléments à considérer pour faire évoluer votre code afin qu’il puisse gérer de grosses volumétries de données (fichiers de plusieurs To ou millions de fichiers par exemple) ?

Lorsque la volumétrie dépassera les ~500Go-1To, il faudra au choix : soit passer sur une solution cloud en exploitant les capacités de ce dernier, soit utiliser des outils comme Spark, fait pour une grosse volumétrie.

### Pourriez-vous décrire les modifications qu’il faudrait apporter, s’il y en a, pour prendre en considération de telles volumétries ?

Ma réponse s'orientera vers la partie cloud GCP, que je maîtrise plus (mais le choix à faire ne dépend évidemment pas de moi).

La pipeline semble adaptée à un besoin batch (à discuter avec le client), je part donc dans cette direction.

Les données seront idéalement stockés sous un autre format que CSV ou JSON : Parquet qui répond au mieux au besoin de volumétrie. Nous avons rarement le choix des données d'entrée cela dit.

Les tables produites seront stockés sur BigQuery. La transformation de données sera fait avec des outils comme DBT ou Dataform. L'orchestration pourra être fait sur Workflows ou bien Apache Airflow.

## Notes

Certains points nécessitent plus d'éclaircissement, et doivent être discutés avant d'être implémentés.
Par exemple, un des journal est "Journal of emergency nursing\xc3\x28", mais les caractères "\xc3\x28" sont en UTF-8 (donc plain text).
J'aurai pu les filtrer, mais cette différence me pousse à d'abord valider avec le client si c'est une bonne chose d'altérer les entrées de journal.
Si ce filtre avait été mis en place, c'est bien le journal "Journal of emergency nursing" qui serait en tête pour les mentions des drugs.