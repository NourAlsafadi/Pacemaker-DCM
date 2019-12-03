from openpyxl import load_workbook
import TextFileManipulation


book = load_workbook(filename = 'database.xlsx')

USERS = book.get_sheet_by_name('USERS')
PARAMETERS = book.get_sheet_by_name('PARAMETERS')


numUsers = USERS.max_row-13

def registerUser(username,password):
    
    USERS['B'+str(numUsers+1)] = username
    USERS['C'+str(numUsers+1)] = password

    book.save('database.xlsx')

    return True

def getUserID(username):
    for row in USERS.iter_rows("B"):
        for cell in row:
            if cell.value == username:
                return USERS.cell(row=cell.row, column=1).value 

def setParameter():
        
    return

def signalSerial():
    return