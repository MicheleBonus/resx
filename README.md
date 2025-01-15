# ResX

Fast residue cross-referencing between PDB and UniProt databases.

## Features
- Quick mapping between PDB and UniProt residue numbers
- Support for residue ranges and windows
- Simple web interface
- Fast SQLite-based backend
- Support for insertion codes

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/resx.git
cd resx
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the server:
```bash
python app.py
```

2. Open a web browser and navigate to:
```
http://127.0.0.1:5000
```

## API Endpoints

### PDB to UniProt Mapping
```
POST /map/pdb
Form data:
- pdb_id: PDB identifier (e.g., "101m")
- chain_id: Chain identifier (e.g., "A")
- residue: Residue number
- window: Number of surrounding residues (optional)
```

### UniProt to PDB Mapping
```
POST /map/uniprot
Form data:
- uniprot_id: UniProt accession (e.g., "P02185")
- residue: Residue number
- window: Number of surrounding residues (optional)
```

## Development

### Running Tests
```bash
pytest tests/
```

### Exploring the Database
Jupyter notebooks in the `notebooks/` directory provide examples and testing procedures.

## License
[Your chosen license]

## Contributors
[Your name/organization]