"""Create fixtures needed by multiple test files"""
import pytest
import numpy as np
from backend.analysis.tissues import TissuePoints

@pytest.fixture(name='tissue_object')
def fixture_tissue_object():
    """Initalize a sine graph based object"""
    time = np.arange(0, 40, 0.001)
    disp = np.sin(time) + 4
    tissue_obj = TissTemp()
    return TissuePoints(disp,  time, tissue_obj)

class TissTemp:
    """Sample tissue"""
    def __init__(self):
        self.post = PostTemp()

class PostTemp:
    """Sample post steup"""
    def __init__(self):
        self.radius = .277
        self.left_post_height = 3
        self.left_tissue_height = 2.8
        self.right_post_height = 3
        self.right_tissue_height = 2.8
         