import os

from cachetools import TTLCache, cached
from flask import Flask, render_template, request, jsonify
import polars as pl

from db.sqlite import get_db
from utils.validation import handle_validation, validate_request

app = Flask(__name__)

CACHE_MAXSIZE = int(os.getenv("QUERY_CACHE_MAXSIZE", 1024))
CACHE_TTL = int(os.getenv("QUERY_CACHE_TTL", 300))
query_cache = TTLCache(maxsize=CACHE_MAXSIZE, ttl=CACHE_TTL)


def clear_query_cache():
    """Invalidate cached query results.

    This should be called whenever the underlying database is modified to
    ensure cached responses remain in sync with persistent storage.
    """

    query_cache.clear()


def _pdb_cache_key(pdb_id: str, chain_id: str, residue: int, window: int, insertion_code: str) -> tuple:
    return pdb_id.lower(), chain_id, residue, window, insertion_code or ""


@cached(cache=query_cache, key=lambda pdb_id, chain_id, residue, window, insertion_code: _pdb_cache_key(pdb_id, chain_id, residue, window, insertion_code))
def fetch_pdb_mappings(pdb_id: str, chain_id: str, residue: int, window: int, insertion_code: str):
    with get_db() as conn:
        query = """
        SELECT
            pdb_residue_number,
            pdb_residue_insertion_code,
            pdb_residue_name,
            uniprot_accession_id,
            uniprot_residue_number,
            uniprot_residue_name
        FROM residues
        WHERE pdb_accession_id = ?
        AND pdb_chain_id = ?
        AND pdb_residue_number BETWEEN ? AND ?
        """
        params = [
            pdb_id.lower(),
            chain_id,
            residue - window,
            residue + window
        ]

        if insertion_code:
            query += " AND pdb_residue_insertion_code = ?"
            params.append(insertion_code)
        else:
            query += " AND (pdb_residue_insertion_code IS NULL OR pdb_residue_insertion_code = '')"

        query += " ORDER BY pdb_residue_number, pdb_residue_insertion_code"

        return pl.read_database(query, conn, execute_options={"parameters": params})


def _uniprot_cache_key(uniprot_id: str, residue: int, window: int) -> tuple:
    return uniprot_id, residue, window


@cached(cache=query_cache, key=lambda uniprot_id, residue, window: _uniprot_cache_key(uniprot_id, residue, window))
def fetch_uniprot_mappings(uniprot_id: str, residue: int, window: int):
    with get_db() as conn:
        query = """
        SELECT
            pdb_accession_id,
            pdb_chain_id,
            pdb_residue_number,
            pdb_residue_insertion_code,
            pdb_residue_name,
            uniprot_residue_name
        FROM residues
        WHERE uniprot_accession_id = ?
        AND uniprot_residue_number BETWEEN ? AND ?
        ORDER BY pdb_accession_id, pdb_chain_id, pdb_residue_number, pdb_residue_insertion_code
        """
        params = [
            uniprot_id,
            residue - window,
            residue + window
        ]

        return pl.read_database(query, conn, execute_options={"parameters": params})


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/map/pdb', methods=['POST'])
def map_pdb():
    validation = validate_request(
        request.form,
        ['pdb_id', 'chain_id', 'residue'],
        allow_insertion_code=True
    )
    error_response = handle_validation(validation)
    if error_response:
        return error_response

    pdb_id = validation.data['pdb_id']
    chain_id = validation.data['chain_id']
    residue = validation.data['residue']
    window = validation.data['window']
    insertion_code = validation.data.get('insertion_code', '')

    result = fetch_pdb_mappings(pdb_id, chain_id, residue, window, insertion_code)

    if len(result) == 0:
        return jsonify({"message": "No mapping found for the requested PDB range"}), 404

    return jsonify(result.to_dicts())


@app.route('/map/uniprot', methods=['POST'])
def map_uniprot():
    validation = validate_request(
        request.form,
        ['uniprot_id', 'residue']
    )
    error_response = handle_validation(validation)
    if error_response:
        return error_response

    uniprot_id = validation.data['uniprot_id']
    residue = validation.data['residue']
    window = validation.data['window']

    result = fetch_uniprot_mappings(uniprot_id, residue, window)

    if len(result) == 0:
        return jsonify({"message": "No mapping found for the requested UniProt range"}), 404

    return jsonify(result.to_dicts())


if __name__ == '__main__':
    app.run(debug=True)
