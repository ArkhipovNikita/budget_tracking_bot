import os

import gspread

from googlesheet.consts import SPREADSHEET_NAME, CREDENTIALS_FILE

# fix abs path to rel
# CREDENTIALS_FILE_PATH = os.path.join('auth_files', CREDENTIALS_FILE)
gc = gspread.service_account('/Users/arkhipov/Documents/Git/budget_tracking_bot/googlesheet/auth_files/telegrambotwrite-1594670249111-247d4243e67c.json')
spreadsheet = gc.open(SPREADSHEET_NAME)
