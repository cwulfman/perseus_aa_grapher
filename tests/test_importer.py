import pytest
from pathlib import Path
from pdl_importer.importer import Importer


def test_import_collections():
    i = Importer()

    collection_data = Path("tests/data/collections.csv")
    i.import_collections(collection_data)
    assert i.collection('Indianapolis Museum of Art') is not None
    assert i.collection('Nothing Here') is None


def test_import_data():
    i = Importer()
    collection_data = Path("tests/data/collections.csv")
    i.import_collections(collection_data)
    data = Path("tests/data/vases.json")
    i.import_data(data)
    assert len(i.artifacts) > 0


def test_import_images():
    i = Importer()
    data = Path("tests/data/test_images.json")
    collection_data = Path("tests/data/collections.csv")
    i.import_collections(collection_data)
    i.import_images(data)
    assert len(list(i.images)) > 0
    assert i.image('1990.30.0001').represents == "aa_1"


def test_export_vases():
    i = Importer()
    collection_data = Path("tests/data/collections.csv")
    i.import_collections(collection_data)
    data = Path("tests/data/vases.json")
    i.import_data(data)
    i.export_artifacts("/tmp/test_vases.ttl")


def test_export_collections():
    i = Importer()
    collection_data = Path("tests/data/collections.csv")
    i.import_collections(collection_data)
    i.export_collections("/tmp/test_collections.ttl")


def test_export_images():
    i = Importer()
    data = Path("tests/data/test_images.json")
    collection_data = Path("tests/data/collections.csv")
    i.import_collections(collection_data)
    i.import_images(data)
    i.export_images("/tmp/test_images.ttl")


def test_export_artifacts():
    i = Importer()
    collection_data = Path("tests/data/collections.csv")
    i.import_collections(collection_data)
    data = Path("tests/data/artifacts.json")
    i.import_data(data)
    i.export_artifacts("/tmp/test_artifacts.ttl")
