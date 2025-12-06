import polars as pl


def test_map_pdb_missing_fields(client):
    response = client.post('/map/pdb', data={'chain_id': 'A', 'residue': '10'})
    assert response.status_code == 400
    assert 'pdb_id' in response.get_json()['error']


def test_map_pdb_invalid_numbers(client):
    response = client.post('/map/pdb', data={'pdb_id': '1abc', 'chain_id': 'A', 'residue': 'x'})
    assert response.status_code == 400
    assert 'integer' in response.get_json()['error']

    response = client.post('/map/pdb', data={'pdb_id': '1abc', 'chain_id': 'A', 'residue': '1', 'window': '-5'})
    assert response.status_code == 400
    assert 'window' in response.get_json()['error']


def test_map_pdb_window_too_large(client):
    response = client.post(
        '/map/pdb',
        data={'pdb_id': '1abc', 'chain_id': 'A', 'residue': '1', 'window': '11'}
    )
    assert response.status_code == 400
    assert response.get_json()['error'] == 'window must be an integer between 0 and 10'


def test_map_pdb_insertion_code_length(client):
    response = client.post(
        '/map/pdb',
        data={'pdb_id': '1abc', 'chain_id': 'A', 'residue': '1', 'insertion_code': 'AB'}
    )
    assert response.status_code == 400
    assert 'insertion_code' in response.get_json()['error']


def test_map_pdb_not_found(client, mock_polars):
    mock_polars(pl.DataFrame())
    response = client.post('/map/pdb', data={'pdb_id': '1abc', 'chain_id': 'A', 'residue': '10'})
    assert response.status_code == 404
    assert 'No mapping found' in response.get_json()['error']


def test_map_uniprot_missing_fields(client):
    response = client.post('/map/uniprot', data={'residue': '5'})
    assert response.status_code == 400
    assert 'uniprot_id' in response.get_json()['error']


def test_map_uniprot_invalid_numbers(client):
    response = client.post('/map/uniprot', data={'uniprot_id': 'P12345', 'residue': 'abc'})
    assert response.status_code == 400
    assert 'integer' in response.get_json()['error']


def test_map_uniprot_window_too_large(client):
    response = client.post('/map/uniprot', data={'uniprot_id': 'P12345', 'residue': '5', 'window': '15'})
    assert response.status_code == 400
    assert response.get_json()['error'] == 'window must be an integer between 0 and 10'


def test_map_uniprot_not_found(client, mock_polars):
    mock_polars(pl.DataFrame())
    response = client.post('/map/uniprot', data={'uniprot_id': 'P12345', 'residue': '5', 'window': '0'})
    assert response.status_code == 404
    assert 'No mapping found' in response.get_json()['error']
