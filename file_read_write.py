import csv
import re
from constants import *
from os import listdir
from os.path import isfile, join


def read_data_from_file(input_file):
    """
    :param input_file:
    :return: return first column of csv file as a python list
    """
    with open(input_file, 'r') as file:
        return [row[0] for row in csv.reader(file)]


def generate_google_contacts_from_numbers(input_file, output_file):
    """
    :param input_file:
    :param output_file:
    :return: Generate a file that can be used to add contacts to google contacts. it takes a csv file with list of numbers
    """
    contacts = read_data_from_file(input_file)
    contacts_added = 0
    with open('generated_contacts_1.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Given Name", "Group Membership", "Phone 1 - Type", "Phone 1 - Value"])
        # for index, n in enumerate(contacts):
        #     contacts_added += 1
        #     x = "0" + str(n)
        #     writer.writerow(["N" + str(index), "N" + str(index), "* myContacts", "", x])
        index = 57000
        for n in contacts:
            contacts_added += 1
            x = "0" + str(n)
            writer.writerow(["N" + str(index), "N" + str(index), "* myContacts", "", x])
            index +=1
    return contacts_added


def write_contact_names_to_file(input_file, output_file):
    """
    Takes Google Contacts csv file as an input and save all contacts names in file
    :param input_file:
    :param output_file:
    :return: None
    """
    contacts = []
    contacts_added = 0
    try:
        with open(input_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] and row[0] != 'Name':
                    contacts.append(row[0])

        existing_contacts = read_data_from_file(output_file)
        with open(output_file, 'a+', newline='') as file:
            writer = csv.writer(file)
            for index, n in enumerate(contacts):
                if not n in existing_contacts:
                    writer.writerow([n])
                    contacts_added += 1
        return contacts_added, True
    except:
        return contacts_added, False


def read_contacts_data():  # read all data saved in files
    my_path = 'Contacts Data'
    all_files = [my_path + str("/") + f for f in listdir(my_path) if isfile(join(my_path, f))]
    contacts_data = {}
    for item in all_files:
        item_name = re.sub(r'|'.join(map(re.escape, ['.csv', 'Contacts Data/'])), '', item)
        contacts_data[item_name] = read_data_from_file(item)
    return contacts_data


# read_contacts_data()
# generate_google_contacts_from_numbers('records.csv', 'xps.csv')

def add_new_contact_to_file(index=None, contact=None):
    file_path = 'Contacts Data/Contacts.csv'
    notification = CONTACT_ADDED_MSG
    if index == 'group':
        notification = GROUP_ADDED_MSG
        file_path = 'Contacts Data/Groups.csv'

    try:
        with open(file_path, 'a+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([contact])
            read_contacts_data()
        return True
    except:
        return False

