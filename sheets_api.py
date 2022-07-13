import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials


CREDENTIALS_FILE = 'ancient-muse-355622-973a87fb135a.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                               ['https://www.googleapis.com/auth/spreadsheets',
                                                                'https://www.googleapis.com/auth/drive'])

httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API

spreadsheet = service.spreadsheets().create(body = {
    'properties': {'title': 'Карусель', 'locale': 'ru_RU'},
    'sheets': [{'properties': {'sheetType': 'GRID',
                               'sheetId': 0,
                               'title': 'Лист номер один',
                               'gridProperties': {'rowCount': 100, 'columnCount': 15}}}]
}).execute()

spreadsheetId = spreadsheet['spreadsheetId'] # сохраняем идентификатор файла
print('https://docs.google.com/spreadsheets/d/' + spreadsheetId)

driveService = apiclient.discovery.build('drive', 'v3', http = httpAuth) # Выбираем работу с Google Drive и 3 версию API
access = driveService.permissions().create(
    fileId = spreadsheetId,
    body = {'type': 'user', 'role': 'writer', 'emailAddress': 'kharisov10@yandex.ru'},  # Открываем доступ на редактирование
    fields = 'id'
).execute()

def write_data(list, count):
    results = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, body={
        "valueInputOption": "USER_ENTERED",
        # Данные воспринимаются, как вводимые пользователем (считается значение формул)
        "data": [
            {"range": f"Лист номер один!A{count}:C{count+len(list)}",
             "majorDimension": "ROWS",  # Сначала заполнять строки, затем столбцы
             "values": list
                   # Заполняем первую строку

             }
        ]
    }).execute()