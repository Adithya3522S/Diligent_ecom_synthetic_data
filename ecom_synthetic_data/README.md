# E-commerce Synthetic Data

This project provides a complete workflow for generating and analyzing synthetic e-commerce datasets. It includes:

* Scripts for creating realistic customer, product, order, and payment datasets
* Utilities to ingest generated data into a local SQLite database
* Example SQL queries demonstrating common analytics workflows

## Current Structure

* `data/`: auto-generated datasets (CSV files)
* `db/`: generated SQLite database (`ecom.db`)
* `scripts/`: Python utilities for data generation, ingestion, and running queries
* `sql/`: example SQL queries for analytics

## Getting Started

1. Activate the Python virtual environment:

   * Windows:

     ```
     venv\Scripts\activate
     ```

   * macOS/Linux:

     ```
     source venv/bin/activate
     ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Generate synthetic datasets:

   ```
   python scripts/generate_ecom_data.py
   ```

4. Ingest datasets into SQLite:

   ```
   python scripts/ingest_to_sqlite.py
   ```

5. Run example SQL queries:

   ```
   python scripts/run_queries.py
   ```

The repository is fully functional with dataset generation, ingestion, and analysis workflows.
