from fx_rates_api import FXRatesAPI, InvalidCurrencyPairError

from data.load import load_overwrites


class InvalidCurrencyRateError(Exception):
    def __init__(self, ccy_from: str, ccy_to: str):
        self.ccy_pair = ccy_from + ccy_to
        self.message = f"Invalid currency rate: {self.ccy_pair}. A currency rate for this pair is not available directly or with triangulation via USD."
        super().__init__(self.message)


class CurrencyConverter:
    def __init__(self):
        self.fx_client = FXRatesAPI()
        self.pairs = self.fx_client.get_all_pairs()["pairs"]

    def get_direct_rate(self, ccy_from: str, ccy_to: str) -> float:
        rates = load_overwrites()
        if rates.get(ccy_from + ccy_to):
            return rates[ccy_from + ccy_to]
        else:
            try:
                return self.fx_client.get({"ccy_pair": ccy_from + ccy_to})

            except InvalidCurrencyPairError as e:
                try:
                    return 1 / self.fx_client.get({"ccy_pair": ccy_to + ccy_from})

                except InvalidCurrencyPairError:
                    raise e

    def get_triangular_rate(self, ccy_from: str, ccy_to: str) -> float:
        if ccy_from != "USD" and ccy_to != "USD":
            rate_from = self.get_direct_rate(ccy_from, "USD")
            rate_to = self.get_direct_rate("USD", ccy_to)
            return rate_from * rate_to
        else:
            raise ValueError("ccy_from or ccy_to must not be 'USD'")

    def convert(self, ccy_from: str, ccy_to: str, quantity: float) -> float:
        if ccy_from == ccy_to:
            return quantity

        try:
            # Direct rate via API
            rate = self.get_direct_rate(ccy_from, ccy_to)
            return round(quantity * rate, 2)

        except InvalidCurrencyPairError:
            try:
                # Triangulation via USD
                rate = self.get_triangular_rate(ccy_from, ccy_to)
                return round(quantity * rate, 2)

            except InvalidCurrencyPairError:
                raise InvalidCurrencyRateError(ccy_from, ccy_to)
