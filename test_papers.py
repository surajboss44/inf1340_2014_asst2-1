#!/usr/bin/env python3

""" Module to test papers.py  """

__author__ = 'Susan Sim'
__email__ = "ses@drsusansim.org"

__copyright__ = "2014 Susan Sim"
__license__ = "MIT License"

__status__ = "Prototype"

# imports one per line
import pytest
from papers import decide


def test_basic():
    assert decide("test_returning_citizen.json", "watchlist.json", "countries.json") == ["Accept", "Accept"]
    assert decide("test_watchlist.json", "watchlist.json", "countries.json") == ["Secondary"]
    assert decide("test_quarantine.json", "watchlist.json", "countries.json") == ["Quarantine"]


def test_files():
    with pytest.raises(FileNotFoundError):
        decide("test_returning_citizen.json", "", "countries.json")


"""function to check if incomplete traveller entries are handled by the program code"""


def test_completeness():
    assert decide("test_completeness.json", "watchlist.json", "countries.json") == ["Reject", "Reject", "Reject"]


"""Function to check if traveler entries are handled based upon their reason of visit. """


def test_entry_reason():
    assert decide("test_entry_reason.json", "watchlist.json", "countries.json") == ['Reject', 'Reject', 'Accept']


"""Function to check if travellers with invalid passports get rejected"""


def test_invalid_passport():
    assert decide("test_invalid_passport.json", "watchlist.json", "countries.json") == ["Reject", "Reject"]


"""Function to check if travellers with invalid visas get rejected"""


def test_invalid_passport():
    assert decide("test_invalid_visa.json", "watchlist.json", "countries.json") == ["Reject", "Reject"]


""" To test if a JSON file that does not exist is handled"""


def test_missing_file():
    with pytest.raises(FileNotFoundError):
        decide("test_json_file.json", "watchlist.json", "countries.json")

""" To test if a JSON file with invalid values is handled"""


def test_invalid_file():
    with pytest.raises(ValueError):
        decide("test_invalid_file.json", "watchlist.json", "countries.json")

