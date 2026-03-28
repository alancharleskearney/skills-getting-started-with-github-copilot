import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(scope="function")
def client():
    original_data = copy.deepcopy(app_module.activities)
    with TestClient(app_module.app) as c:
        yield c
    app_module.activities = original_data