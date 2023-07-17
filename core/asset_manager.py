"""AssetManager is maintains the definitions and repricing duties for all assets.
Assets are registered with AssetManager using the asset name as the key.
Pricing is lazy evaluation relying on asset dependencies.
"""


class AssetManager:
    def __init__(self):
        self.assets = []
        self.prices = {}

    def add_asset(self, asset):
        self.assets.append(asset)

    def calculate_price(self, asset, market):
        if asset.name in self.prices:
            return self.prices[asset.name]

        dependencies_satisfied = all(
            dependency in self.prices for dependency in asset.dependencies
        )

        if not dependencies_satisfied:
            for dependency in asset.dependencies:
                if dependency not in self.prices:
                    dependency_asset = next(
                        a for a in self.assets if a.name == dependency
                    )
                    self.calculate_price(dependency_asset, market)

        asset_price = self.calculate_asset_price(asset, market)
        self.prices[asset.name] = asset_price

        return asset_price

    def calculate_asset_price(self, asset, market):
        return 10 * len(asset.dependencies)

    def lazy_price(self, market):
        for asset in self.assets:
            if asset.name not in self.prices:
                self.calculate_price(asset, market)
        for asset in self.assets:
            yield asset.name, self.prices[asset.name]

    def reprice_assets(self, market):
        for asset_name, asset_price in self.lazy_price(market):
            print(f"{asset_name}: {asset_price}")


if __name__ == '__main__':
    class Asset:
        def __init__(self, name, dependencies):
            self.name = name
            self.dependencies = dependencies


    manager = AssetManager()

    manager.add_asset(Asset("Asset 3", ["Asset 1", "Asset 2"]))
    manager.add_asset(Asset("Asset 1", []))
    manager.add_asset(Asset("Asset 2", ["Asset 1"]))

    manager.reprice_assets(None)
    print(manager.prices)
