#!/usr/bin/env python3

""" Computer-based immigration office for Kanadia """

__author__ = 'Sam Novak and Suraj Narayanan'

__copyright__ = "2014 Sam & Suraj"
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
        if conditions['med_check']:
            output_list.append('Quarantine')
        elif conditions['comp_check']:
            output_list.append('Reject')
        elif conditions['entry_check']:
            output_list.append('Reject')
        elif conditions['watch_check']:
            output_list.append('Secondary')
        else:
            output_list.append('Accept')

    return output_list


def check_medical_advisory(item, countries):
    """
    Checks if the traveller's has passed through or has a home country with a medical advisory
    :param item: dictionary containing traveller information
    :param countries: dictionary containing list of countries with medical advisory information
    :return: Boolean; True if format meets any of the conditions, False otherwise
    """
    from_country = item["from"]["country"].upper()

    if countries[from_country]["medical_advisory"] != "":
        return True

    if "via" in item:
        via_country = item["via"]["country"].upper()
        if countries[via_country]["medical_advisory"] != "":
            return True

    return False


def check_watchlist(item, watchlist):
    """
    Checks whether a traveller's passport, last name, or first and last name is contained in a traveller watchlist
    :param item: dictionary containing traveller information
    :param watchlist: dictionary containing list of travellers that require additional screening
    :return: Boolean; True if traveller meets any of the conditions, False otherwise
    """
    for watch_item in watchlist:
        """Condition to check if the traveller is on the watchlist"""
        first_name = watch_item["first_name"].upper()
        last_name = watch_item["last_name"].upper()
        passport_number = watch_item["passport"].upper()

        if (first_name == item["first_name"].upper() and last_name == item["last_name"].upper()) or\
                last_name == item["last_name"].upper() or\
                passport_number == item["passport"].upper():

            return True

    return False


def check_completeness(item):
    """
    Checks whether a traveller has all the required information
    :param item: dictionary containing traveller information
    :return: Boolean; True if invalid birth date, passport, or missing req info. False otherwise
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
            return True
    else:
        return True

    return False


def check_entry_reason(item, countries):
    """
    Checks whether a traveller's has a valid visa based on the reason for entry
    :param item: dictionary containing traveller information
    :param countries: dictionary containing a list of countries and visa requirements
    :return: Boolean; True if fails to meet requirements for given entry reason, False otherwise
    """

    home_country = item["home"]["country"]

    if item["entry_reason"] == "visit":
        if "visa" in item:
            if home_country == countries[home_country]["code"] and valid_visa(item["visa"]["code"], item["visa"]["date"]):
                return False
            else:
                return True
        else:
            return True

    elif item["entry_reason"] == "transit":
        if "visa" in item:
            if home_country == countries[home_country]["code"] and valid_visa(item["visa"]["code"], item["visa"]["date"]):
                return False
            else:
                return True
        else:
            return True

    elif item["entry_reason"] == "returning":
        if home_country == "KAN":
            return False
        else:
            return True
    else:
        return True


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
    Checks whether a visa number is two sets of five alpha-number characters separated by dashes,
    and has been issued within 2 years (730 days).
    :param visa_number: alpha-numeric string
    :param date: date when visa was issued
    :return: Boolean; True if the visa is valid, False otherwise
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

print(decide('example_entries.json', 'watchlist.json', 'countries.json'))
#print(valid_visa('YD77Y-1MH6U', '2009-11-01'))