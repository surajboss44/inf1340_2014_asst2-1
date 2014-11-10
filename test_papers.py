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


def test_completeness():
    """function to check if incomplete traveller entries are handled by the program code"""
    assert decide("test_completeness.json", "watchlist.json", "countries.json") == ["Reject", "Reject", "Reject"]


def test_entry_reason():
    """Function to check if traveler entries are handled based upon their reason of visit. """
    assert decide("test_entry_reason.json", "watchlist.json", "countries.json") == ['Reject', 'Reject', 'Accept']


def test_invalid_passport():
    """Function to check if travellers with invalid passports get rejected"""
    assert decide("test_invalid_passport.json", "watchlist.json", "countries.json") == ["Reject", "Reject"]


def test_invalid_visa():
    """Function to check if travellers with invalid visas get rejected"""
    assert decide("test_invalid_visa.json", "watchlist.json", "countries.json") == ["Reject", "Reject"]


def test_missing_file():
    """ To test if a JSON file that does not exist is handled"""
    with pytest.raises(FileNotFoundError):
        decide("test_json_file.json", "watchlist.json", "countries.json")


def test_invalid_file():
    """ To test if a JSON file with invalid values is handled"""
    with pytest.raises(ValueError):
        decide("test_invalid_file.json", "watchlist.json", "countries.json")


def test_invalid_keys():
    """ To test for missing keys in the JSON file. Entries with missing keys will fail the completeness test\
 unless there is enough information for a failed medical advisory."""
    decide("test_invalid_keys.json", "watchlist.json", "countries.json") == ["Quarantine", "Reject"]


def test_invalid_date():
    """ To test for invalid date format in the traveller birth date and visa date"""
    decide("test_invalid_date.json", "watchlist.json", "countries.json") == ["Quarantine", "Accept", "Reject"]
