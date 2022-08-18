from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64
from lib2to3.pgen2.pgen import generate_grammar
import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
import time
from datetime import datetime


class GmailService():

    CLIENT_SECRET_FILE = 'apis/creds/gmail-creds.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']
    
    

    @staticmethod
    def Create_Service(client_secret_file, api_name, api_version, *scopes):
        print(client_secret_file, api_name, api_version, scopes, sep='-')
        CLIENT_SECRET_FILE = client_secret_file
        API_SERVICE_NAME = api_name
        API_VERSION = api_version
        SCOPES = [scope for scope in scopes[0]]
        print(SCOPES)

        cred = None

        pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
        # print(pickle_file)

        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as token:
                cred = pickle.load(token)

        if not cred or not cred.valid:
            if cred and cred.expired and cred.refresh_token:
                cred.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CLIENT_SECRET_FILE, SCOPES)
                cred = flow.run_local_server()

            with open(pickle_file, 'wb') as token:
                pickle.dump(cred, token)

        try:
            service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
            print(API_SERVICE_NAME, 'service created successfully')
            return service
        except Exception as e:
            print('Unable to connect.')
            print(e)
            return None

    def __init__(self):
        self.service = self.Create_Service(self.CLIENT_SECRET_FILE, self.API_NAME, self.API_VERSION, self.SCOPES)
        self.supervisors_emails = ["22d10@kjg.lt"] 
    
    @staticmethod
    def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
        dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
        return dt
    # returns datetime object   

    # sends email 
    def send_email(self, message, recipient_email, subject):
        mimeMessage = MIMEMultipart()
        mimeMessage['to'] = recipient_email
        mimeMessage['subject'] = subject
        mimeMessage.attach(MIMEText(message, 'plain'))
        raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
        try:
            message = self.service.users().messages().send(
                userId='me', body={'raw': raw_string}).execute()
        except Exception as e:
            print(e)


    # formats text for gmail body
    @staticmethod
    def generate_report(user, current_temp, zone=None):
        return f"{user} turi {current_temp} temperatūrą. \nMeasured with: {zone}"

    # sends report to all of the suprervisors
    def report_user(self, str_report):
        for supervisor_email in self.supervisors_emails:
            self.send_email(str_report, supervisor_email,
                    "Viršyta leidžiama temperatūra")



print("gmail_api_call imported...")


