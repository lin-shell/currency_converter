import pytest

from currency_converter import CurrencyConverter, InvalidCurrencyRateError
from fx_rates_api import InvalidCurrencyPairError


class TestCurrencyConverter:
    ccy_cnv = CurrencyConverter()

    def test_get_direct_rate(self):
        assert self.ccy_cnv.get_direct_rate("GBP", "USD") == 1.28
        assert self.ccy_cnv.get_direct_rate("USD", "GBP") == 1 / 1.28

        ccy_from = "GBP"
        ccy_to = "JPY"
        with pytest.raises(
            InvalidCurrencyPairError,
            match=InvalidCurrencyPairError(ccy_from + ccy_to).message
        ):
            self.ccy_cnv.get_direct_rate(ccy_from, ccy_to)

    def test_get_triangular_rate(self):
        assert self.ccy_cnv.get_triangular_rate("GBP", "CAD") == 1.28 * 1.4
        assert self.ccy_cnv.get_triangular_rate("CAD", "JPY") == 154.31 / 1.4

        with pytest.raises(ValueError):
            self.ccy_cnv.get_triangular_rate("GBP", "USD")

        with pytest.raises(ValueError):
            self.ccy_cnv.get_triangular_rate("USD", "EUR")

        with pytest.raises(InvalidCurrencyPairError):
            self.ccy_cnv.get_triangular_rate("GBP", "NZD")

    def test_convert(self):
        assert self.ccy_cnv.convert("USD", "GBP", 1000) == 781.25
        assert self.ccy_cnv.convert("GBP", "CAD", 1000) == 1792

        with pytest.raises(InvalidCurrencyRateError):
            self.ccy_cnv.convert("GBP", "NZD", 1000)
