import datetime
from .conftest import client

from schemas import schema_experiment

exp = {"id": "exp_1", "start_date": "2020-01-01"}


def test_add_experiment():
    response = client.post("addExperiment", json=exp)
    assert response.status_code == 201


def test_read_experiment():
    exps = [{"id": "exp_1", "start_date": "2020-01-01", "has_vids": False}]
    response = client.get("/experiments")
    assert response.status_code == 200
    assert response.json() == exps
