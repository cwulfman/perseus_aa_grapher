import pytest

from pdl_importer.models import VaseData

__author__ = "Cliff Wulfman"
__copyright__ = "Cliff Wulfman"
__license__ = "MIT"


def test_vase_data(artifact_test_data):
    assert artifact_test_data['object'][0]['xml:id'] == "aa_1"
