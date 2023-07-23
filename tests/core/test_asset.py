"""Test Asset and AssetPrice classes"""
import unittest
import pytest
from pyport import Asset, AssetPrice, AssetManager


class Dummy(Asset):
    def __init__(self, name):
        super().__init__(name, [])

    def reprice(self, *_args, **_kwargs):
        return AssetPrice(self.name, price=100, date='1/1/2023')


class TestAsset(unittest.TestCase):
    def setUp(self):
        self.asset = Dummy('dummy')
        self.manager = AssetManager()

    def tearDown(self):
        self.manager.reset()

    def test_asset_creation_fails(self):
        with pytest.raises(TypeError) as excinfo:
            _ = Asset('dummy')
        expected = "Can't instantiate abstract class Asset with abstract method reprice"
        assert str(excinfo.value) == expected

    def test_asset_price(self):
        price_info = self.asset.reprice()
        assert price_info.to_string() == 'Asset(dummy, 2023-01-01, 100)'

    def test_asset_from_market(self):
        asset = Dummy.from_market(market=None, name='test')
        assert isinstance(asset, Dummy)

    def test_from_market_registers_asset(self):
        _ = Dummy.from_market(None, 'test')
        assert 'test' in self.manager.assets

    def test___init___registers_asset(self):
        _ = Dummy('test')
        assert 'test' in self.manager.assets
