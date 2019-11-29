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
from kivy.lang import Builder
from kivy.config import Config

from TextFileManipulation import UserPassCheck, databaseIsFull, addUser, passwordConfirm
import DatabaseManipulation

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

common = ['Maximum Sensor Rate','Activity Threshold', 'Reaction Time', 'Response Factor', 'Recovery Time']

AOORParameters = AOOParameters + common 
VOORParameters = VOOParameters + common
AAIRParameters = AAIParameters + common
VVIRParameters = VVIParameters + common
DOORParameters = limits + A + V + common + ['Fixed AV Delay'] 
######################################################### parameter values
tp1 = tuple( [str(x) for x in range(30,55,5)])
tp2 = tuple( [str(x) for x in range(51,91)] )
tp3 = tuple( [str(x) for x in range(95,180,5)] )

tp4 = tuple( [str(x) for x in range(50,180,5)] )
tp5 = tuple(["0.05"]) + tuple( [str(x/10) for x in range(1,20,1)] )
tp6 = tuple( ["off"] + [str(x/10) for x in range(5,33,1)] + [str(x/10) for x in range(35,75,5)] )

tp7 = tuple( ["0.25","0.5","0.7"] + [str(x/10) for x in range(1,11,1)])
tp8 = tuple( [str(x) for x in range(150,510,10)] )
tp9 = tuple(["off"] + [str(x) for x in range(3,24,3)] + ["25"])

tp10 = ("V-Low","Low","Med-Low","Med","Med-High","High","V-High")
tp11 = tuple([str(x) for x in range(10,60,10)])
tp12 = tuple([str(x) for x in range(1,17)])
tp13 = tuple([str(x) for x in range(2,17)])
tp14 = tuple([str(x) for x in range(70,310,10)])

ParameterValues =	{
  "Lower Rate Limit": [tp1 + tp2 + tp3,"60"],
  "Upper Rate Limit": [tp4,"120"],
  "Atrial Amplitude": [tp6,"3.5"],
  "Atrial Pulse Width": [tp5,"0.4"],
  "Ventricular Amplitude": [tp6,"3.5"],
  "Ventricular Pulse Width": [tp5,"0.5"],
  "Atrial Sensitivity": [tp7,"0.75"],
  "ARP": tp8,
  "PVARP": tp8,
  "Hysteresis": tuple(["off"]) + tp1 + tp2 + tp3,
  "Rate Smoothing": tp9,
  "Ventricular Sensitivity": [tp7,"2.5"],
  "VRP": [tp8,"320"],
  "Maximum Sensor Rate": [tp4,"120"],
  "Activity Threshold": [tp10,"Med"],
  "Reaction Time": [tp11,"30"],
  "Response Factor": [tp12,"8"],
  "Recovery Time": [tp13,"5"],
  "Fixed AV Delay": [tp14,"150"]
}

#### Classes to add widgets to screen for each pacing mode
#refer to main.kv for description of each class
class TableAOO(BoxLayout):
    def __init__(self, **kwargs):
        super(TableAOO, self).__init__(**kwargs)
        for element in AOOParameters:
            self.add_widget(RowAOO(element))

        self.add_widget(statusBar())
        

class RowAOO(BoxLayout):
    txt = StringProperty()
  

    def __init__(self, row, **kwargs):
        super(RowAOO, self).__init__(**kwargs)
        self.txt = row

    def getValues(name):
        return ParameterValues[name][0]

    def getNominal(name):
        return ParameterValues[name][1]

#------
class TableVOO(BoxLayout):
    def __init__(self, **kwargs):
        super(TableVOO, self).__init__(**kwargs)
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
        for element in DOOParameters:
            self.add_widget(RowDOO(element))
        self.add_widget(statusBar())
        
class RowDOO(BoxLayout):
    txt = StringProperty()
    def __init__(self, row, **kwargs):
        super(RowDOO, self).__init__(**kwargs)
        self.txt = row
#------
class TableAOOR(BoxLayout):
    def __init__(self, **kwargs):
        super(TableAOOR, self).__init__(**kwargs)
        for element in AOORParameters:
            self.add_widget(RowAOOR(element))
        self.add_widget(statusBar())
        
class RowAOOR(BoxLayout):
    txt = StringProperty()
    def __init__(self, row, **kwargs):
        super(RowAOOR, self).__init__(**kwargs)
        self.txt = row
#------
class TableVOOR(BoxLayout):
    def __init__(self, **kwargs):
        super(TableVOOR, self).__init__(**kwargs)
        for element in VOORParameters:
            self.add_widget(RowVOOR(element))
        self.add_widget(statusBar())
        
class RowVOOR(BoxLayout):
    txt = StringProperty()
    def __init__(self, row, **kwargs):
        super(RowVOOR, self).__init__(**kwargs)
        self.txt = row
#------
class TableAAIR(BoxLayout):
    def __init__(self, **kwargs):
        super(TableAAIR, self).__init__(**kwargs)
        for element in AAIRParameters:
            self.add_widget(RowAAIR(element))
        self.add_widget(statusBar())
        
class RowAAIR(BoxLayout):
    txt = StringProperty()
    def __init__(self, row, **kwargs):
        super(RowAAIR, self).__init__(**kwargs)
        self.txt = row
#------
class TableVVIR(BoxLayout):
    def __init__(self, **kwargs):
        super(TableVVIR, self).__init__(**kwargs)
        for element in VVIRParameters:
            self.add_widget(RowVVIR(element))
        self.add_widget(statusBar())
        
class RowVVIR(BoxLayout):
    txt = StringProperty()
    def __init__(self, row, **kwargs):
        super(RowVVIR, self).__init__(**kwargs)
        self.txt = row

#------
class TableDOOR(BoxLayout):
    def __init__(self, **kwargs):
        super(TableDOOR, self).__init__(**kwargs)
        
        self.add_widget(titles())
        for element in DOORParameters:
            self.add_widget(RowDOOR(element))
        self.add_widget(statusBar())
        
        
class RowDOOR(BoxLayout):
    txt = StringProperty()
    def __init__(self, row, **kwargs):
        super(RowDOOR, self).__init__(**kwargs)
        self.txt = row
#------

class titles(BoxLayout):
    def __init__(self,**kwargs):
        super(titles,self).__init__(**kwargs)
    
class statusBar(BoxLayout):
    def __init__(self,**kwargs):
        super(statusBar,self).__init__(**kwargs)

    def returnConnection(self):
        runtimeApp.screen_manager.current='Connection'

###########
#screen for displaying and modifying pacing mode parameters
class Parameters(TabbedPanel):
    def __init__(self, **kwargs):
        super(Parameters, self).__init__(**kwargs)
        
        
    def getTab(self):
        return self.get_tab_list(self)


# def getValues(name):
#     return ParameterValues[name][0]

# def getNominal(name):
#     return ParameterValues[name][1]


    



##########
#app (screen_manager)
class PacemakerApp(App):

    def build(self):
        self.screen_manager=ScreenManager()

        ####### Login
        #instantiate class above describing screen
        self.Login_screen=LoginScreen()
        #create screen object
        screen=Screen(name='Login')
        #add class instance to describe screen
        screen.add_widget(self.Login_screen)
        #add the screen to the manager
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



########################

