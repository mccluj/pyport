class TestAssetHashingBase(unittest.TestCase):

    def create_asset(self, **kwargs):
        """Factory method to create an instance of the specific asset class."""
        raise NotImplementedError("This method should be overridden in a subclass")

    def test_hash_consistency(self):
        asset = self.create_asset()
        self.assertEqual(hash(asset), hash(asset), "Hash value should be consistent across multiple calls.")

    def test_equal_objects_have_same_hash(self):
        asset1 = self.create_asset()
        asset2 = self.create_asset()
        self.assertEqual(hash(asset1), hash(asset2), "Equal objects must have the same hash value.")

    def test_unequal_objects_have_different_hash(self):
        # Create two assets that differ in one attribute at a time to ensure proper hashing
        attributes_to_test = self.get_test_attributes()
        for attribute, differing_value in attributes_to_test.items():
            kwargs = self.default_kwargs()
            kwargs[attribute] = differing_value
            asset1 = self.create_asset()
            asset2 = self.create_asset(**kwargs)
            self.assertNotEqual(hash(asset1), hash(asset2), f"Objects differing in '{attribute}' should have different hash values.")

    def test_hash_works_in_set(self):
        asset1 = self.create_asset()
        asset2 = self.create_asset()
        asset_set = {asset1}
        self.assertIn(asset2, asset_set, "Equal objects should be considered the same in a set.")

    def get_test_attributes(self):
        """Override this in subclasses to provide a dict of attributes to test for uniqueness."""
        raise NotImplementedError("This method should be overridden in a subclass")
    
    def default_kwargs(self):
        """Override this in subclasses to provide default keyword arguments for asset creation."""
        raise NotImplementedError("This method should be overridden in a subclass")

# Specific test cases for each Asset subclass
class TestStockHashing(TestAssetHashingBase):

    def create_asset(self, **kwargs):
        # Provide defaults for Stock; kwargs can override these
        return Stock(name=kwargs.get("name", "CompanyA"), asset_type=kwargs.get("asset_type", "Equity"), 
                     price=kwargs.get("price", 100.0), ticker=kwargs.get("ticker", "CMPA"), 
                     exchange=kwargs.get("exchange", "NYSE"))

    def get_test_attributes(self):
        return {
            'name': 'CompanyB',
            'asset_type': 'Bond',
            'price': 200.0,
            'ticker': 'CMPB',
            'exchange': 'NASDAQ'
        }

    def default_kwargs(self):
        return {
            'name': 'CompanyA',
            'asset_type': 'Equity',
            'price': 100.0,
            'ticker': 'CMPA',
            'exchange': 'NYSE'
        }

# Additional test classes for other Asset types can be added similarly.

if __name__ == '__main__':
    unittest.main()
