import bs4
import csv
import datetime
import imaplib
import os
import re
import ssl
import sys
import traceback

COLUMN_LABELS = ["location", "date", "start_time", "coach", "grey_zone", "blue_zone", "green_zone", "orange_zone", "red_zone", "calories", "splat_points", "avg_heart_rate", "max_heart_rate", "treadmill_num_steps", "treadmill_distance", "treadmill_time", "treadmill_avg_velocity", "treadmill_max_velocity", "treadmill_avg_incline", "treadmill_max_incline", "treadmill_avg_pace", "treadmill_max_pace", "treadmill_elevation", "rower_distance", "rower_time", "rower_avg_power", "rower_max_power", "rower_avg_velocity", "rower_max_velocity", "rower_500m_split_avg_pace", "rower_500m_split_max_pace", "rower_avg_stroke_rate"]
DATA_INDICES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 13, 15, 17, 19, 22, 25, 28, 30, 33, 35, 39, 40, 43, 46, 49, 52, 54, 58, 60, 64, 66, 70]
IMAP_SERVER = "imap.gmail.com"
PORT = "993"

def remove_duplicates(lst):
    unique = []
    for element in lst:
        if element not in unique:
            unique.append(element)
    lst.clear()
    for element in unique:
        lst.append(element)

def merge_columns(rows, starting_column_index):
    for row in rows:
        row[starting_column_index] += ":" + row[starting_column_index + 1] + row[starting_column_index + 2]
        row.pop(4)
        row.pop(3)

def sort_rows(rows):
    for i in range(len(rows)):
        dt = datetime.datetime.strptime(rows[i][1] + " " + rows[i][2], "%m/%d/%Y %I:%M %p")
        rows[i] = (dt, rows[i])
    rows.sort(key=lambda dt_and_row: dt_and_row[0])
    for i in range(len(rows)):
        dt, row = rows[i]
        rows[i] = row

def pretty_print_row(row):
    for i in range(len(row)):
        print(str(i) + " " + COLUMN_LABELS[i] + " " + row[i])

def pretty_print_text(text):
    for i in range(len(text)):
        label = ""
        if i in DATA_INDICES:
            label = COLUMN_LABELS[DATA_INDICES.index(i)]
        print(str(i) + " " + label + " " + text[i])

def clean_text(text):
    text = [e.encode("ascii", "ignore").decode("utf-8").strip() for e in text]
    to_remove = ["Peak HR:", "Max:", "Fastest:", ","]
    for i in range(len(text)):
        for s in to_remove:
            text[i] = text[i].replace(s, "").strip()
    return text

def get_row_from_data(data, data_indices):
    row = []
    start_index = data.find("<!doctype")
    if start_index == -1:
        start_index = data.find("<!DOCTYPE")
    data = data[start_index:].replace("=\r\n", "")
    bs = bs4.BeautifulSoup(data, "html.parser")
    text = []
    for element in bs.find_all(["p", "span"]):
        t = element.get_text()
        if t != "" and not t.isspace():
            text.append(t)
    text = clean_text(text)
    contains_rower_data = True if "ROWER PERFORMANCE TOTALS" in text else False
    for i in range(len(text)):
        if (i < 45 or (i >= 45 and contains_rower_data)) and i in DATA_INDICES:
            row.append(text[i])
    return row

def get_indices_to_patterns():
    location_pattern = re.compile(r"^(?:.*? \w{2})*$")
    date_pattern = re.compile(r"^(?:\d{1,2}\/\d{1,2}\/\d{4})*$")
    time_of_day_pattern = re.compile(r"^(?:\d{1,2}:\d{2} (?:A|P)M)*$")
    trainer_name_pattern = re.compile(r"^(?:\w+)*$")
    time_pattern = re.compile(r"^(?:\d{1,2}:\d{2})*$")
    number_pattern = re.compile(r"^(?:\d+|(?:\d{1,3}(?:,\d{3})+))(?:\.\d+)*$")
    indices_to_patterns = {
        0: location_pattern,
        1: date_pattern,
        2: time_of_day_pattern,
        3: trainer_name_pattern
    }
    indices_with_number_pattern = [*range(4, 15), *range(16, 20), *range(22, 24), *range(25, 29), 31]
    indices_with_time_pattern = [15, *range(20, 22), 24, *range(29, 31)]
    patterns_indices = [(number_pattern, indices_with_number_pattern), (time_pattern, indices_with_time_pattern)]
    for pattern, indices in patterns_indices:
        for index in indices:
            indices_to_patterns[index] = pattern
    return indices_to_patterns

def find_row_specific_errors(row, indices_to_patterns=None):
    row_specific_errors = []
    required_indices_errors = {
        0: "MISSING REQUIRED LOCATION",
        1: "MISSING REQUIRED DATE",
        2: "MISSING REQUIRED START TIME",
    }
    if not indices_to_patterns:
        indices_to_patterns = get_indices_to_patterns()
    for index, pattern in indices_to_patterns.items():
        if index < len(row):
            m = pattern.search(row[index])
            if not m:
                row_specific_errors.append((index, row[index]))
        else:
            if index <= 2:
                row_specific_errors.append((index, required_indices_errors[index]))
    return row_specific_errors

def remove_errors(rows):
    indices_to_remove = []
    errors = {}
    indices_to_patterns = get_indices_to_patterns()
    for i in range(len(rows)):
        row_specific_errors = find_row_specific_errors(rows[i], indices_to_patterns)
        if len(row_specific_errors) != 0:
            indices_to_remove.append(i)
            errors[i] = (rows[i], row_specific_errors)
    for i in range(len(rows) - 1, -1, -1):
        if i in indices_to_remove:
            rows.pop(i)
    return errors

def pretty_print_errors(errors, column_labels):
    for data_frame_num, row_and_errors in errors.items():
        row, row_specific_errors = row_and_errors
        print("Data Frame Number: " + str(data_frame_num + 1))
        erroneous_indices = [index for index, data_point in row_specific_errors]
        for i in range(len(row)):
            arrow_and_label = ""
            if i in erroneous_indices:
                arrow_and_label = "=> " + column_labels[i]
            print(row[i] + " " + arrow_and_label)
        print()

def get_search_start_datetime(only_new, data_file_name):
    search_start_datetime = None
    if only_new:
        if data_file_name:
            if data_file_name in os.listdir():
                with open(data_file_name, "r") as file:
                    csv_reader = csv.reader(file, delimiter=",")
                    next(csv_reader) # skip header
                    for row in csv_reader:
                        dt = datetime.datetime.strptime(row[1] + " " + row[2], "%m/%d/%Y %I:%M %p")
                        if not search_start_datetime or search_start_datetime.date() < dt.date() or (search_start_datetime.date() == dt.date() and search_start_datetime.time() > dt.time()):
                            search_start_datetime = dt
        else:
            raise(Exception("Request was for only new dates to be searched for but data file name was not given"))
    return search_start_datetime

def get_message_search_str(search_start_datetime, originating_email_address):
    search_str = "(FROM \"" + originating_email_address + "\""
    if search_start_datetime:
        search_str += " SINCE \"" + datetime.datetime.strftime(search_start_datetime.date(), "%d-%b-%Y") + "\""
    search_str += ")"
    return search_str

def get_current_rows(data_file_name):
    rows = []
    if data_file_name in os.listdir():
        with open(data_file_name, "r") as file:
            csv_reader = csv.reader(file, delimiter=",")
            next(csv_reader) # skip header
            for row in csv_reader:
                rows.append(row)
    return rows

def get_data_from_emails(email_address, password, originating_email_addresses, mailbox, only_new=False, data_file_name=None):
    rows = []
    if only_new and data_file_name:
        rows += get_current_rows(data_file_name)
    try:
        ssl_context = ssl.create_default_context()
        imap4ssl = imaplib.IMAP4_SSL(host=IMAP_SERVER, port=PORT, ssl_context=ssl_context)
        imap4ssl.login(email_address, password)
        if mailbox == "":
            imap4ssl.select()
        else:
            imap4ssl.select(mailbox)
        search_start_datetime = None
        try:
            search_start_datetime = get_search_start_datetime(only_new, data_file_name)
        except Exception as e:
            raise
        for originating_email_address in originating_email_addresses:
            search_str = get_message_search_str(search_start_datetime, originating_email_address)
            message_ids = imap4ssl.search(None, search_str)[1][0].split()
            print("For " + originating_email_address + ", found " + str(len(message_ids)) + " messages")
            count = 1
            for message_id in message_ids:
                data = imap4ssl.fetch(message_id, "(RFC822)")[1][0][1].decode("utf-8")
                row = get_row_from_data(data, DATA_INDICES)
                rows.append(row)
                print("Progress: {percentage:.2f}% for {email_address}".format(percentage=(count / len(message_ids) * 100), email_address=originating_email_address))
                count += 1
        imap4ssl.close()
        imap4ssl.logout()
    except Exception as e:
        raise Exception("Error interacting with mail server or processing data: " + str(e))
    remove_duplicates(rows)
    errors = remove_errors(rows)
    sort_rows(rows)
    rows = [COLUMN_LABELS] + rows
    print("\nFound and removed " + str(len(errors)) + " data frames with errors\n")
    print("Error rate: {error_rate:.2f}%\n".format(error_rate=((len(errors) / len(rows)) * 100)))
    if len(errors) > 0:
        print("Errors (indicated by \"=> expected type\"):\n")
        pretty_print_errors(errors, COLUMN_LABELS)
    print("Finished")
    return rows
