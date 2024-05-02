import pytest
import json


@pytest.fixture
def artifact_test_data():
    with open('tests/data/artifacts.json') as f:
        return json.load(f)


@pytest.fixture
def vase_test_data():
    with open('tests/data/vases.json') as f:
        return json.load(f)
