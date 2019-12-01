from openpyxl import load_workbook
import TextFileManipulation


book = load_workbook(filename = 'database.xlsx')

USERS = book.get_sheet_by_name('USERS')
#DEVICES = book.get_sheet_by_name('DEVICES')
#CONNECTIONS = book.get_sheet_by_name('CONNECTIONS')
PARAMETERS = book.get_sheet_by_name('PARAMETERS')


numUsers = USERS.max_row
#numDevices = DEVICES.max_row
#numConnections = CONNECTIONS.max_row

def registerUser(username,password):
    
    USERS['B'+str(numUsers+1)] = username
    USERS['C'+str(numUsers+1)] = password

    book.save('database.xlsx')

    return True

def getUserID(username):
    for row in USERS.iter_rows("E"):
        for cell in row:
            if cell.value == username:
                return USERS.cell(row=cell.row, column=1).value 


# def registerDevice(deviceID):

#     USERS['B'+str(numDevices)] = deviceID

#     #book.save(filepath)
#     return True

# def connectDevice():
#     return

def setParameter():
    

    return

def signalSerial():
    return