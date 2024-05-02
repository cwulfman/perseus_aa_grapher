import pytest
from pathlib import Path
from pdl_importer.importer import Importer




def test_importer():
    i = Importer()
    assert len(i.vases) == 0

    collection_data = Path("tests/data/collections.csv")
    i.import_collections(collection_data)
    assert i.get_collection('Indianapolis Museum of Art') is not None
    assert i.get_collection('Nothing Here') is None
