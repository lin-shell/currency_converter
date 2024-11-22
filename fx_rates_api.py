class InvalidCurrencyPairError(Exception):
    def __init__(self, ccy_pair: str):
        self.ccy_pair = ccy_pair
        self.message = f"Invalid currency pair: {ccy_pair}. Use 'get_all_pairs' for all available pairs."
        super().__init__(self.message)


class FXRatesAPI:
    BASE_URL = "https://example-fx.com"  # Example host

    def get_all_pairs(self) -> dict:
        pairs = {"pairs": ["EURGBP", "EURUSD", "GBPUSD", "USDCAD", "USDJPY"]}
        return pairs

    def get(self, params: dict) -> float:
        """
        Equivalent of requests.get(self.BASE_URL, params=params)
        """
        ccy_pair = params.get("ccy_pair")
        if ccy_pair is None:
            raise ValueError("ccy_pair is required in params")
        elif ccy_pair == "GBPUSD":
            return 1.28
        elif ccy_pair == "USDCAD":
            return 1.4
        elif ccy_pair == "EURGBP":
            return 0.83
        elif ccy_pair == "EURUSD":
            return 1.04
        elif ccy_pair == "USDJPY":
            return 154.31
        else:
            raise InvalidCurrencyPairError(ccy_pair)
