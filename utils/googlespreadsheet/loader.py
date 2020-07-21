import os

import gspread

from utils.googlespreadsheet.consts import SPREADSHEET_NAME, CREDENTIALS_FILE

CREDENTIALS_FILE_PATH = os.path.join('utils', 'googlespreadsheet', 'auth_files', CREDENTIALS_FILE)
gc = gspread.service_account(CREDENTIALS_FILE_PATH)
spreadsheet = gc.open(SPREADSHEET_NAME)
