
"""Tests de performance pour la triangulation."""

import pytest

from triangulator import triangulation


# Test de performance pour la triangulation avec un grand nombre de points
@pytest.mark.perf
def test_perf_large_triangulation():
    """Test de performance pour la triangulation avec un grand nombre de points."""
    points = [(i, i) for i in range(10000)]
    result = triangulation(points)
    assert len(result) > 0

@pytest.mark.perf
def perf_small_triangulation():
    """Test de performance pour la triangulation avec un petit nombre de points."""
    points = [(i, i) for i in range(100)]
    result = triangulation(points)
    assert len(result) > 0

