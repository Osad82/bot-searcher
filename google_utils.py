import gspread
from oauth2client.service_account import ServiceAccountCredentials

from config import *





def get_list_of_rows(url):
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name('spread sheets-ec938419569a.json', scope)

    gc = gspread.authorize(credentials)

    # Open a worksheet from spreadsheet with one shot
    sh = gc.open_by_url(url)

    sheet = sh.get_worksheet(0)    
    list_of_lists = sheet.get_all_values()

    return list_of_lists


def search_by_last_name(rows_list, last_name):
    last_name = last_name.lower()
    family_matching_list = []

    for row in rows_list:
        l_name = row[1].lower()
        if last_name == l_name:
            family_matching_list.append(row)
    
    return family_matching_list


def search_by_first_name(rows_list, first_name):
    if first_name == '':
        return rows_list
    first_name = first_name.lower()
    name_matching_list = []
    for row in rows_list:
        f_name = row[2].lower()
        if first_name == f_name:
            name_matching_list.append(row)
    
    return name_matching_list


def search_by_otchestvo(rows_list, otchestvo):
    if otchestvo == '':
        print(rows_list)
        return rows_list
    otchestvo = otchestvo.lower()
    otchestvo_matching_list = []
    for row in rows_list:
        o_name = row[3].lower()
        if otchestvo == o_name:
            otchestvo_matching_list.append(row)
    print(otchestvo_matching_list)
    return otchestvo_matching_list


def parse_fio(fio):
    if len(fio.split()) == 3:
        last_name, first_name, otchestvo = fio.split()

    if len(fio.split()) == 2:        
        last_name, first_name = fio.split()
        otchestvo = ''

    if len(fio.split()) == 1:
        last_name = fio
        first_name = ''
        otchestvo = ''

    return last_name, first_name, otchestvo    


def search(rows_list, fio):    
    last_name, first_name, otchestvo = parse_fio(fio)

    fam_list = search_by_last_name(rows_list, last_name)
    fam_name_list = search_by_first_name(fam_list, first_name)
    fam_name_otch_list = search_by_otchestvo(fam_name_list, otchestvo)

    return fam_name_otch_list

    




if __name__ == "__main__":
    rows_list = get_list_of_rows(SPREADSHEET_URL)
    search(rows_list, 'матюхин виктор')
