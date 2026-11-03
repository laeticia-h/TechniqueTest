"""Tests unitaires pour l'API de triangulation."""

from flask import Flask 
import pytest

from triangulator import create_app, encode_pointset

URL = "/triangulation/123e4567-e89b-12d3-a456-426614174000"

manager = Flask("pointset_manager")

@manager.route("/pointset/<pointset_id>")

def get_pointset(pointset_id):
    """Faux PointSeetManager qui retourne le poinset."""
    return manager.config["DATA"], manager.config["STATUS"]

def fetch_manager_data(pointset_id):
    """Fonction qui simule la récupération d'un pointset par son ID."""
    response = manager.test_client().get("/pointset/"+pointset_id)
    if response.status_code == 404:
        raise ValueError("PointSet not found")
    elif response.status_code == 200:
        return response.data

@pytest.fixture
def client():
    """Fixture pour créer un client de test Flask."""
    return create_app(fetch_manager_data).test_client()

# Test le cas d'un id invalide
def test_api_triangulation_invalid_uuid(client):
    """Test le cas d'un id invalide."""
    response =  client.get("/triangulation/invalid_uuid")
    assert response.status_code == 400
    assert "code" in response.json()
    assert "message" in response.json()

# Test le cas d'une route non trouvée
def test_api_triangulation_not_found(client):
    """Test le cas d'une route non trouvée."""
    response = client.get("/non_existent_endpoint")
    assert response.status_code == 404
    assert "code" in response.json()
    assert "message" in response.json()

# Test le cas d'un pointset non trouvé par le PointSetManager
def test_api_pointset_not_found(client):
    """Test le cas d'un pointset non trouvé par le PointSetManager."""
    manager.config["STATUS"] = 404
    manager.config["DATA"] = b""

    response = client.get(URL)
    assert response.status_code == 404
    assert "code" in response.json()
    assert "message" in response.json()

# Test le cas de 3 points donne un triangle
def test_api_triangulate(client):
    """Test le cas de 3 points qui forment un triangle."""
    pointset = encode_pointset([(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)])
    manager.config["STATUS"] = 200
    manager.config["DATA"] = pointset
 
    response = client.get(URL)
    assert response.status_code == 200
    

# Test le cas d'un pointset vide
def test_api_triangulate_empty_input(client):
    """Test le cas d'un pointset vide."""
    manager.config["STATUS"] = 200
    manager.config["DATA"] = encode_pointset([])
 
    response = client.get(URL)
 
    assert response.status_code == 500
    assert "code" in response.json
    assert "message" in response.json

# Test le cas d'un flux de données corrompu 
def test_api_triangulate_invalid_input(client):
    """Test le cas d'un flux de données corrompu."""
    manager.config["STATUS"] = 200
    manager.config["DATA"] = b"\x00\x00\x0e"
 
    response = client.get(URL)
 
    assert response.status_code == 503
    assert "code" in response.json
    assert "message" in response.json


 # Test le cas d'une entrée avec un caractère (NotaNumber)
def test_api_triangulate_not_a_number(client):
    """Test le cas d'une entrée avec un caractère (NotaNumber)."""
    manager.config["STATUS"] = 200
    manager.config["DATA"] = encode_pointset([(0, 0), (1, 0), (1, 1), (0, 1), ('a', 2)])
 
    response = client.get(URL)
 
    assert response.status_code == 500
    assert response.json()["code"] == "TRIANGULATION_FAILED"



# Test PointSetManager sans réponse
def test_api_pointset_manager_no_response(client):
    """Test le cas d'une absence de réponse du PointSetManager."""
    manager.config["STATUS"] = 503
    manager.config["DATA"] = b""
 
    response = client.get(URL)

    assert response.status_code == 503
    assert "code" in response.json
    assert "message" in response.json

# Test PointSetManager avec une erreur de serveur
def test_api_pointset_manager_server_error():
    """Test le cas d'une erreur de serveur du PointSetManager."""
    manager.config["STATUS"] = 500
    manager.config["DATA"] = b""
 
    response = client.get(URL)

    assert response.status_code == 503
    assert "code" in response.json
    assert "message" in response.json

