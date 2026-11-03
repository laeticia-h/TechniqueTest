"""Test erreurs pour la triangulation."""
import pytest

from triangulator import triangulation


# Test le cas avec un caractère ( NotaNumber)
def test_not_a_number():
    """Test le cas d'une entrée avec un caractère (NotaNumber)."""
    pts = [(0, 0), (1, 0), (1, 1), (0, 1), ('a', 2)]
    with pytest.raises(ValueError):
        triangulation(pts)

# Test le cas de points avec 3 coordonnées
def test_three_coordonnees():
    """Test le cas d'une entrée avec 3 coordonnées."""
    pts = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
    with pytest.raises(ValueError):
        triangulation(pts)

def test_point_one_coordonnes():
    """Test le cas d'une entrée avec un point avec une seule coordonnée."""
    pts = [(0, 0), (1, 0), (0,)]
    with pytest.raises(ValueError):
        triangulation(pts)

def test_without_points():
    """Test le cas d'une entrée sans points."""
    with pytest.raises(ValueError):
        triangulation(None)


def test_not_a_list():
    """Test le cas d'une entrée qui n'est pas une liste."""
    pts = 27
    with pytest.raises(ValueError):
        triangulation(pts)
