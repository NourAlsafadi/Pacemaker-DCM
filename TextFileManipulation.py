'''
python file manipulation tests
input username and password and compare
to text file
'''

#checking if entered username and password are in file
#used for login
#returns true or false
def UserPassCheck(username, password):

    accountsFile=open("Accounts.txt","r")
    fileLines=accountsFile.readlines()

    usernameFlag=False
    
    for line in fileLines:
        if usernameFlag==True:
            if line[:-1]==password:
                #login info matches records
                accountsFile.close()
                return True

        if line[:-1]==username: 
            usernameFlag=True
        else:
            usernameFlag=False
        
        


    accountsFile.close()

    return False

        

#function to check if the password is correct for
#new user registration
def passwordConfirm(password,confirm):

    if password==confirm:
        return True
    else:
        return False
    

#checks if max number of users have been registered    
def databaseIsFull():
    accountsFile=open("Accounts.txt","r")
    fileLines=accountsFile.readlines()

    if len(fileLines)>=20:
        accountsFile.close()
        return True
    else:
        accountsFile.close()
        return False


def addUser(username,password):
    accountsFile=open("Accounts.txt","a")#change to append? find out if append can create new file

    accountsFile.write(username+"\n")
    accountsFile.write(password+"\n")

    accountsFile.close()
    
#debugging function prints every line in file
#not called by main script
def FileRead():

    accountsFile=open("Accounts.txt","r")
    fileLine=accountsFile.readlines()

    for line in fileLine:
        print(line)

    print(len(fileLine))
