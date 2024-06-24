import pytest
from rdflib import URIRef
from pdl_importer.models import VaseData, CollectionData
from pdl_importer.entities import Vase, Collection

data = CollectionData(index="Malibu, The J. Paul Getty Museum",
                      name="foo",
                      entityid="bar",
                      uri="https://www.wikidata.org/wiki/Q731126")

collection_index = {"Malibu, The J. Paul Getty Museum": Collection(data)}

def test_vase(vase_test_data):
    vase_data = VaseData(**vase_test_data['object'][0])
    fields = vase_data.model_dump()
    live_fields = [f for f in fields.keys() if fields[f] ]
    assert len(live_fields) == 12
    vase = Vase(vase_data, collection_index)
    assert vase.str_id == "aa_3951"
    assert vase.collection.id == URIRef("https://www.wikidata.org/wiki/Q731126")
