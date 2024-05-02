import pytest

from pdl_importer.models import VaseData

__author__ = "Cliff Wulfman"
__copyright__ = "Cliff Wulfman"
__license__ = "MIT"


def test_vase_data(vase_test_data):
    assert vase_test_data['object'][0]['id'] == "aa_3951"


def test_vase_data_object(vase_test_data):
    a_vase = VaseData(**vase_test_data['object'][0])
    assert a_vase.name == "Malibu 86.AE.34"
