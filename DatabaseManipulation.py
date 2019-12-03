from openpyxl import load_workbook
import TextFileManipulation
import Parameters


book = load_workbook(filename = 'database.xlsx')

USERS = book.get_sheet_by_name('USERS')
PARAMETERS = book.get_sheet_by_name('PARAMETERS')


numUsers = 2
activeUser = ''
currentM = 'AOO'

def registerUser(username,password):
    
    global numUsers
    USERS['B'+ str(numUsers)] = username
    USERS['C'+ str(numUsers)] = password
    
    numUsers += 1

    book.save('database.xlsx')

    return True

def getUserID(username):
    i=1
    for row in USERS.values:
        if(row[1] == activeUser):
            return i
        i += 1
    

def setParameters():
    PARAMETERS['B' + str(getUserID(activeUser))] = currentM
    print('B'+ currentM)
    for i in range(0,13):
        if(currentM == 'AOO'):
            PARAMETERS[str(chr(ord('C') + i)) + str(getUserID(activeUser)) ] = Parameters.allValuesAOO[i]
        if(currentM == 'VOO'):
            PARAMETERS[str(chr(ord('C') + i)) + str(getUserID(activeUser)) ] = Parameters.allValuesVOO[i]
        if(currentM == 'AAI'):
            PARAMETERS[str(chr(ord('C') + i)) + str(getUserID(activeUser)) ] = Parameters.allValuesAAI[i]
        if(currentM == 'VVI'):
            PARAMETERS[str(chr(ord('C') + i)) + str(getUserID(activeUser)) ] = Parameters.allValuesVVI[i]
        if(currentM == 'DOO'):
            PARAMETERS[str(chr(ord('C') + i)) + str(getUserID(activeUser)) ] = Parameters.allValuesDOO[i]
    
    book.save('database.xlsx')
    return


def signalSerial():
    return