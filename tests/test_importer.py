import pytest
from pathlib import Path
from pdl_importer.importer import Importer




def test_import_collections():
    i = Importer()
    assert len(i.vases) == 0

    collection_data = Path("tests/data/collections.csv")
    i.import_collections(collection_data)
    assert i.collection('Indianapolis Museum of Art') is not None
    assert i.collection('Nothing Here') is None


def test_import_data():
    i = Importer()
    data = Path("tests/data/vases.json")
    i.import_data(data)
    assert len(i.vases) > 0


def test_import_images():
    i = Importer()
    data = Path("tests/data/test_images.json")
    i.import_images(data)
    assert len(i.images) > 0
    assert i.image('1990.30.0001').represents == "aa_1"
