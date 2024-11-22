import pytest

from fx_rates_api import FXRatesAPI, InvalidCurrencyPairError


class TestFXRatesAPI:
    fx_client = FXRatesAPI()

    def test_get_all_pairs(self):
        expected = {"pairs": ["EURGBP", "EURUSD", "GBPUSD", "USDCAD", "USDJPY"]}
        output = self.fx_client.get_all_pairs()
        assert output == expected

    def test_get(self):
        with pytest.raises(
            ValueError,
            match="ccy_pair is required in params"
        ):
            self.fx_client.get({})

        ccy_pair_error = "PLNUSD"
        with pytest.raises(
            InvalidCurrencyPairError,
            match=InvalidCurrencyPairError(ccy_pair_error).message
        ):
            self.fx_client.get({"ccy_pair": "PLNUSD"})

        assert self.fx_client.get({"ccy_pair": "GBPUSD"}) == 1.28
