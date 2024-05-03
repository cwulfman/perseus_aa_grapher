import pytest
from pdl_importer.models import VaseData, CollectionData
from pdl_importer.entities import Vase

data = CollectionData(index="Malibu, The J. Paul Getty Museum",
                      name="foo",
                      entityid="bar",
                      uri="https://www.wikidata.org/wiki/Q731126")

collection_index = {"Malibu, The J. Paul Getty Museum": data}

def test_vase(vase_test_data):
    vase_data = VaseData(**vase_test_data['object'][0])
    vase = Vase(vase_data, collection_index)
    assert vase.str_id == "aa_3951"
    assert vase.collection.uri == "https://www.wikidata.org/wiki/Q731126"
