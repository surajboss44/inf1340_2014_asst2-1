#!/usr/bin/env python3

""" Computer-based immigration office for Kanadia """

__author__ = 'Susan Sim'
__email__ = "ses@drsusansim.org"

__copyright__ = "2014 Susan Sim"
__license__ = "MIT License"

__status__ = "Prototype"

# imports one per line
import re
import datetime
import json


def decide(input_file, watchlist_file, countries_file):

    """
    Decides whether a traveller's entry into Kanadia should be accepted

    :param input_file: The name of a JSON formatted file that contains cases to decide
    :param watchlist_file: The name of a JSON formatted file that contains names and passport numbers on a watchlist
    :param countries_file: The name of a JSON formatted file that contains country data, such as whether
        an entry or transit visa is required, and whether there is currently a medical advisory
    :return: List of strings. Possible values of strings are: "Accept", "Reject", "Secondary", and "Quarantine"
    """
    with open(countries_file, "r") as file_reader:
        countries_content = file_reader.read()
        countries = json.loads(countries_content)

    with open(input_file, "r") as file_reader:
        input_content = file_reader.read()
        inputs = json.loads(input_content)

    with open(watchlist_file, "r") as file_reader:
        watchlist_file = file_reader.read()
        watchlist = json.loads(watchlist_file)

    for item in inputs:
        """Condition to check if the traveller is coming from country with medical advisory"""
        country = item["from"]["country"].upper()
        if countries[country]["medical_advisory"] != "":
            return 'Quarantine'

    for item in inputs:
        """Condition to check if the traveller details are incomplete"""
        if valid_passport_format(item["passport"]) and valid_date_format(item["birth_date"]):
            if not item["passport"] and\
                    not item["first_name"] and\
                    not item["last_name"] and\
                    not item["birth_date"] and\
                    not item["home"]["city"] and\
                    not item["home"]["region"] and \
                    not item["home"]["country"] and\
                    not item["entry_reason"] and\
                    not item["from"]["city"] and\
                    not item["from"]["region"] and\
                    not item["from"]["country"]:
                return 'Reject'
        else:
            return 'Reject'

    for item in watchlist:
        """Condition to check if the traveller is on the watchlist"""
        first_name = item["first_name"].upper()
        last_name = item["last_name"].upper()
        passport_number = item["passport"].upper()

        for item2 in inputs:
            if (first_name == item2["first_name"].upper() and last_name == item2["last_name"].upper()) or\
                    last_name == item2["last_name"].upper() or\
                    passport_number == item2["passport"].upper():

                return 'Secondary'

    for item in inputs:
        if item["entry_reason"] == "transit":
            print("hey")

    """If the reason for entry is to visit and the visitor has a passport from a country from which a visitor
    visa is required, the traveller must have a valid visa. A valid visa is one that is less than two years
    old."""
    # for item in inputs:
    #         home_country = item["home"]["country"]
    #         if item["home"]["country"] == countries[home_country]["code"] and item["visa"]["code"] != "":
    #             print(item["first_name"]+" "+item["last_name"] + " accept")
    #         elif item["home"]["country"] == countries[home_country]["code"] and item["visa"]["code"] == "":
    #             print(item["first_name"] + " " + item["last_name"] + " reject")


    return "Accept"

def valid_passport_format(passport_number):
    """
    Checks whether a passport number is five sets of five alpha-number characters separated by dashes
    :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    passport_format = re.compile('\w{5}-\w{5}-\w{5}-\w{5}-\w{5}$')

    if passport_format.match(passport_number):
        return True
    else:
        return False


def valid_visa_format(visa_number):
    """
    Checks whether a visa number is two sets of five alpha-number characters separated by dashes
    :param visa_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    visa_format = re.compile('\w{5}-\w{5}$')

    if visa_format.match(visa_number):
        print("valid time")
        return True
    else:
        print("not valid time")
        return False


def valid_date_format(date_string):
    """
    Checks whether a date has the format YYYY-mm-dd in numbers
    :param date_string: date to be checked
    :return: Boolean True if the format is valid, False otherwise
    """
    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

print(decide('example2.json','watchlist.json','countries.json'))
