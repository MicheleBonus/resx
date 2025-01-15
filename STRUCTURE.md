# ResX Project Structure

## Overview
ResX is a web service that provides fast residue cross-referencing between PDB and UniProt databases.

## Directory Structure
```
resx/
├── app.py              # Main Flask application
├── db/                 # Database handling
│   ├── __init__.py    # Database package initialization
│   └── sqlite.py      # SQLite database operations
├── static/            # Static web assets
│   └── style.css      # CSS styling
├── templates/         # Flask HTML templates
│   ├── base.html     # Base template with common elements
│   └── index.html    # Main interface template
├── notebooks/        # Development notebooks
│   ├── 01_initial_mapping_prototype.ipynb
│   └── 02_test_db_module.ipynb
├── tests/           # Test suite
│   ├── __init__.py
│   ├── conftest.py  # Test configurations
│   └── test_mapping.py
├── README.md        # Project documentation
├── STRUCTURE.md     # This file
└── requirements.txt # Project dependencies
```

## Component Descriptions

### Main Application
- `app.py`: Flask application entry point, contains route definitions and request handling

### Database Layer (`/db`)
- `sqlite.py`: Handles all database operations and connections
- `__init__.py`: Exposes database functionality to other parts of the application

### Web Interface (`/templates`, `/static`)
- `templates/base.html`: Base template with common HTML structure
- `templates/index.html`: Main interface template with forms and results display
- `static/style.css`: Custom styling for the web interface

### Development (`/notebooks`)
- Jupyter notebooks used during development for testing and prototyping
- Contains database exploration and API testing

### Testing (`/tests`)
- Contains pytest test suite
- Includes database and API endpoint tests

## Key Features
1. PDB to UniProt residue mapping
2. UniProt to PDB residue mapping
3. Support for residue ranges
4. Window-based residue lookup
5. Web interface for easy access