"""Test Asset and AssetPrice classes"""
import unittest
import pytest
from pyport.core.asset import Asset, AssetPrice


class TestAsset(unittest.TestCase):
    def setUp(self):
        class Dummy(Asset):
            def reprice(self, *_args, **_kwargs):
                return AssetPrice(self.name, price=100, date='1/1/2023')
        self.asset = Dummy('dummy')

    def test_asset_creation_fails(self):
        with pytest.raises(TypeError) as excinfo:
            _ = Asset('dummy')
        expected = "Can't instantiate abstract class Asset with abstract method reprice"
        assert str(excinfo.value) == expected

    def test_asset_price(self):
        price_info = self.asset.reprice()
        assert price_info.to_string() == 'Asset(dummy, 2023-01-01, 100)'
