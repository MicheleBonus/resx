import sqlite3
from functools import lru_cache
from pathlib import Path
from typing import Generator
from contextlib import contextmanager

# Database configuration
DATABASE_PATH = "C:/Users/Miche/Desktop/TopUniPDBMapper/topunipdbmapper.db"

class DatabaseError(Exception):
    """Base class for database-related errors"""
    pass

class DatabaseConnectionError(DatabaseError):
    """Raised when database connection fails"""
    pass

@contextmanager
def get_db() -> Generator[sqlite3.Connection, None, None]:
    """
    Create and manage a database connection using a context manager.
    
    Returns:
        sqlite3.Connection: Database connection object
        
    Raises:
        DatabaseConnectionError: If connection cannot be established
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        # Enable foreign keys
        conn.execute("PRAGMA foreign_keys = ON")
        yield conn
    except sqlite3.Error as e:
        raise DatabaseConnectionError(f"Failed to connect to database: {str(e)}")
    finally:
        if 'conn' in locals():
            conn.close()

def initialize_db():
    """
    Initialize database with required indexes.
    Should be called on application startup.
    """
    try:
        with get_db() as conn:
            # Index for PDB lookups
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_pdb_lookup 
                ON residues (
                    pdb_accession_id, 
                    pdb_chain_id, 
                    pdb_residue_number,
                    pdb_residue_insertion_code
                )
            """)
            
            # Index for UniProt lookups
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_uniprot_lookup 
                ON residues (
                    uniprot_accession_id, 
                    uniprot_residue_number
                )
            """)
            
            conn.commit()
    except sqlite3.Error as e:
        raise DatabaseError(f"Failed to initialize database: {str(e)}")

def verify_database():
    """
    Verify database existence and basic structure.
    Returns basic statistics about the database.
    """
    try:
        with get_db() as conn:
            # Check if residues table exists
            table_check = conn.execute("""
                SELECT name 
                FROM sqlite_master 
                WHERE type='table' AND name='residues'
            """).fetchone()
            
            if not table_check:
                raise DatabaseError("Required table 'residues' not found in database")
            
            # Get basic statistics
            stats = {
                'total_entries': conn.execute("SELECT COUNT(*) FROM residues").fetchone()[0],
                'unique_pdbs': conn.execute(
                    "SELECT COUNT(DISTINCT pdb_accession_id) FROM residues"
                ).fetchone()[0],
                'unique_uniprots': conn.execute(
                    "SELECT COUNT(DISTINCT uniprot_accession_id) FROM residues"
                ).fetchone()[0]
            }
            
            return stats
    except sqlite3.Error as e:
        raise DatabaseError(f"Database verification failed: {str(e)}")

def optimize_db():
    """
    Optimize database by running ANALYZE and VACUUM.
    Should be called periodically for maintenance.
    """
    try:
        with get_db() as conn:
            conn.execute("ANALYZE")
            conn.execute("VACUUM")
    except sqlite3.Error as e:
        raise DatabaseError(f"Database optimization failed: {str(e)}")

# Optional: Cache frequently accessed data
@lru_cache(maxsize=1000)
def get_pdb_chains(pdb_id: str) -> list:
    """
    Get all chains for a given PDB ID.
    Cached for performance.
    """
    try:
        with get_db() as conn:
            chains = conn.execute(
                """
                SELECT DISTINCT pdb_chain_id 
                FROM residues 
                WHERE pdb_accession_id = ?
                ORDER BY pdb_chain_id
                """, 
                (pdb_id.lower(),)
            ).fetchall()
            return [chain[0] for chain in chains]
    except sqlite3.Error as e:
        raise DatabaseError(f"Failed to get chains for PDB {pdb_id}: {str(e)}")