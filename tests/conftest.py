"""Create fixtures needed by multiple test files"""
import pytest
import numpy as np
from backend.analysis.tissues import TissuePoints

@pytest.fixture(name='tissue_object')
def fixture_tissue_object():
    """Initalize a sine graph based object"""
    time = np.arange(0, 40, 0.001)
    disp = np.sin(time) + 1
    return TissuePoints(disp,  time)
