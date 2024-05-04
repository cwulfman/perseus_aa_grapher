import pytest
from rdflib import URIRef
from pdl_importer.models import GemData, CollectionData
from pdl_importer.entities import Gem, Collection


data = CollectionData(index="Museum of Fine Arts, Boston",
                      name="foo",
                      entityid="bar",
                      uri="https://example.org/q1")

collection_index = {"Museum of Fine Arts, Boston": Collection(data)}


def test_gem(gem_test_data):
    gem_data = GemData(**gem_test_data['object'][0])
    gem = Gem(gem_data, collection_index)
    assert gem.str_id == "aa_1730"
