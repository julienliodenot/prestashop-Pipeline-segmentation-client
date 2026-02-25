# Prestashop - Pipeline de segmentation clients

Projet data end-to-end démontrant la construction d'un pipeline analytique pour segmenter les clients Prestashop (`particulier` vs `société`) et produire des insights actionnables.

## En 10 secondes

- Problème : manque de visibilité fiable sur les segments clients
- Solution : API -> base -> transformation -> datamart -> BI
- Livrable : pipeline reproductible + dashboard de pilotage
- Positionnement : cas réel anonymisé à usage portfolio

## Contexte business

Objectif : comprendre la contribution des segments clients au chiffre d'affaires et orienter les décisions d'acquisition/fidélisation sur des données fiabilisées.

## Objectifs du pipeline

- Extraire depuis l'API Prestashop
- Charger et modéliser dans SQLite
- Transformer/nettoyer via KNIME
- Produire un CSV analytique
- Alimenter un dashboard Power BI

## Architecture

```text
API Prestashop -> Extraction Python -> SQLite -> Nettoyage/Transformation KNIME -> CSV data mart -> Power BI -> Restitution métier
```

## Stack

- Source : Prestashop Webservice API
- Ingestion : Python
- Stockage : SQLite
- Transformation : KNIME
- Datamart : CSV
- Visualisation : Power BI

## Structure du repository

```text
src/prestashop_etl/          Modules d'extraction et chargement
scripts/run_pipeline.py      Script d'exécution
config/.env.example          Variables d'environnement
Workflow_knime.knwf          Workflow de transformation
reporting.pbix               Dashboard Power BI
exemple_clean_data.csv       Exemple anonymisé
docs/architecture/           Documentation technique
```

## Démarrage rapide

1. Créer un environnement virtuel
2. Installer les dépendances
```bash
pip install -r requirements.txt
```
3. Créer `.env` depuis `config/.env.example`
4. Renseigner les identifiants Prestashop
5. Exécuter :
```bash
python scripts/run_pipeline.py
```
6. Ouvrir `Workflow_knime.knwf` et configurer :
- connexion SQLite
- chemin de sortie CSV
7. Exécuter le workflow KNIME
8. Ouvrir `reporting.pbix`, pointer le CSV, rafraîchir

Note :
- Un MegaNode LLM facultatif peut être activé pour traiter certains cas limites de classification.

## Valeur livrée

- Pipeline complet API vers BI
- Données structurées pour pilotage par segment
- Support de décision exploitable par métier et management

## Confidentialité

- Données brutes exclues
- Secrets en variables d'environnement
- Données d'exemple anonymisées/modifiées

## Limites et évolutions

Limites :
- Version portfolio, certaines étapes restent manuelles

Évolutions :
- Tests automatiques de qualité de données
- Orchestration planifiée
- Monitoring (fraîcheur, erreurs, reprise)
