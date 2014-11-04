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


# def decide(input_file, watchlist_file, countries_file):
def decide():
    """
    Decides whether a traveller's entry into Kanadia should be accepted

    :param input_file: The name of a JSON formatted file that contains cases to decide
    :param watchlist_file: The name of a JSON formatted file that contains names and passport numbers on a watchlist
    :param countries_file: The name of a JSON formatted file that contains country data, such as whether
        an entry or transit visa is required, and whether there is currently a medical advisory
    :return: List of strings. Possible values of strings are: "Accept", "Reject", "Secondary", and "Quarantine"
    """
    with open("countries.json", "r") as file_reader:
        countries_file = file_reader.read()
        countries = json.loads(countries_file)
    with open("example_entries.json", "r") as file_reader:
        sample_entries_file = file_reader.read()
        sample_entries = json.loads(sample_entries_file)
    for item in sample_entries:
        # print(item["passport"])
        """Condition to check if the traveller details are incomplete"""
        """if item["passport"] and item["first_name"] and item["last_name"] and item["birth_date"] and item["home"][
            "city"] and item["home"]["region"] and item["home"]["country"] and item["entry_reason"] and item["from"][
            "city"] and item["from"]["region"] and item["from"]["country"]:
            print("")
        else:
            print("")"""""
    for item in sample_entries:
       country = item["from"]["country"]
       if countries[country]["medical_advisory"] != "":
          print("hi")





            #print(countries["LUG"]["name"])
            # return ["Reject"]




def valid_passport_format(passport_number):
    """
    Checks whether a pasport number is five sets of five alpha-number characters separated by dashes
    :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    passport_format = re.compile('.{5}-.{5}-.{5}-.{5}-.{5}')

    if passport_format.match(passport_number):
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


decide()