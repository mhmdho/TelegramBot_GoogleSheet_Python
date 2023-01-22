from oauth2client.service_account import ServiceAccountCredentials
import gspread
import os


scope = ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive.file',
         'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_dict(
  keyfile_dict={
                'type': os.getenv('type'),
                'project_id': os.getenv('project_id'),
                'private_key_id': os.getenv('private_key_id'),
                'private_key': os.getenv('private_key'),
                'client_email': os.getenv('client_email'),
                'client_id': os.getenv('client_id'),
                'auth_uri': os.getenv('auth_uri'),
                'token_uri': os.getenv('token_uri'),
                'auth_provider_x509_cert_url': os.getenv('auth_provider_x509_cert_url'),
                'client_x509_cert_url': os.getenv('client_x509_cert_url')
                },
  scopes=scope)

client = gspread.authorize(creds)

spreadsheet = client.open("TelegramToGoogleSheet")