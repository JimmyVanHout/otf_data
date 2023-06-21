import batch_send
import csv
import data_from_emails
import getpass
import json
import os
import re
import subprocess
import sys
import time
import traceback
import webbrowser

RUN_MODE_OPTIONS = ["--browser", "--terminal"]
VALID_OPTIONS = [*RUN_MODE_OPTIONS, "--help", "--store-password"]
CONFIG_FILE_NAME = "config.txt"
OUTPUT_FILE_NAME = "data.csv"
USER_INTERFACE_URL = "http://127.0.0.1:5000/user_interface"
USER_INPUT_FILE_NAME = "user_input.json"

def check_emails_format_validity(email_addresses):
    email_address_pattern = re.compile("(?:\w|\.)+@.*?\..*")
    for email_address in [ea.strip() for ea in email_addresses.split(",")]:
        if not email_address_pattern.search(email_address):
            return False
    return True

def get_config_data_from_terminal_input():
    email_address_pattern = re.compile("(?:\w|\.)+@gmail.com")
    email_address = input("Enter email address: ")
    while not email_address_pattern.search(email_address.strip()):
        email_address = input("Enter email address: ")
    email_address = email_address.strip()
    password = getpass.getpass("Enter password: ")
    password = password.strip()
    originating_email_addresses = input("Enter comma-separated originating email addresses: ")
    while not check_emails_format_validity(originating_email_addresses):
        originating_email_addresses = input("Enter comma-separated originating email addresses: ")
    originating_email_addresses = ",".join([ea.strip() for ea in originating_email_addresses.split(",")])
    mailbox = input("Enter mailbox (left blank, default is inbox): ")
    only_new_input = input("Only search for new emails (yes or no)?: ")
    only_new = True if only_new_input == "yes" else False
    return email_address, password, originating_email_addresses, mailbox, only_new

def get_forwarding_data_from_terminal_input():
    email_address = input("Enter the email address of the account to search in: ").strip()
    password = getpass.getpass("Enter the password of the account to search in: ").strip()
    receiving_email_address = input("Enter receiving email address: ").strip()
    mailbox = input("Enter mailbox to search (left blank, default is inbox): ").strip()
    return email_address, password, receiving_email_address, mailbox

def setup_config_file(email_address, password, originating_email_addresses, mailbox, only_new):
    with open(CONFIG_FILE_NAME, "w") as config_file:
        config_file.write(email_address + " # email address\n")
        config_file.write(password + " # password\n")
        config_file.write(originating_email_addresses + " # originating email addresses\n")
        config_file.write(mailbox + " # mailbox\n")
        only_new_str = "yes" if only_new else "no"
        config_file.write(only_new_str + " # only search for new messages")

def read_from_config_file():
    with open(CONFIG_FILE_NAME, "r") as config_file:
        email_address = config_file.readline().split("#", 1)[0].rstrip()
        password = config_file.readline().split("#", 1)[0].rstrip()
        originating_email_addresses = [originating_email_address.strip() for originating_email_address in config_file.readline().split("#", 1)[0].split(",")]
        mailbox = config_file.readline().split("#", 1)[0].rstrip()
        only_new = True if config_file.readline().split("#", 1)[0].rstrip() == "yes" else False
    return email_address, password, originating_email_addresses, mailbox, only_new

def write_to_output_file(rows, output_file_name):
    with open(output_file_name, "w", newline="") as data_file:
        csv_writer = csv.writer(data_file, delimiter=",")
        for row in rows:
            csv_writer.writerow(row)

def terminal_exec(store_password=False):
    email_address = password = originating_email_addresses= mailbox = only_new = None
    if CONFIG_FILE_NAME not in os.listdir():
        forward_emails = input("Would you like to forward past otbeatreport@orangetheoryfitness.com emails from one email account to another (yes or no)?: ")
        if forward_emails == "yes":
            email_address, password, receiving_email_address, mailbox = get_forwarding_data_from_terminal_input()
            try:
                batch_send.send(email_address, password, receiving_email_address, mailbox)
            except Exception as e:
                print("Error sending mail:" + str(e))
                traceback.print_exc()
                sys.exit(1)
        email_address, password, originating_email_addresses, mailbox, only_new = get_config_data_from_terminal_input()
        if store_password:
            setup_config_file(email_address, password, originating_email_addresses, mailbox, only_new)
        else:
            setup_config_file(email_address, "", originating_email_addresses, mailbox, only_new)
        originating_email_addresses = originating_email_addresses.split(",")
    else:
        email_address, password, originating_email_addresses, mailbox, only_new = read_from_config_file()
    if not store_password and password == "":
        password = getpass.getpass("Password: ")
    rows = None
    try:
        rows = data_from_emails.get_data_from_emails(email_address, password, originating_email_addresses, mailbox, only_new=True, data_file_name=OUTPUT_FILE_NAME)
    except Exception as e:
        print("Error extracting data from emails: " + str(e))
        traceback.print_exc()
        sys.exit(1)
    write_to_output_file(rows, OUTPUT_FILE_NAME)
    sys.exit(0)

def browser_exec(store_password=False):
    email_address = password = originating_email_addresses= mailbox = only_new = None
    if CONFIG_FILE_NAME not in os.listdir():
        server_process = subprocess.Popen("python3 -m flask run".split(), cwd="./server")
        time.sleep(1)
        webbrowser.open(USER_INTERFACE_URL)
        data = None
        while not data:
            if USER_INPUT_FILE_NAME in os.listdir(path="./server"):
                with open("./server/" + USER_INPUT_FILE_NAME, "r") as file:
                    data = json.loads(file.read())
                os.remove("./server/" + USER_INPUT_FILE_NAME)
            else:
                time.sleep(1)
        server_process.kill()
        if "should_forward" in data and data["should_forward"] == "on":
            forwarding_email_address = data["forwarding_email_address"].replace(" ", "")
            forwarding_password = data["forwarding_password"].replace(" ", "")
            forwarding_receiving_email_address = data["forwarding_receiving_email_address"].replace(" ", "")
            forwarding_mailbox = data["forwarding_mailbox"].replace(" ", "")
            try:
                batch_send.send(forwarding_email_address, forwarding_password, forwarding_receiving_email_address, forwarding_mailbox)
            except Exception as e:
                print("Error sending mail:" + str(e))
                traceback.print_exc()
                sys.exit(1)
        email_address = data["email_address"].replace(" ", "")
        password = data["password"].replace(" ", "")
        originating_email_addresses = data["originating_email_addresses"].replace(" ", "")
        mailbox = data["mailbox"].replace(" ", "")
        only_new = True if "only_search_new" in data and data["only_search_new"] == "on" else False
        if store_password:
            setup_config_file(email_address, password, originating_email_addresses, mailbox, only_new)
        else:
            setup_config_file(email_address, "", originating_email_addresses, mailbox, only_new)
        originating_email_addresses = originating_email_addresses.split(",")
    else:
        email_address, password, originating_email_addresses, mailbox, only_new = read_from_config_file()
    if not store_password and password == "":
        password = getpass.getpass("Password: ")
    rows = None
    try:
        rows = data_from_emails.get_data_from_emails(email_address, password, originating_email_addresses, mailbox, only_new, data_file_name=OUTPUT_FILE_NAME)
    except Exception as e:
        print("Error extracting data from emails: " + str(e))
        traceback.print_exc()
        sys.exit(1)
    write_to_output_file(rows, OUTPUT_FILE_NAME)
    sys.exit(0)

def print_correct_usage():
    print("Correct usage: python3 otf.py [--<arg>]. Use --help for more information.")
    sys.exit(1)

def print_help():
    print("Correct usage:\n")
    print("python3 otf.py [--browser|--terminal|--help] [--store-password]")
    print("--browser: execute program with browser user interface (default behavior)")
    print("--terminal: execute program with terminal user interface")
    print("--help: get help message")
    print("--store-password: store password unencrypted in configuration file")
    sys.exit(0)

def get_command_start_index(args):
    for i in range(len(args)):
        if os.path.basename(os.path.realpath(__file__)) in sys.argv[i]:
            return i

def is_command_valid(command):
    if len(command) > 1 and len(command) < 3:
        for word in command[1:]:
            if word not in VALID_OPTIONS:
                return False
        if "--help" in command[1:] and len(command) > 2:
            return False
        run_mode_option_count = 0
        for option in RUN_MODE_OPTIONS:
            if option in command[1:]:
                run_mode_option_count += 1
            if run_mode_option_count > 1:
                return False
    return True

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    command = sys.argv[get_command_start_index(sys.argv):]
    if not is_command_valid(command):
        print_correct_usage()
        sys.exit(1)
    store_password = True if "--store-password" in command[1:] else False
    if "--browser" in command[1:]:
        browser_exec(store_password)
    elif "--terminal" in command[1:]:
        terminal_exec(store_password)
    elif "--help" in command[1:]:
        print_help()
    else:
        browser_exec(store_password)
