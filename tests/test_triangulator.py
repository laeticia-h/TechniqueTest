"""Test unitaires pour la triangulation."""
import pytest

from triangulator import (
    decode_pointset,
    encode_pointset,
    encode_triangles,
    triangulation,
)


#Test le cas de 3 points donne 1 triangle
def test_triangle():
    """Test le cas de 3 points qui forment un triangle."""
    pts = [(0, 0), (1, 0), (0, 1)]
    triangles = triangulation(pts)
    
    assert len(triangles) == 1
    assert triangles[0] == (0, 1, 2)

# Test le cas d'un quadrilatère qui doit me donner 2 triangles
def test_quadrilatere():
    """Test le cas d'un quadrilatère qui doit me donner 2 triangles."""
    pts = [(0, 0), (1, 0), (1, 1), (0, 1)]
    result = triangulation(pts)
    
    assert len(result) == 2


# Test le cas d'un pentagone
def test_pentagone():
    """Test le cas d'un pentagone qui doit me donner 3 triangles."""
    pts = [(0, 0), (1, 0), (2, 1), (1, 2), (0, 1)]
    triangles = triangulation(pts)

    assert len(triangles) == 3

#Test le cas de points alignés (liste vide)
def test_aligned_points():
    """Test le cas de points alignés qui ne peuvent pas former de triangle."""
    pts = [(0, 0), (1, 0), (2, 0)]
    result = triangulation(pts)


    assert result == []

# Test de aucun point (liste vide)
def test_empty():
    """Test le cas d'aucun point."""
    assert triangulation([]) == []

# Test avec un seul point ( liste vide)
def test_single_point():
    """Test le cas d'un seul point."""
    assert triangulation([(0, 0)]) == []

# Test avec deux points ( liste vide)
def test_two_points():
    """Test le cas de deux points."""
    assert triangulation([(0, 0), (1, 0)]) == []

#Fonction qui  transforme un nombre en bytes
def transform_to_bytes(nombres):
    """Fonction qui transforme une liste de nombres en bytes."""
    result = b""
    for nb in nombres:
        octet0 = nb % 256
        octet1 = (nb // 256) % 256
        octet2 = (nb // 65536) % 256
        octet3 = (nb // 16777216) % 256

        nombre_bytes = bytes([octet0]) 
        + bytes([octet1])
        + bytes([octet2]) + bytes([octet3])
        result = result + nombre_bytes
    return result


# Les floats utilisés pour les tests d'encodage et de décodage des coordonnées
FLOATS = (
    transform_to_bytes([3])        
    + b"\x00\x00\xa0\x40"          # 5.0
    + b"\x00\x00\x00\x40"          # 2.0
    + b"\x00\x00\x00\x41"          # 8.0
    + b"\x00\x00\x80\x3f"          # 1.0
    + b"\x00\x00\x80\x40"          # 4.0
    + b"\x00\x00\xe0\x40"          # 7.0
)


# Test la transformation en byte avec un seul triangle (encodage du triangle)
def test_encode_simple_triangle():
    """Test la transformation en byte avec un seul triangle."""
    points = [(5.0, 2.0), (8.0, 1.0), (4.0, 7.0)]
    triangles = [(0, 1, 2)]

    result = encode_triangles(points, triangles)
    expected = (FLOATS + transform_to_bytes([1]) 
                + transform_to_bytes([0, 1, 2]))

    assert result == expected


#  Test la transformation en byte avec 3 points (décodage des coordonnées)
def test_decode_simple_pointset():
    """Test la transformation en byte avec 3 points (décodage des coordonnées)."""
    points = [(5.0, 2.0), (8.0, 1.0), (4.0, 7.0)]
    result = decode_pointset(FLOATS)
    assert result == points

# Test la transformation en byte avec 3 points (encodage des coordonnées)
def test_encode_simple_pointset():
    """Test la transformation en byte avec 3 points (encodage des coordonnées)."""
    points = [(5.0, 2.0), (8.0, 1.0), (4.0, 7.0)]

    result = encode_pointset(points)
    expected = FLOATS

    assert result == expected

#  Test avec des coordonnées négatives 
def test_coordonnees_negatives():
    """Test le cas d'un encodage et décodage avec des coordonnées négatives."""
    points = [(-3.5, -2.0), (1.25, -1.0), (0.0, 4.5)]
    assert len(triangulation(points)) == 1

# Test le cas d'un encodage et décodage avec des coordonnées négatives
def test_encode_decode_negatifs():
    """Test le cas d'un encodage et décodage avec des coordonnées négatives."""
    points = [(-3.0, -2.0), (5.0, -1.5), (-4.0, 6.0)]
    assert decode_pointset(encode_pointset(points)) == points

# Test le cas d'un encodage avec pas de triangle (liste vide)
def test_encode_triangles_without_triangle():
    """Test le cas d'un encodage avec pas de triangle (liste vide)."""
    points = [(5.0, 2.0), (8.0, 1.0), (4.0, 7.0)]
    assert encode_triangles(points, []) == FLOATS + transform_to_bytes([0])

# Test le cas d'un décodage avec des données corrompues (moins d'octets)
def test_decode_corrupted_binary():
    """Test le cas d'un décodage avec des données corrompues (moins d'octets)."""
    corrupted = transform_to_bytes([2]) + b"\xFF\xFF\xAA"  
    with pytest.raises(ValueError):
        decode_pointset(corrupted)

def test_decode_wrong_size():
    """Test le cas d'un décodage avec des données corrompues (taille incorrecte)."""
    data = FLOATS + b"\x00\x00\x80\x3f"  
    with pytest.raises(ValueError):
        decode_pointset(data)