"""
    Dummy conftest.py for pdl_importer.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""

import pytest
import json


@pytest.fixture
def artifact_test_data():
    with open('tests/data/artifacts.json') as f:
        return json.load(f)
