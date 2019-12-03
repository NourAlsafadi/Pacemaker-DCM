import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.config import Config

from TextFileManipulation import UserPassCheck, databaseIsFull, addUser, passwordConfirm
import DatabaseManipulation
import Parameters as p

#loads kv file
Builder.load_file('main.kv')

#prevents the window from being resized and screwing up the float layout
Config.set('graphics','resizable', False)
Config.set('graphics','width', '900')
Config.set('graphics','height', '700')
Config.write()
###########

#Login screen stlye and button functionality
class LoginScreen(FloatLayout):

    def __init__(self,**kwargs):
        super(LoginScreen,self).__init__(**kwargs)
        self.loginFlag=True

        self.size=[300,300]
        self.title=Label(text='Welcome to the Pace Maker DCM',font_size=30,size_hint=[.5,.05],pos=[200,500])
        self.add_widget(self.title)
        self.usernameLabel=Label(text='Username',font_size=20,size_hint=[.25,.05],pos=[150,400])
        self.add_widget(self.usernameLabel)

        self.usernameInput=TextInput(write_tab=False,multiline=False,size_hint=[.30,.05],pos=[450,400])
        self.add_widget(self.usernameInput)

        self.passwordLabel=Label(text='Password',font_size=20,size_hint=[.25,.05],pos=[150,350])
        self.add_widget(self.passwordLabel)

        self.passconfirmLabel=Label(text='Confirm Password',font_size=20,size_hint=[.25,.05],pos=[150,300],color=[1,1,1,0])
        self.add_widget(self.passconfirmLabel)

        self.passwordInput=TextInput(write_tab=False,multiline=False,password=True,size_hint=[.30,.05],pos=[450,350])
        self.add_widget(self.passwordInput)

        self.passconfirmLabel=Label(text='Confirm Password',font_size=20,size_hint=[.25,.05],pos=[150,300],color=[1,1,1,0])
        self.add_widget(self.passconfirmLabel)

        self.passconfirmInput=TextInput(write_tab=False,multiline=False,password=True,size_hint=[.30,.05],pos=[450,300],readonly=True,background_color=[1,1,1,0],cursor_color=[1,0,0,0])
        self.add_widget(self.passconfirmInput)

        self.wrongPassword=Label(text='Username and Password do not match existing users',size_hint=[.4,.05],pos=[250,250],color=[1,1,1,0])
        self.add_widget(self.wrongPassword)

        self.maxNumUsers=Label(text='Maximum number of Users have been registered',size_hint=[.4,.05],pos=[250,250],color=[1,1,1,0])
        self.add_widget(self.maxNumUsers)

        self.noMatchPassword=Label(text='The password does not match',size_hint=[.4,.05],pos=[250,250],color=[1,1,1,0])
        self.add_widget(self.noMatchPassword)

        self.submitButton=Button(text='Login',size_hint=[.10,.05],pos=[350,200])
        self.submitButton.bind(on_press=self.submitPress)
        self.add_widget(self.submitButton)

        self.switchLayoutButton=Button(text='Register A New User',size_hint=[.2,.05],pos=[310,150])
        self.switchLayoutButton.bind(on_press=self.switchLayoutPress)
        self.add_widget(self.switchLayoutButton)
  
    def submitPress(self, instance):
        username=self.usernameInput.text
        password=self.passwordInput.text
        passconfirm=self.passconfirmInput.text

        if self.loginFlag==True:
            #logic to check username and password are correct
            if UserPassCheck(username,password) and username!="":
                self.wrongPassword.color=[1,1,1,0]
                runtimeApp.screen_manager.current='Connection'
            else:
                self.wrongPassword.color=[1,1,1,1]
            
        else:
            #logic to add new user to file
            if databaseIsFull():
                self.maxNumUsers.color=[1,1,1,1]
            elif passwordConfirm(password,passconfirm)==False:
                self.noMatchPassword.color=[1,1,1,1]
            else:
                if username!="" and password != "":
                    addUser(username,password)
                    self.noMatchPassword.color=[1,1,1,0]
                    self.maxNumUsers.color=[1,1,1,0]
            
        self.usernameInput.text=""
        self.passwordInput.text=""
        self.passconfirmInput.text=""

    def switchLayoutPress(self,instance):

        if self.loginFlag==True:
            #switching from login to register mode
            self.wrongPassword.color=[1,1,1,0]
            self.passconfirmLabel.color=[1,1,1,1]
            self.passconfirmInput.background_color=[1,1,1,1]
            self.passconfirmInput.cursor_color=[1,0,0,1]
            self.passconfirmInput.readonly=False
            self.passconfirmInput.text=""
            
            self.usernameLabel.text='New Username'
            self.passwordLabel.text='New Password'
            
            self.submitButton.text='Register'
            self.switchLayoutButton.text='Login Existing User'
            
            self.loginFlag=False
        
        else:		        
	        #switching from register to login mode
            self.maxNumUsers.color=[1,1,1,0]
            self.noMatchPassword.color=[1,1,1,0]
            
            self.passconfirmLabel.color=[1,1,1,0]

            self.passconfirmInput.background_color=[1,1,1,0]
            self.passconfirmInput.cursor_color=[1,0,0,0]
            self.passconfirmInput.readonly=True

            self.usernameLabel.text='Username'
            self.passwordLabel.text='Password'

            
            self.submitButton.text='Login'
            self.switchLayoutButton.text='Register a new user'

            self.loginFlag=True

#screen for connecting with device
class Connection(BoxLayout):
    def __init__(self,**kwargs):
        super(Connection,self).__init__(**kwargs)
    
    def status(self):
        status = 'Connected'
        return 'Status: ' + status
    
    def color(self):
        if self.status() == 'Status: Connected':
            return (0,1,0.5,1)
        elif self.status() == 'Status: Disconnected':
            return (1,0.25,0.25,1)
        elif self.status() == 'Status: Device Unrecognized':
            return (1,0.9,0.25,1)

    def showPacingModes(self):
        if self.status() == 'Status: Connected':
            return True
        else:
            return False

    def disconnect(self):
        if self.status() == 'Status: Connected':
            return 'Disconnect from Device'
        else:
            return 'Connect to Device'

    def Logout(self):

        runtimeApp.screen_manager.current='Login'
        
    def pacingModesScreen(self):
        runtimeApp.screen_manager.current='Parameters'

######################################################### pacing mode parameters
limits = ['Lower Rate Limit', 'Upper Rate Limit']
A = ['Atrial Amplitude', 'Atrial Pulse Width'] 
V = ['Ventricular Amplitude', 'Ventricular Pulse Width'] 

AOOParameters = limits + A
VOOParameters = limits + V
AAIParameters = limits + A + ['Atrial Sensitivity','ARP','PVARP','Hysteresis','Rate Smoothing'] 
VVIParameters = limits + V + ['Ventricular Sensitivity','VRP','Hysteresis','Rate Smoothing'] 
DOOParameters = limits + A + V + ['Fixed AV Delay'] 

#### Classes to add widgets to screen for each pacing mode
#refer to main.kv for description of each class
#------


class TableAOO(BoxLayout):
    def __init__(self, **kwargs):
        super(TableAOO, self).__init__(**kwargs)
        self.add_widget(title())

        for element in AOOParameters:
            self.add_widget(RowAOO1())
            self.add_widget(RowAOO2())
            self.add_widget(RowAOO3())
            self.add_widget(RowAOO4())

        self.add_widget(statusBar())                

class RowAOO1(BoxLayout):
    def __init__(self, **kwargs):
        super(RowAOO, self).__init__(**kwargs)

#------
class TableVOO(BoxLayout):
    def __init__(self, **kwargs):
        super(TableVOO, self).__init__(**kwargs)
        self.add_widget(title())
        for element in VOOParameters:
            self.add_widget(RowVOO(element))
        self.add_widget(statusBar())
        
class RowVOO(BoxLayout):
    txt = StringProperty()
    def __init__(self, row, **kwargs):
        super(RowVOO, self).__init__(**kwargs)
        self.txt = row
#------
class TableAAI(BoxLayout):
    def __init__(self, **kwargs):
        super(TableAAI, self).__init__(**kwargs)
        self.add_widget(title())
        for element in AAIParameters:
            self.add_widget(RowAAI(element))
        self.add_widget(statusBar())
        
class RowAAI(BoxLayout):
    txt = StringProperty()
    def __init__(self, row, **kwargs):
        super(RowAAI, self).__init__(**kwargs)
        self.txt = row
#------
class TableVVI(BoxLayout):
    def __init__(self, **kwargs):
        super(TableVVI, self).__init__(**kwargs)
        self.add_widget(title())
        for element in VVIParameters:
            self.add_widget(RowVVI(element))
        self.add_widget(statusBar())
        
class RowVVI(BoxLayout):
    txt = StringProperty()
    def __init__(self, row, **kwargs):
        super(RowVVI, self).__init__(**kwargs)
        self.txt = row
#------
class TableDOO(BoxLayout):
    def __init__(self, **kwargs):
        super(TableDOO, self).__init__(**kwargs)
        self.add_widget(title())
        for element in DOOParameters:
            self.add_widget(RowDOO(element))
        self.add_widget(statusBar())
        
class RowDOO(BoxLayout):
    txt = StringProperty()
    def __init__(self, row, **kwargs):
        super(RowDOO, self).__init__(**kwargs)
        self.txt = row
#------
class statusBar(BoxLayout):
    def __init__(self,**kwargs):
        super(statusBar,self).__init__(**kwargs)

    def returnConnection(self):
        runtimeApp.screen_manager.current='Connection'

class title(BoxLayout):
    def __init__(self,**kwargs):
        super(title,self).__init__(**kwargs)

###########
#screen for displaying and modifying pacing mode parameters
class Parameters(TabbedPanel):
    def __init__(self, **kwargs):
        super(Parameters, self).__init__(**kwargs)
        
    def getTab(self):
        return self.get_tab_list(self)

##########
#app (screen_manager)
class PacemakerApp(App):
    currentMode = StringProperty()

    def build(self):
        self.screen_manager=ScreenManager()
        ####### Login
        #instantiate class above describing screen
        self.Login_screen=LoginScreen()
        #create screen object
        screen=Screen(name='Login')
        # add class instance to describe screen
        screen.add_widget(self.Login_screen)
        # add the screen to the manager
        self.screen_manager.add_widget(screen)
        
        ######## CONNECTION
        self.Connection_screen=Connection()
        screen=Screen(name='Connection')
        screen.add_widget(self.Connection_screen)
        self.screen_manager.add_widget(screen)


        ######## PARAMETERS
        self.Parameters_screen=Parameters()
        screen=Screen(name='Parameters')
        screen.add_widget(self.Parameters_screen)
        self.screen_manager.add_widget(screen)

        
        return self.screen_manager



###########
#running the program; main loop
if __name__=='__main__':
    runtimeApp=PacemakerApp()
    runtimeApp.run()



###########

