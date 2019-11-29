from openpyxl import Workbook
import TextFileManipulation


book = Workbook()    #open a new workbook
filepath="database.xlsx"  #set directory for the excel file
book.save(filepath)

USERS = book.get_sheet_by_name('USERS')
#DEVICES = book.get_sheet_by_name('DEVICES')
#CONNECTIONS = book.get_sheet_by_name('CONNECTIONS')
PARAMETERS = book.get_sheet_by_name('PARAMETERS')


numUsers = USERS.max_row
#numDevices = DEVICES.max_row
#numConnections = CONNECTIONS.max_row

def registerUser(username,password):
    
    USERS['B'+str(numUsers)] = username
    USERS['C'+str(numUsers)] = password

    book.save(filepath)
    return True

#def getUserID(username):

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