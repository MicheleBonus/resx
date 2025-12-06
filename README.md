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

2. Create and activate an isolated environment (recommended):

   - **venv (built-in Python):**
     ```bash
     python -m venv .venv
     source .venv/bin/activate  # On Windows: .venv\Scripts\activate
     ```

   - **Conda/Mamba:**
     ```bash
     mamba create -n resx python=3.11
     mamba activate resx
     # or with conda
     conda create -n resx python=3.11
     conda activate resx
     ```

3. Install dependencies using one of the options below.

### Option A: `pip` with `pyproject.toml`
If the project is configured with a `pyproject.toml`, install in editable mode:
```bash
pip install -e .
```

### Option B: `pip` with `requirements.txt`
Install the pinned dependencies directly:
```bash
pip install -r requirements.txt
```

### Option C: `uv` equivalents
Using [`uv`](https://docs.astral.sh/uv/):
```bash
# Create the virtual environment
uv venv .venv
source .venv/bin/activate

# Install from pyproject (when available)
uv pip install -e .

# Or install from requirements.txt
uv pip install -r requirements.txt
```

### Option D: `conda`/`mamba` installation
If you prefer to manage packages through `conda` or `mamba` inside the activated environment:
```bash
# Install from pyproject (when available)
mamba install pip
pip install -e .

# Or install from requirements.txt
pip install -r requirements.txt
```

### Database location
Place `topunipdbmapper.db` in the repository’s `db/` directory so it resolves to `db/topunipdbmapper.db` by default. To use a different path—whether you install via `pip`, `uv`, or inside a `conda`/`mamba` environment—set the `TOPUNIPDBMAPPER_DB` environment variable before running the app:
```bash
export TOPUNIPDBMAPPER_DB=/path/to/your/topunipdbmapper.db
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

## API Usage

The API accepts `application/x-www-form-urlencoded` form data (e.g., from HTML forms or `curl -d`). All routes enforce the same validation rules used by the web form.

### `POST /map/pdb` — PDB to UniProt mapping

Required fields:
- `pdb_id`: PDB identifier (e.g., `101m`).
- `chain_id`: Chain identifier (e.g., `A`).
- `residue`: Integer residue number.

Optional fields:
- `window`: Integer window size from `0`–`10` (default: `0`). Values outside this range return `{"error": "window must be an integer between 0 and 10"}` with HTTP 400.
- `insertion_code`: Single-character insertion code. Submitting more than one character returns `{"error": "insertion_code must be a single character"}` with HTTP 400. Omit this field to target residues without an insertion code.

Validation behavior:
- Missing required fields return `{"error": "Missing required field: <field>"}` with HTTP 400.
- Non-integer `residue` or `window` values return `"<field> must be an integer"` with HTTP 400.
- A valid request that finds no mapping returns `{"error": "No mapping found for the requested PDB range"}` with HTTP 404.

Sample request:
```bash
curl -X POST http://127.0.0.1:5000/map/pdb \
  -d "pdb_id=1abc" \
  -d "chain_id=A" \
  -d "residue=42" \
  -d "window=2"
```

Sample response:
```json
[
  {
    "pdb_residue_number": 41,
    "pdb_residue_insertion_code": "",
    "pdb_residue_name": "SER",
    "uniprot_accession_id": "P12345",
    "uniprot_residue_number": 105,
    "uniprot_residue_name": "SER"
  },
  {
    "pdb_residue_number": 42,
    "pdb_residue_insertion_code": "A",
    "pdb_residue_name": "GLY",
    "uniprot_accession_id": "P12345",
    "uniprot_residue_number": 106,
    "uniprot_residue_name": "GLY"
  }
]
```

### `POST /map/uniprot` — UniProt to PDB mapping

Required fields:
- `uniprot_id`: UniProt accession (e.g., `P02185`).
- `residue`: Integer residue number.

Optional fields:
- `window`: Integer window size from `0`–`10` (default: `0`). Values outside this range return `{"error": "window must be an integer between 0 and 10"}` with HTTP 400.

Validation behavior:
- Missing required fields return `{"error": "Missing required field: <field>"}` with HTTP 400.
- Non-integer `residue` or `window` values return `"<field> must be an integer"` with HTTP 400.
- A valid request that finds no mapping returns `{"error": "No mapping found for the requested UniProt range"}` with HTTP 404.

Sample request:
```bash
curl -X POST http://127.0.0.1:5000/map/uniprot \
  -d "uniprot_id=P12345" \
  -d "residue=106" \
  -d "window=1"
```

Sample response:
```json
[
  {
    "pdb_accession_id": "1abc",
    "pdb_chain_id": "A",
    "pdb_residue_number": 105,
    "pdb_residue_insertion_code": "",
    "pdb_residue_name": "SER",
    "uniprot_residue_name": "SER"
  },
  {
    "pdb_accession_id": "1abc",
    "pdb_chain_id": "A",
    "pdb_residue_number": 106,
    "pdb_residue_insertion_code": "A",
    "pdb_residue_name": "GLY",
    "uniprot_residue_name": "GLY"
  }
]
```

## Development

### Running Tests
```bash
pytest tests/
```

### Exploring the Database
Jupyter notebooks in the `notebooks/` directory provide examples and testing procedures.

## License
MIT

## Contributors
Michele Bonus
