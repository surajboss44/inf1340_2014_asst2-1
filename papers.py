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

    output_list = []
    for item in inputs:

        conditions = {
            'med_check': check_medical_advisory(item, countries),
            'comp_check': check_completeness(item),
            'watch_check': check_watchlist(item, watchlist),
            'entry_check': check_entry_reason(item, countries)
        }
        print(conditions)
        if conditions['med_check'] == 'Quarantine':
            output_list.append('Quarantine')

        elif conditions['comp_check'] == 'Reject':
            output_list.append('Reject')
        elif conditions['entry_check'] == 'Reject':
            output_list.append('Reject')
        elif conditions['watch_check'] == 'Secondary':
            output_list.append('Secondary')
        else:
            output_list.append('Accept')

    return output_list




def check_medical_advisory(item, countries):
    """
    Checks whether a passport number is five sets of five alpha-number characters separated by dashes
    :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """

    """Condition to check if the traveller is coming from country with medical advisory"""
    from_country = item["from"]["country"].upper()

    if countries[from_country]["medical_advisory"] != "":
        return 'Quarantine'
    if "via" in item:
        via_country = item["via"]["country"].upper()
        if countries[via_country]["medical_advisory"] != "":
            return 'Quarantine'


def check_watchlist(item, watchlist):
    """
    Checks whether a passport number is five sets of five alpha-number characters separated by dashes
    :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    for watch_item in watchlist:
        """Condition to check if the traveller is on the watchlist"""
        first_name = watch_item["first_name"].upper()
        last_name = watch_item["last_name"].upper()
        passport_number = watch_item["passport"].upper()

        if (first_name == item["first_name"].upper() and last_name == item["last_name"].upper()) or\
                last_name == item["last_name"].upper() or\
                passport_number == item["passport"].upper():

            return 'Secondary'


def check_completeness(item):
    """
    Checks whether a passport number is five sets of five alpha-number characters separated by dashes
    :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    """Condition to check if the traveller details are incomplete"""
    if valid_passport_format(item["passport"]) and valid_date_format(item["birth_date"]):
        if not item["passport"] or\
                not item["first_name"] or\
                not item["last_name"] or\
                not item["birth_date"] or\
                not item["home"]["city"] or\
                not item["home"]["region"] or \
                not item["home"]["country"] or\
                not item["entry_reason"] or\
                not item["from"]["city"] or\
                not item["from"]["region"] or\
                not item["from"]["country"]:
            return 'Reject'
    else:
        return 'Reject'


def check_entry_reason(item, countries):
    """If the reason for entry is to visit and the visitor has a passport from a country from which a visitor
    visa is required, the traveller must have a valid visa. A valid visa is one that is less than two years
    old."""

    home_country = item["home"]["country"]
    if item["entry_reason"] == "returning":

        if home_country == "KAN":
            return
        else:
            return "Reject"
    elif item["entry_reason"] == "visit":

        if home_country == countries[home_country]["code"] and valid_visa(item["visa"]["code"], item["visa"]["date"]):
            return
        else:
            return "Reject"
    elif item["entry_reason"] == "transit":

        if home_country == countries[home_country]["code"] and valid_visa(item["visa"]["code"], item["visa"]["date"]):
            return
        else:
            return "Reject"
    else:
        return "Reject"


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


def valid_visa(visa_number, date):
    """
    Checks whether a visa number is two sets of five alpha-number characters separated by dashes
    :param visa_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    visa_format = re.compile('\w{5}-\w{5}$')


    if visa_format.match(visa_number) and valid_date_format(date):
        current_date = str(datetime.date.today())
        current_date = datetime.datetime.strptime(current_date, "%Y-%m-%d")
        visa_date = datetime.datetime.strptime(date, "%Y-%m-%d")

        if abs((current_date - visa_date).days) < 730:
            return True
        else:
            return False
    else:
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

print(decide('example2.json', 'watchlist.json', 'countries.json'))
#print(valid_visa('YD77Y-1MH6U', '2009-11-01'))