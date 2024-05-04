import pytest
import json
from csv import DictReader
from pdl_importer.models import CollectionData


@pytest.fixture
def artifact_test_data():
    with open('tests/data/artifacts.json') as f:
        return json.load(f)


@pytest.fixture
def vase_test_data():
    with open('tests/data/vases.json') as f:
        return json.load(f)

@pytest.fixture
def gem_test_data():
    with open('tests/data/gems.json') as f:
        return json.load(f)


@pytest.fixture
def collection_test_data():
    collections = {}
    with open("tests/data/collections.csv") as f:
        reader = DictReader(f)
        for row in reader:
            c = CollectionData(**row)
            collections[c.index] = c
    return collections
