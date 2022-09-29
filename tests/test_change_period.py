"""
test_change_period.py
Test script for PostgreSQL function change_period().
"""
import pytest

from tests.samples.change_period import EURGBP_M5
from tykee.data import Database
from tykee.market import Symbol, Period


@pytest.fixture
def load_data():
    """Loads data from PostgreSQL using function change_period()"""
    db = Database()
    df = db.get_symbol_history(
        Symbol.EURGBP, Period.M5, "2022-07-01 00:00:00", "2022-07-01 00:30:00"
    )
    db.close()
    return df


def test_change_period(load_data):
    """Tests if change_period() works correctly"""
    assert load_data.equals(EURGBP_M5)
