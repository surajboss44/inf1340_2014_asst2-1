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
            # 'entry_check': check_entry_reason(item, countries)
        }

        if conditions['med_check'] == 'Quarantine':
            output_list.append('Quarantine')

        elif conditions['comp_check'] == 'Reject':  # or conditions['entry_check'] == 'Reject':
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


def check_entry_reason(inputs, countries):
    """
    Checks for the entry reason of a traveller and does the necessary checks.
    """
    for item in inputs:
        home_country = item["home"]["country"]
        if item["entry_reason"] == "returning":
            if home_country == "KAN":
                return "accept"
        elif item["entry_reason"] == "visit":
            if home_country == countries[home_country]["code"]and valid_visa(item["visa"]["code"], item["visa"]["date"]):
                return "accept"
        elif item["entry_reason"] == "transit":
            if home_country == countries[home_country]["code"]and valid_visa(item["visa"]["code"], item["visa"]["date"]):
                return "accept"
        else:
            return "reject"

    """If the reason for entry is to visit and the visitor has a passport from a country from which a visitor
    visa is required, the traveller must have a valid visa. A valid visa is one that is less than two years
    old."""
    # for item in inputs:
    #         home_country = item["home"]["country"]
    #         if item["home"]["country"] == countries[home_country]["code"] and item["visa"]["code"] != "":
    #             print(item["first_name"]+" "+item["last_name"] + " accept")
    #         elif item["home"]["country"] == countries[home_country]["code"] and item["visa"]["code"] == "":
    #             print(item["first_name"] + " " + item["last_name"] + " reject")
    # for item in inputs:
    #         home_country = item["home"]["country"]
    #         # Today's date in string format
    #         date_in_string_format = str(datetime.date.today())
    #         # Today's date in date format
    #         date_today = datetime.datetime.strptime(date_in_string_format, "%Y-%m-%d")
    #         visa_date_from_file = item["visa"]["date"]
    #         visa_date = datetime.datetime.strptime(visa_date_from_file,"%Y-%m-%d")
    #         date_difference = int(str(date_today - visa_date)[0:3])
    #         print(date_difference)
    #         if item["entry_reason"] == "transit" and item["home"]["country"] == countries[home_country]["code"] and (item["visa"]["code"] != " ") and date_difference < 730:
    #             print(item["first_name"]+" "+item["last_name"] + " accept")
    #         elif item["home"]["country"] == countries[home_country]["code"] and (item["visa"]["code"] == " " or date_difference > 730):
    #             print(item["first_name"] + " " + item["last_name"] + " reject")


def date_diff(visa_date_from_file):
    """
    Checks whether a passport number is five sets of five alpha-number characters separated by dashes
    :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    # Today's date in string format
    date_in_string_format = str(datetime.date.today())
    # Today's date in date format
    date_today = datetime.datetime.strptime(date_in_string_format, "%Y-%m-%d")
    #   visa_date_from_file = items["visa"]["date"]
    visa_date = datetime.datetime.strptime(visa_date_from_file, "%Y-%m-%d")
    date_difference = int(str(date_today - visa_date)[0:3])


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

    # Today's date in date format and computing the difference between visa date and current date
    date_in_string_format = str(datetime.date.today())
    date_today = datetime.datetime.strptime(date_in_string_format, "%Y-%m-%d")
    visa_date = datetime.datetime.strptime(date, "%Y-%m-%d")
    date_difference = int(str(date_today - visa_date)[0:3])

    if visa_format.match(visa_number) and (valid_date_format(date) and date_difference < 730):
        return True
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
#print(valid_visa('YD77Y-1MH6U', '2014-04-30'))