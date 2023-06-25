import pytest
from pyport.core.asset import Asset


def test_asset_creation_fails():
    with pytest.raises(TypeError) as excinfo:
        _ = Asset('dummy')
    expected = "Can't instantiate abstract class Asset with abstract method reprice"
    assert str(excinfo.value) == expected
