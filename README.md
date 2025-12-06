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

## API Endpoints

### PDB to UniProt Mapping
```
POST /map/pdb
Form data:
- pdb_id: PDB identifier (e.g., "101m")
- chain_id: Chain identifier (e.g., "A")
- residue: Residue number
- window: Number of surrounding residues (optional, maximum of 10)
```

### UniProt to PDB Mapping
```
POST /map/uniprot
Form data:
- uniprot_id: UniProt accession (e.g., "P02185")
- residue: Residue number
- window: Number of surrounding residues (optional, maximum of 10)
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
