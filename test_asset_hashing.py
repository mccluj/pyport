import pytest

# Assuming Stock and Bond classes are already defined similarly as before

@pytest.fixture
def stock():
    return Stock(name="CompanyA", asset_type="Equity", price=100.0, ticker="CMPA", exchange="NYSE")

@pytest.fixture
def bond():
    return Bond(name="BondA", asset_type="Debt", price=1000.0, maturity_date="2030-01-01", coupon_rate=5.0)

@pytest.mark.parametrize("asset_fixture", ["stock", "bond"])
def test_hash_consistency(asset_fixture, request):
    asset = request.getfixturevalue(asset_fixture)
    assert hash(asset) == hash(asset), "Hash value should be consistent across multiple calls."

@pytest.mark.parametrize("asset_fixture", ["stock", "bond"])
def test_equal_objects_have_same_hash(asset_fixture, request):
    asset1 = request.getfixturevalue(asset_fixture)
    asset2 = request.getfixturevalue(asset_fixture)
    assert hash(asset1) == hash(asset2), "Equal objects must have the same hash value."

@pytest.mark.parametrize("asset_fixture", ["stock", "bond"])
def test_unequal_objects_have_different_hash(asset_fixture, request):
    asset1 = request.getfixturevalue(asset_fixture)
    asset2 = request.getfixturevalue(asset_fixture)
    if isinstance(asset1, Stock):
        asset2 = Stock(name="CompanyB", asset_type="Equity", price=100.0, ticker="CMPB", exchange="NYSE")
    elif isinstance(asset1, Bond):
        asset2 = Bond(name="BondB", asset_type="Debt", price=1000.0, maturity_date="2035-01-01", coupon_rate=4.5)
    assert hash(asset1) != hash(asset2), "Unequal objects should generally have different hash values."

@pytest.mark.parametrize("asset_fixture", ["stock", "bond"])
def test_hash_works_in_set(asset_fixture, request):
    asset1 = request.getfixturevalue(asset_fixture)
    asset2 = request.getfixturevalue(asset_fixture)
    asset_set = {asset1}
    assert asset2 in asset_set, "Equal objects should be considered the same in a set."
