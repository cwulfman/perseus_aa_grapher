import pytest
from pdl_importer.models import VaseData
from pdl_importer.entities import Vase


def test_vase(vase_test_data):
    vase_data = VaseData(**vase_test_data['object'][0])
    vase = Vase(vase_data)
    assert vase.str_id == "aa_3951"
