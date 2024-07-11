from pprint import pprint

import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials


# Файл, полученный в Google Developer Console
CREDENTIALS_FILE = 'creds.json'
# ID Google Sheets документа (можно взять из его URL)
spreadsheet_id = '1E9pA9gVX27IEckoz85DE0rf9KARqZFpxP60Kokmq6sc'

# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

# Чтение листа заявок
output_values = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='Заявки!A1:E10',
    majorDimension='COLUMNS'
).execute()


# Чтение листа сервисменов
servicemen_values = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='Сервисмены!A1:G7',
    majorDimension='ROWS'
).execute()
