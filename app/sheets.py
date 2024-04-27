import pandas as pd
import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials
from app.db import Database

class SheetData:
    
    def __init__(self) -> None:        
        self.client = self.connect()
    
    def connect(self):
        try:
            scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_name('credentials/sheets_credentials.json', scope)  
            return gspread.authorize(creds)
        except gspread.exceptions as e:
            raise e
        
    def insert(self, spreadsheet_name, sheet_name, data) -> bool:
        try:
            if len(data) <= 0:
                return False
            spreadsheet = self.client.open(spreadsheet_name)
            sheet = spreadsheet.worksheet(sheet_name)
            print("INSERT G.SHEETS, WAIT...")        
            sheet.append_rows(data)  
            return True                      
        except Exception as e:
            raise e
