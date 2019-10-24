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

### KV FILE
Builder.load_file('main.kv')

### FUNCTIONALITY
from TextFileManipulation import UserPassCheck

#prevents the window from being resized and screwing up the float layout
Config.set('graphics','resizable', False)

#Login screen style and button functionality
class LoginScreen(FloatLayout):

    def __init__(self,**kwargs):

        super(LoginScreen,self).__init__(**kwargs)
        self.size=[300,300]
        self.title=Label(text='Welcome to the Pace Maker DCM',font_size=30,size_hint=[.5,.05],pos=[200,500])
        self.add_widget(self.title)
        self.usernameLabel=Label(text='Username',font_size=20,size_hint=[.25,.05],pos=[150,400])
        self.add_widget(self.usernameLabel)

        self.usernameInput=TextInput(multiline=False,size_hint=[.30,.05],pos=[450,400])
        self.add_widget(self.usernameInput)

        self.passwordLabel=Label(text='Password',font_size=20,size_hint=[.25,.05],pos=[150,300])
        self.add_widget(self.passwordLabel)

        self.passwordInput=TextInput(multiline=False,password=True,size_hint=[.30,.05],pos=[450,300])
        self.add_widget(self.passwordInput)

        self.submitButton=Button(text='Submit',size_hint=[.10,.05],pos=[350,200])
        self.submitButton.bind(on_press=self.pressed)
        self.add_widget(self.submitButton)

        self.newUserButton=Button(text='Register A New User',size_hint=[.2,.05],pos=[310,100])
        self.newUserButton.bind(on_press=self.newUserPress)
        self.add_widget(self.newUserButton)

    def pressed(self, instance):
        username=self.usernameInput.text
        password=self.passwordInput.text

        print("Match: " + UserPassCheck(username,password))
        self.usernameInput.text=""
        self.passwordInput.text=""
        runtimeApp.screen_manager.current='New'
        
    def newUserPress(self,instance):
        runtimeApp.screen_manager.current='NewUser'


#screen style and functionality to register a new user
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

#screen for choosing pacing modes
class PacingModes(FloatLayout):
   
    def __init__(self,**kwargs):
        super(PacingModes,self).__init__(**kwargs)
        self.size=[300,300]
        self.title=Label(text='Pacing Modes',font_size=30,size_hint=[.5,.05],pos=[200,500])
        self.add_widget(self.title)

        #### BUTTONS
        
        #AOO#
        self.AOO_mode=Button(text='AOO',size_hint=[.25,.25],pos=[515,250])
        self.AOO_mode.bind(on_press=self.AOOscreen)
        self.add_widget(self.AOO_mode)
        
        #VOO#
        self.VOO_mode=Button(text='VOO',size_hint=[.25,.25],pos=[315,100])
            #self.VOO_mode.bind(on_press=self.pressed)
        self.add_widget(self.VOO_mode)

        #AAI#
        self.AAI_mode=Button(text='AAI',size_hint=[.25,.25],pos=[315,250])
            #self.AAI_mode.bind(on_press=self.pressed)
        self.add_widget(self.AAI_mode)

        #VVI#
        self.VVI_mode=Button(text='VVI',size_hint=[.25,.25],pos=[515,100])
            #self.VVI_mode.bind(on_press=self.pressed)
        self.add_widget(self.VVI_mode)

    def AOOscreen(self, instance):
        runtimeApp.screen_manager.current='ParametersAOO'

    def VOOscreen(self, instance):
        runtimeApp.screen_manager.current='ParametersVOO'

    def AAIscreen(self, instance):
        runtimeApp.screen_manager.current='ParametersAAI'

    def VVIscreen(self, instance):
        runtimeApp.screen_manager.current='ParametersVVI'


#screen for displaying and modifying AOO parameters
AOOParameters = ['Lower Rate Limit', 'Upper Rate Limit', 'Atrial Amplitude', 'Atrial Pulse Width'] 

class Table(BoxLayout):
    def __init__(self, **kwargs):
        super(Table, self).__init__(**kwargs)
        for element in AOOParameters:
            self.add_widget(Row(element))

class Row(BoxLayout):
    txt = StringProperty()
    def __init__(self, row, **kwargs):
        super(Row, self).__init__(**kwargs)
        self.txt = row

class ParametersAOO(TabbedPanel):
    pass

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
        
class PacemakerApp(App):

    def build(self):
        self.screen_manager=ScreenManager()

        #instantiate class above describing screen
        self.Login_screen=LoginScreen()
        #create screen object
        screen=Screen(name='Login')
        #add class instance to describe screen
        screen.add_widget(self.Login_screen)
        #add the screen to the manager
        self.screen_manager.add_widget(screen)
        
        self.NewUserScreen=NewUser()
        screen=Screen(name='NewUser')
        screen.add_widget(self.NewUserScreen)
        self.screen_manager.add_widget(screen)
        
        self.New_screen=NewScreen()
        screen=Screen(name='New')
        screen.add_widget(self.New_screen)
        self.screen_manager.add_widget(screen)

        ######## PACING MODES
        self.PacingModes_screen=PacingModes()
        screen=Screen(name='PacingModes')
        screen.add_widget(self.PacingModes_screen)
        self.screen_manager.add_widget(screen)

        ######## AOO PARAMETERS
        self.ParametersAOO_screen=ParametersAOO()
        screen=Screen(name='ParametersAOO')
        screen.add_widget(self.ParametersAOO_screen)
        self.screen_manager.add_widget(screen)
        
        return self.screen_manager



if __name__=='__main__':
    runtimeApp=PacemakerApp()
    runtimeApp.run()
