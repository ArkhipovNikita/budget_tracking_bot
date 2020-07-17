import os

import gspread

from googlesheet.consts import SPREADSHEET_NAME, CREDENTIALS_FILE

# fix abs path to rel
CREDENTIALS_FILE_PATH = os.path.join('googlesheet', 'auth_files', CREDENTIALS_FILE)
gc = gspread.service_account(CREDENTIALS_FILE_PATH)
spreadsheet = gc.open(SPREADSHEET_NAME)
