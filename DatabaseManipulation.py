from openpyxl import load_workbook
import TextFileManipulation
import Parameters 


book = load_workbook(filename = 'database.xlsx')

USERS = book.get_sheet_by_name('USERS')
PARAMETERS = book.get_sheet_by_name('PARAMETERS')


activeUser = ''
currentM = 'AOO'
activeValues = [ Parameters.ParameterValues['Lower Rate Limit'][1], Parameters.ParameterValues['Maximum Rate Sensor'][1],  Parameters.ParameterValues['Fixed AV Delay'][1],  Parameters.ParameterValues['Atrial Amplitude'][1], Parameters.ParameterValues['Ventricular Amplitude'][1], Parameters.ParameterValues['Atrial Pulse Width'][1], Parameters.ParameterValues['Ventricular Pulse Width'][1],  Parameters.ParameterValues['VRP'][1],  Parameters.ParameterValues['ARP'][1],  Parameters.ParameterValues['Activity Threshold'][1],  Parameters.ParameterValues['Reaction Time'][1]	, Parameters.ParameterValues['Response Factor'][1],	 Parameters.ParameterValues['Recovery Time'][1]]

def registerUser(username,password):
    
    i=1
    for row in USERS.values:
        if(row[1] == None):
            break
        i += 1
    
    USERS['B'+ str(i)] = username
    USERS['C'+ str(i)] = password

    book.save('database.xlsx')

    return True

def getUserID(username):
    i=1
    for row in USERS.values:
        if(row[1] == activeUser):
            return i
        i += 1
    return False
    

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

def getParameters(AU):
    
    if(getUserID(activeUser) == False):
        return []

    data = []
    for i in range(13):
        data.append(PARAMETERS[str(chr(ord('C') + i)) + str(getUserID(AU)) ])
    return data


def signalSerial():
    return