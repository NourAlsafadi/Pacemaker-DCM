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
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.config import Config

from TextFileManipulation import UserPassCheck, databaseIsFull, addUser, passwordConfirm

#loads kv file
Builder.load_file('main.kv')

#prevents the window from being resized and screwing up the float layout
Config.set('graphics','resizable', False)

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

        self.usernameInput=TextInput(multiline=False,size_hint=[.30,.05],pos=[450,400])
        self.add_widget(self.usernameInput)

        self.passwordLabel=Label(text='Password',font_size=20,size_hint=[.25,.05],pos=[150,350])
        self.add_widget(self.passwordLabel)

        self.passconfirmLabel=Label(text='Confirm Password',font_size=20,size_hint=[.25,.05],pos=[150,300],color=[1,1,1,0])
        self.add_widget(self.passconfirmLabel)

        self.passwordInput=TextInput(multiline=False,password=True,size_hint=[.30,.05],pos=[450,350])
        self.add_widget(self.passwordInput)

        self.passconfirmLabel=Label(text='Confirm Password',font_size=20,size_hint=[.25,.05],pos=[150,300],color=[1,1,1,0])
        self.add_widget(self.passconfirmLabel)

        self.passconfirmInput=TextInput(multiline=False,password=True,size_hint=[.30,.05],pos=[450,300],readonly=True,background_color=[1,1,1,0],cursor_color=[1,0,0,0])
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
                if username!="":
                    addUser(username,password)
                
            
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


#screen for choosing pacing modes
class PacingModes(FloatLayout):
   
    def __init__(self,**kwargs):
        super(PacingModes,self).__init__(**kwargs)
        self.size=[300,300]
        self.title=Label(text='Pacing Modes',font_size=30,size_hint=[.5,.05],pos=[200,500])
        self.add_widget(self.title)
        
        #### BUTTONS
        
        #AOO#
        self.AOO_mode=Button(text='AOO',size_hint=[.25,.25],pos=[400,250])
        self.AOO_mode.bind(on_press= self.AOOscreen)
        self.add_widget(self.AOO_mode)
        
        #VOO#
        self.VOO_mode=Button(text='VOO',size_hint=[.25,.25],pos=[200,100])
        self.VOO_mode.bind(on_press=self.VOOscreen)
        self.add_widget(self.VOO_mode)

        #AAI#
        self.AAI_mode=Button(text='AAI',size_hint=[.25,.25],pos=[200,250])
            #self.AAI_mode.bind(on_press=self.pressed)
        self.AAI_mode.bind(on_press=self.AAIscreen)
        self.add_widget(self.AAI_mode)

        #VVI#
        self.VVI_mode=Button(text='VVI',size_hint=[.25,.25],pos=[400,100])
        self.VVI_mode.bind(on_press=self.VVIscreen)
        self.add_widget(self.VVI_mode)

    def AOOscreen(self, instance):
        runtimeApp.screen_manager.current= 'Parameters'

    def VOOscreen(self, instance):
        runtimeApp.screen_manager.current='Parameters'

    def AAIscreen(self, instance):
        runtimeApp.screen_manager.current='Parameters'

    def VVIscreen(self, instance):
        runtimeApp.screen_manager.current= 'Parameters'


# pacing mode parameters
AOOParameters = ['Lower Rate Limit', 'Upper Rate Limit', 'Atrial Amplitude', 'Atrial Pulse Width'] 
VOOParameters = ['Lower Rate Limit', 'Upper Rate Limit', 'Ventricular Amplitude', 'Ventricular Pulse Width'] 
AAIParameters = ['Lower Rate Limit', 'Upper Rate Limit', 'Atrial Amplitude', 'Atrial Pulse Width', 'Atrial Sensitivity','ARP','PVARP','Hysteresis','Rate Smoothing'] 
VVIParameters = ['Lower Rate Limit', 'Upper Rate Limit', 'Ventricular Amplitude', 'Ventricular Pulse Width','Ventricular Sensitivity','VRP','Hysteresis','Rate Smoothing'] 

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

        ######## PACING MODES
        self.PacingModes_screen=PacingModes()
        screen=Screen(name='PacingModes')
        screen.add_widget(self.PacingModes_screen)
        self.screen_manager.add_widget(screen)

        ######## PARAMETERS
        self.Parameters_screen=Parameters()
        screen=Screen(name='Parameters')
        screen.add_widget(self.Parameters_screen)
        self.screen_manager.add_widget(screen)

        '''
        self.NewUserScreen=NewUser()
        screen=Screen(name='NewUser')
        screen.add_widget(self.NewUserScreen)
        self.screen_manager.add_widget(screen)
        
        self.New_screen=NewScreen()
        screen=Screen(name='New')
        screen.add_widget(self.New_screen)
        self.screen_manager.add_widget(screen)
        '''
        
        return self.screen_manager



###########
#running the program; main loop
if __name__=='__main__':
    runtimeApp=PacemakerApp()
    runtimeApp.run()



########################
#screen style and functionality to register a new user
#functionality now handled by class LoginScreen
#remove?
'''
class NewUser(FloatLayout):

    def __init__(self,**kwargs):

        super(NewUser,self).__init__(**kwargs)
        self.size=[300,300]
        self.title=Label(text='Register a new user',font_size=30,size_hint=[.5,.05],pos=[200,500])
        self.add_widget(self.title)

        self.usernameLabel=Label(text='Username',font_size=20,size_hint=[.25,.05],pos=[150,400])
        self.add_widget(self.usernameLabel)
        
        self.usernameInput=TextInput(multiline=False,size_hint=[.30,.05],pos=[450,400])
        self.add_widget(self.usernameInput)

        self.passwordLabel=Label(text='Password',font_size=20,size_hint=[.25,.05],pos=[150,300])
        self.add_widget(self.passwordLabel)

        self.passwordInput=TextInput(multiline=False,password=True,size_hint=[.30,.05],pos=[450,300])
        self.add_widget(self.passwordInput)

        self.passconfirmLabel=Label(text='Confirm Password',font_size=20,size_hint=[.25,.05],pos=[150,200])
        self.add_widget(self.passconfirmLabel)

        self.passconfirmInput=TextInput(multiline=False,password=True,size_hint=[.30,.05],pos=[450,200])
        self.add_widget(self.passconfirmInput)

        self.submitButton=Button(text='Submit',size_hint=[.10,.05],pos=[350,100])
        self.submitButton.bind(on_press=self.pressed)
        self.add_widget(self.submitButton)

    def pressed(self,instance):
        print("Button has been pressed")
        runtimeApp.screen_manager.current='Login'

'''


#new screen used in testing
#remove?
'''
class NewScreen(GridLayout):

    def __init__(self, **kwargs):

        super(NewScreen,self).__init__(**kwargs)
        self.rows=3

        self.label1=Label(text='Hello World')
        self.add_widget(self.label1)

        self.button1=Button(text='Click me to switch back')
        self.button1.bind(on_press=self.press)
        self.add_widget(self.button1)

        self.button2=Button(text='Pacing Modes')
        self.button2.bind(on_press=self.pressP)
        self.add_widget(self.button2)
        

    def press(self, instance):
        runtimeApp.screen_manager.current='Login'

    def pressP(self, instance):
        runtimeApp.screen_manager.current='PacingModes'
'''
