
from dotenv import load_dotenv

import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv
# Загрузка переменных окружения из .env файла
load_dotenv()

# Получение значений из .env
SAMPLE_SPREADSHEET_ID = os.getenv('SAMPLE_SPREADSHEET_ID')
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')

SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), SERVICE_ACCOUNT_FILE)


# Загрузка переменных окружения из .env файла
load_dotenv()

# Приватные константы, не экспортируемые наружу
_SAMPLE_SPREADSHEET_ID = os.getenv('SAMPLE_SPREADSHEET_ID')
_SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')


_SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), _SERVICE_ACCOUNT_FILE)
_SHEET_NAME = os.getenv('SHEET_NAME')

# Загрузка учетных данных для аутентификации
_SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

_credentials = service_account.Credentials.from_service_account_file(
    _SERVICE_ACCOUNT_FILE, scopes=_SCOPES)

# Инициализация сервиса Google Sheets API
_service = build('sheets', 'v4', credentials=_credentials)

def _get_sheet_id(service, spreadsheet_id, sheet_name):
    """
    Получает идентификатор листа по его имени.
    """
    sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheets = sheet_metadata.get('sheets', '')
    
    for sheet in sheets:
        if sheet['properties']['title'] == sheet_name:
            return sheet['properties']['sheetId']
    
    raise ValueError(f"Лист с именем '{sheet_name}' не найден.")

def merge_cells(start_row, end_row, start_col, end_col):
    """
    Объединяет ячейки на указанном листе.
    """
    sheet_id = _get_sheet_id(_service, _SAMPLE_SPREADSHEET_ID, _SHEET_NAME)
    
    merge_range = {
        "sheetId": sheet_id,
        "startRowIndex": start_row,
        "endRowIndex": end_row,
        "startColumnIndex": start_col,
        "endColumnIndex": end_col
    }

    requests = [{
        "mergeCells": {
            "range": merge_range,
            "mergeType": "MERGE_ALL"
        }
    }]

    body = {
        'requests': requests
    }
    
    response = _service.spreadsheets().batchUpdate(
        spreadsheetId=_SAMPLE_SPREADSHEET_ID,
        body=body).execute()
    
    print(response)

def resize_row(start_row, end_row, pixel_size):
    sheet_id = _get_sheet_id(_service, _SAMPLE_SPREADSHEET_ID, _SHEET_NAME)
    
    requests = [{
        "updateDimensionProperties": {
            "range": {
                "sheetId": sheet_id,
                "dimension": "ROWS",  # Изменение высоты строки
                "startIndex": start_row,
                "endIndex": end_row
            },
            "properties": {
                "pixelSize": pixel_size  # Высота в пикселях
            },
            "fields": "pixelSize"
        }
    }]

    body = {
        'requests': requests
    }
    
    response = _service.spreadsheets().batchUpdate(
        spreadsheetId=_SAMPLE_SPREADSHEET_ID,
        body=body).execute()
    
    print(response)

def big_last_row(list_name='Follow'):
    sheet = _service.spreadsheets()
        
    # Получаем последний заполненный ряд в колонке A
    range_name = f"{list_name}!A:A"
    result = sheet.values().get(spreadsheetId=_SAMPLE_SPREADSHEET_ID, range=range_name).execute()
    values = result.get('values', [])
    
    # Определяем следующую пустую строку
    line_num = len(values) + 1

    merge_cells(line_num-1, line_num, 0, 8)
    resize_row(line_num-1, line_num, 80)
def write_to_google_sheets(data, cell=None, list_name='Follow'):
    """
    Записывает данные в Google Sheets на указанный лист.
    """
    if not cell:

        sheet = _service.spreadsheets()
        
        # Получаем последний заполненный ряд в колонке A
        range_name = f"{list_name}!A:A"
        result = sheet.values().get(spreadsheetId=_SAMPLE_SPREADSHEET_ID, range=range_name).execute()
        values = result.get('values', [])
        
        # Определяем следующую пустую строку
        last_row = len(values) + 1

        cell = f"A{last_row}"
    
    # Определяем диапазон для записи данных
    range_name = f"{list_name}!{cell}"
    print(f"Запись данных в диапазон: {range_name}")
    
    # Записываем данные
    result = sheet.values().update(
        spreadsheetId=_SAMPLE_SPREADSHEET_ID,
        range=range_name,
        valueInputOption="USER_ENTERED",
        body={"values": data}
    ).execute()
    
    print(f"Результат обновления: {result}")
def write_to_google_sheets2(data, cell='A1',LIST_NAME='New Coins'):
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=_SCOPES)
    
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    range_name = f"{LIST_NAME}!A:A"  # Assuming the column A is used for row numbers
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_name).execute()
    values = result.get('values', [])
    last_row = len(values) + 1
    cell='A'+str(last_row)
    range_name = f"{LIST_NAME}!{cell}"
    print(range_name)
    result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                   range=range_name,
                                   valueInputOption="USER_ENTERED",
                                   body={"values":data}).execute()
    print(result)

# to_write = [['testiiiiim','2222']]
# write_to_google_sheets(to_write, cell='A6')