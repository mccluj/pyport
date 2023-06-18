import pytest
from pyport.assets.asset import Asset


def test_asset_creation_fails():
    with pytest.raises(TypeError) as excinfo:
        _ = Asset('dummy')
    assert str(excinfo.value) == "Can't instantiate abstract class Asset with abstract methods reprice, unit_price"