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

#### Classes to add widgets to screen for each pacing mode
#refer to main.kv for description of each class
#------

class TableAOO(BoxLayout):
    def __init__(self, **kwargs):
        super(TableAOO, self).__init__(**kwargs)
        self.add_widget(title())

        self.add_widget(RowAOO1())
        self.add_widget(RowAOO2())
        self.add_widget(RowAOO3())
        self.add_widget(RowAOO4())

        self.add_widget(statusBar())                

class RowAOO1(BoxLayout):
    def __init__(self, **kwargs):
        super(RowAOO1, self).__init__(**kwargs)
class RowAOO2(BoxLayout):
    def __init__(self, **kwargs):
        super(RowAOO2, self).__init__(**kwargs)
class RowAOO3(BoxLayout):
    def __init__(self, **kwargs):
        super(RowAOO3, self).__init__(**kwargs)
class RowAOO4(BoxLayout):
    def __init__(self, **kwargs):
        super(RowAOO4, self).__init__(**kwargs)

#------
class TableVOO(BoxLayout):
    def __init__(self, **kwargs):
        super(TableVOO, self).__init__(**kwargs)
        self.add_widget(title())
            
        self.add_widget(RowVOO1())
        self.add_widget(RowVOO2())
        self.add_widget(RowVOO3())
        self.add_widget(RowVOO4())

        self.add_widget(statusBar())
        
class RowVOO1(BoxLayout):
    def __init__(self,**kwargs):
        super(RowVOO1, self).__init__(**kwargs)
class RowVOO2(BoxLayout):
    def __init__(self,**kwargs):
        super(RowVOO2, self).__init__(**kwargs)
class RowVOO3(BoxLayout):
    def __init__(self,**kwargs):
        super(RowVOO3, self).__init__(**kwargs)
class RowVOO4(BoxLayout):
    def __init__(self,**kwargs):
        super(RowVOO4, self).__init__(**kwargs)

#------
class TableAAI(BoxLayout):
    def __init__(self, **kwargs):
        super(TableAAI, self).__init__(**kwargs)
        self.add_widget(title())
        
        self.add_widget(RowAAI1())
        self.add_widget(RowAAI2())
        self.add_widget(RowAAI3())
        self.add_widget(RowAAI4())
        self.add_widget(RowAAI5())
        self.add_widget(RowAAI6())
        self.add_widget(RowAAI7())
        self.add_widget(RowAAI8())
        self.add_widget(RowAAI9())
        
        self.add_widget(statusBar())
        
class RowAAI1(BoxLayout):
    def __init__(self,**kwargs):
        super(RowAAI1, self).__init__(**kwargs)
class RowAAI2(BoxLayout):
    def __init__(self, **kwargs):
        super(RowAAI2, self).__init__(**kwargs)
class RowAAI3(BoxLayout):
    def __init__(self, **kwargs):
        super(RowAAI3, self).__init__(**kwargs)
class RowAAI4(BoxLayout):
    def __init__(self, **kwargs):
        super(RowAAI4, self).__init__(**kwargs)
class RowAAI5(BoxLayout):
    def __init__(self, **kwargs):
        super(RowAAI5, self).__init__(**kwargs)
class RowAAI6(BoxLayout):
    def __init__(self, **kwargs):
        super(RowAAI6, self).__init__(**kwargs)
class RowAAI7(BoxLayout):
    def __init__(self, **kwargs):
        super(RowAAI7, self).__init__(**kwargs)
class RowAAI8(BoxLayout):
    def __init__(self, **kwargs):
        super(RowAAI8, self).__init__(**kwargs)
class RowAAI9(BoxLayout):
    def __init__(self, **kwargs):
        super(RowAAI9, self).__init__(**kwargs)


#------
class TableVVI(BoxLayout):
    def __init__(self, **kwargs):
        super(TableVVI, self).__init__(**kwargs)
        
        self.add_widget(title())

        self.add_widget(RowVVI1())
        self.add_widget(RowVVI2())
        self.add_widget(RowVVI3())
        self.add_widget(RowVVI4())
        self.add_widget(RowVVI5())
        self.add_widget(RowVVI6())
        self.add_widget(RowVVI7())
        self.add_widget(RowVVI8())

        self.add_widget(statusBar())
        
class RowVVI1(BoxLayout):
    def __init__(self, **kwargs):
        super(RowVVI1, self).__init__(**kwargs)
class RowVVI2(BoxLayout):
    def __init__(self, **kwargs):
        super(RowVVI2, self).__init__(**kwargs)
class RowVVI3(BoxLayout):
    def __init__(self, **kwargs):
        super(RowVVI3, self).__init__(**kwargs)
class RowVVI4(BoxLayout):
    def __init__(self, **kwargs):
        super(RowVVI4, self).__init__(**kwargs)
class RowVVI5(BoxLayout):
    def __init__(self, **kwargs):
        super(RowVVI5, self).__init__(**kwargs)
class RowVVI6(BoxLayout):
    def __init__(self, **kwargs):
        super(RowVVI6, self).__init__(**kwargs)
class RowVVI7(BoxLayout):
    def __init__(self, **kwargs):
        super(RowVVI7, self).__init__(**kwargs)
class RowVVI8(BoxLayout):
    def __init__(self, **kwargs):
        super(RowVVI8, self).__init__(**kwargs)


#------
class TableDOO(BoxLayout):
    def __init__(self, **kwargs):
        super(TableDOO, self).__init__(**kwargs)
        
        self.add_widget(title())
        
        self.add_widget(RowDOO1())
        self.add_widget(RowDOO2())
        self.add_widget(RowDOO3())
        self.add_widget(RowDOO4())
        self.add_widget(RowDOO5())
        self.add_widget(RowDOO6())
        self.add_widget(RowDOO7())

        self.add_widget(statusBar())
        
class RowDOO1(BoxLayout):
    def __init__(self, **kwargs):
        super(RowDOO1, self).__init__(**kwargs)
class RowDOO2(BoxLayout):
    def __init__(self, **kwargs):
        super(RowDOO2, self).__init__(**kwargs)
class RowDOO3(BoxLayout):
    def __init__(self, **kwargs):
        super(RowDOO3, self).__init__(**kwargs)
class RowDOO4(BoxLayout):
    def __init__(self, **kwargs):
        super(RowDOO4, self).__init__(**kwargs)
class RowDOO5(BoxLayout):
    def __init__(self, **kwargs):
        super(RowDOO5, self).__init__(**kwargs)
class RowDOO6(BoxLayout):
    def __init__(self, **kwargs):
        super(RowDOO6, self).__init__(**kwargs)
class RowDOO7(BoxLayout):
    def __init__(self, **kwargs):
        super(RowDOO7, self).__init__(**kwargs)

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
    currentMode = StringProperty('AOO')

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

