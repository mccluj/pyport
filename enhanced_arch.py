class BufferETF:
    def __init__(self, config):
        self.config = config

    def solve(self):
        # Base buffer ETF solving logic
        return {"buffer": self.config.initial_buffer, "cap": self.config.cap}


class MaxBufferEnhancer:
    def __init__(self, buffer_etf, min_cap=0.03):
        self.base = buffer_etf
        self.min_cap = min_cap

    def solve(self):
        result = self.base.solve()
        if result["cap"] >= self.min_cap:
            return result
        else:
            # Recompute with min cap
            self.base.config.cap = self.min_cap
            return self.base.solve()


class FinancingEnhancer:
    def __init__(self, buffer_etf, strategy="etf", collateral="cash"):
        self.base = buffer_etf
        self.strategy = strategy
        self.collateral = collateral

    def solve(self):
        result = self.base.solve()
        # Apply financing layer
        result["financing"] = f"Replaced deep-ITM calls with {self.strategy} + {self.collateral}"
        return result


# ✨ Compose them arbitrarily:
config = Config(initial_buffer=1.0, cap=0.01)
etf = BufferETF(config)

# Apply max buffer logic
max_buffer_etf = MaxBufferEnhancer(etf)

# Apply financing logic on top
financed_max_buffer_etf = FinancingEnhancer(max_buffer_etf)

solution = financed_max_buffer_etf.solve()
print(solution)
