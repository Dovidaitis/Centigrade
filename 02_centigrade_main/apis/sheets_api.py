from functools import cache
from html import entities
from sqlite3 import Timestamp
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from tinydb import TinyDB, Query
from os import path
import logging

print("sheets_api_call.py imported...")

class DebugLogs():

    logging.basicConfig(filename="dubug_logs.txt",
                    level=logging.DEBUG,
                    format='%(levelname)s: %(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S')

    @staticmethod
    def debug_log(failed_function, full_error):
        logging.info(f"Failed function: {failed_function}\n Error: {full_error}\n")

class SheetsEntry():

    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    #authentication token path
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "apis/creds/sheets-creds.json", SCOPES)
        
    index = 2  # where to start at worksheet to inser data
    
    def open_log_sheet(self):
        try:
            temperature_log = self.client.open("temperature_log").get_worksheet(0)
            settings = self.client.open("temperature_log").get_worksheet(1)
            return temperature_log, settings
        except Exception as e:
            DebugLogs().debug_log("temperature_log sheet was not opened", e)
            print(e)

    def __init__(self): 
        try:
            self.client = gspread.authorize(self.creds)
            self.temperature_log, self.settings = self.open_log_sheet()
        except Exception as e:
            print(f"sheet connection exception occured... \n{e}")



    @staticmethod
    def create_data_row(timestamp, station_name, user_uid, user_temp):
        row = [timestamp, station_name, user_uid, user_temp]
        return row
        
    """
    Insert a row of data into the temperature_log table

    :param data_row: a list of values to insert into the table
    """
    def push_temp(self, data_row):
        try:
            self.temperature_log.insert_row(data_row, 2)
        except Exception as e:
            print(f'push_temp() error: not inserted row: {data_row}')
            print(e)

    # function prints all data from database
    def print_sheet(self, sheet_to_print):
        data = sheet_to_print.get_all_records()
        print(data)

    @staticmethod
    def timestamp():
        # gives current time in a format HH:MM:SS-dd/mm/yyyy
        return datetime.now().strftime("%H:%M:%S-%d/%m/%y")

    def new_settings(self):
        return self.settings.get_all_records()[0]






# log = SheetsEntry()
# print(log.new_settings()['mirror'])
# print(type(log.new_settings()['mirror']))
# print(log.temperature_log)
# print(log.settings)
# log.print_sheet(log.settings)

# data_log = log.create_data_row("date", "station name", "uid", "tempasdf")
# log.push_temp(data_log)
# log.print_sheet(log.temperature_log)

class Cache():

    def __init__(self, db_name):
            self.db = TinyDB(f'apis/database/{db_name}.json')

    def save_log(self, log_data):
        db_entry = {"type":"log", "timestamp":log_data[0], "station_name":log_data[1], "user_uid":log_data[2], "user_temp":log_data[3]}
        self.db.insert(db_entry)
    
    def save_email_notification(self, report_letter):
        db_entry = {"type":"notification", "report_letter":report_letter}
        self.db.insert

    # note: log is a object of SheetsEntry class, pass a log object to this function as an argument
    def reupload_logs(self, log):
        q = Query()
        entries = self.db.search(q.type == "log")
        for entry in entries:
            try:
                log_data = log.create_data_row(entry['timestamp'], entry['station_name'], entry['user_uid'], entry['user_temp'])
                log.push_temp(log_data)
                self.db.remove(q.timestamp == entry['timestamp'])
            except Exception as e:
                DebugLogs().debug_log("reupload_logs()", e)
    
    # note: pass gmail_service object to this function
    def resend_emails(self, gmail_service):
        q = Query()
        entries = self.db.search(q.type == "notification")
        for entry in entries:
            try:
                gmail_service.report_user(entry['report_letter'])
                self.db.remove(q.report_letter == entry['report_letter'])
            except Exception as e:
                DebugLogs.debug_log("resend_emails()", e)
