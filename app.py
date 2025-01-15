from flask import Flask, render_template, request, jsonify
from db.sqlite import get_db
import polars as pl

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map/pdb', methods=['POST'])
def map_pdb():
    pdb_id = request.form.get('pdb_id')
    chain_id = request.form.get('chain_id')
    residue = request.form.get('residue')
    window = request.form.get('window', 0)
    insertion_code = request.form.get('insertion_code', '')
    
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
            int(residue) - int(window), 
            int(residue) + int(window)
        ]
        
        if insertion_code:
            query += " AND pdb_residue_insertion_code = ?"
            params.append(insertion_code)
        else:
            query += " AND (pdb_residue_insertion_code IS NULL OR pdb_residue_insertion_code = '')"
        
        query += " ORDER BY pdb_residue_number, pdb_residue_insertion_code"
        
        result = pl.read_database(query, conn, execute_options={"parameters": params})
        
        if len(result) == 0:
            return jsonify({"error": "No mapping found"})
            
        return jsonify(result.to_dicts())

@app.route('/map/uniprot', methods=['POST'])
def map_uniprot():
    uniprot_id = request.form.get('uniprot_id')
    residue = request.form.get('residue')
    window = request.form.get('window', 0)
    
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
            int(residue) - int(window),
            int(residue) + int(window)
        ]
        
        result = pl.read_database(query, conn, execute_options={"parameters": params})
        
        if len(result) == 0:
            return jsonify({"error": "No mapping found"})
            
        return jsonify(result.to_dicts())

if __name__ == '__main__':
    app.run(debug=True)