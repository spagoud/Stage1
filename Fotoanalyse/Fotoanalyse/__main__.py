# Tom Landzaat student @ EE THUAS
# student ID : 14073595
# date : 11-12-2017

#----------------------------------------Import needed librarys------------------------------------

import numpy as np
import cv2
import time
import math
import numpy.ma as ma
from time import sleep


#project .py files
from detection import detection
from color import color
from wait import wait

#----------------------------------------color definitions----------------------------------------


print('Preparing Colors...')


color('red', 340, 15)
color('orange', 16, 40)
color('yellow', 41, 70)
color('green', 71, 160)
color('light blue', 161, 190)
color('dark blue', 191, 270)
color('purple', 271, 339)

#----------------------------------------Kivy----------------------------------------

import kivy
import kivy.event

from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.uix.switch import Switch
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.dropdown import DropDown
from kivy.properties import ObjectProperty
from kivy import clock
from kivy.clock import Clock
from kivy.uix.widget import Widget


#-----------------------------------Screen definitions-----------------------------------

class StartScreen(Screen):
        
   def __init__(self, *args, **kwargs):
        super(StartScreen, self).__init__(*args, **kwargs)

        layout = StartScreenLayout()
        self.add_widget(layout)

class ResultScreen(Screen):

    def __init__(self, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)
        
        self.AllPercentages = ShowPercentages()
        self.add_widget(self.AllPercentages)

class CalculationScreen(Screen):

    def __init__(self, *args, **kwargs):
        super(CalculationScreen, self).__init__(*args, **kwargs)

    def CaculateResults(self):

        for image in detection.ListOfAllImages:
            image.StartColorDetection()

        detection.CalcAllPercentages()

        if detection.EnableWriteDataToTXTfile == True:
            detection.WriteDataToTXTfile()

        Interface.switch_to(ResultScreen())
        

class TakingPicturesScreen(Screen):

    def __init__(self, *args, **kwargs):
        super(TakingPicturesScreen, self).__init__(*args, **kwargs)
        
        self.StopTakingPicturesButton = Button(text = 'Stop Taking Pictures')
        self.StopTakingPicturesButton.bind(on_press = self.StopTakingPictures)

        self.add_widget(self.StopTakingPicturesButton)

    def StartTakingPictures(self):
      
        Clock.schedule_interval(self.TakePicture, 1)
         
    def TakePicture(self, interval):

        image = cv2.imread('C:\\Users\\tom_l\\OneDrive\\HHS\\Jaar_3\\stage_2\\test_image.png')
        detection(image)
        print('picture taken')

    def StopTakingPictures(self, interval):

        try:
            
            Clock.unschedule(self.TakePicture)
            print('stopped taking pictures')

        except NameError:
            pass

        Interface.switch_to(CalculationScreen())

class ConfigurationScreen(Screen):

    def __init__(self, *args, **kwargs):
        super(ConfigurationScreen, self).__init__(*args, **kwargs)
       
        Layout = ConfigurationScreenLayout()
        self.add_widget(Layout)

#-----------------------------------Layout definitions-----------------------------------

class StartScreenLayout(GridLayout):

    def __init__(self, **kwargs):
        super(StartScreenLayout, self).__init__(**kwargs)

        self.rows = 1
        self.cols = 2

        self.StartColorDetectionButton = Button(text = 'Start taking picture')
        self.StartColorDetectionButton.bind(on_press = self.GoToTakingPicuresScreen)

        self.GoToConfigButton = Button(text = 'Go to config settings' )
        self.GoToConfigButton.bind(on_press = self.GoToConfigurationScreen)
        
        self.add_widget(self.GoToConfigButton)
        self.add_widget(self.StartColorDetectionButton)

    def GoToTakingPicuresScreen(self, instance):
        Interface.switch_to(TakingPicturesScreen())

    def GoToConfigurationScreen(self, instance):
        Interface.switch_to(ConfigurationScreen())


class ConfigurationScreenLayout(GridLayout):

    def __init__(self, *args, **kwargs):
        super(ConfigurationScreenLayout, self).__init__(*args, **kwargs)

        self.rows = 11
        self.cols = 2

        #switches
        self.SaveDetectedPlasticImageSwitchLabel = Label(text = 'Save image with detected plastic for each picture: ')
        self.SaveDetectedPlasticImageSwitch = Switch()
        self.SaveDetectedPlasticImageSwitch.bind(active = self.TurnSaveDetectedPlasticImageOn)

        self.SaveBilateralfilterImageSwitchLabel = Label(text = 'Save image with bilateral filter for each picture: ')
        self.SaveBilateralfilterImageSwitch = Switch()
        self.SaveBilateralfilterImageSwitch.bind(active = self.TurnSaveBilateralfilterImageOn)

        self.WriteDataToTXTfileSwitchLabel = Label(text = 'Write data to .txt file: ')
        self.WriteDatatoTXTfileSwitch = Switch()
        self.WriteDatatoTXTfileSwitch.bind(active = self.WriteDataToTXTfile)

        #integer textinput
        self.InputNumberOfDecimalLabel = Label(text = 'Set the number of decimals for the calculation: ')
        self.InputNumberOfDecimals = TextInput(text = '2', multiline = False, input_filter = 'int')
        self.InputNumberOfDecimals.bind(text = self.SetNumberOfDecimals)

        self.InputBeltValueLabel = Label(text = 'Set the value of the belt in "value" from HSV: ')
        self.InputBeltValue = TextInput(text = '40', multiline = False, input_filter = 'int')
        self.InputBeltValue.bind(text = self.SetBeltValue)

        self.InputBlackValueLabel = Label(text = 'Set the value of the color black in "value" from HSV: ')
        self.InputBlackValue = TextInput(text = '20', multiline = False, input_filter = 'int')
        self.InputBlackValue.bind(text = self.SetBlackValue)

        self.InputWhiteValueLabel = Label(text = 'Set the value of the color white in "value" from HSV: ')
        self.InputWhiteValue = TextInput(text = '75', multiline = False, input_filter = 'int')
        self.InputWhiteValue.bind(text = self.SetWhiteValue)
        
        self.InputMaxSaturationValueLabel = Label(text = 'The maximal saturation of "S" in HSV for a color the to be \ndefined as white/grey/black: ')
        self.InputMaxSaturationValue = TextInput(text = '25', multiline = False, input_filter = 'int')
        self.InputMaxSaturationValue.bind(text = self.SetMaxSaturation)

        self.InputBeltSpeedSettingLabel = Label(text = 'Input the setting of the belt')
        self.InputBeltSpeedSetting = TextInput(text = '0', multiline = False, input_filter = 'int')
        self.InputBeltSpeedSetting.bind(text = self.SetBeltSpeedSetting)

        self.InputPictureWidthLabel = Label(text = 'Input the width of the pictures in meters')
        self.InputPictureWidth = TextInput(text = '0.165', multiline = False, input_filter = 'int')
        self.InputPictureWidth.bind(text = self.SetPictureWidth)
        
        #buttons
        self.ReturnToStartScreenButton = Button(text = 'Return to startscreen')
        self.ReturnToStartScreenButton.bind(on_press = self.GoToStartScreen)

        #IMPORTANT: first add label, then the widgets
        self.add_widget(self.SaveDetectedPlasticImageSwitchLabel)
        self.add_widget(self.SaveDetectedPlasticImageSwitch)

        self.add_widget(self.SaveBilateralfilterImageSwitchLabel)
        self.add_widget(self.SaveBilateralfilterImageSwitch)

        self.add_widget(self.WriteDataToTXTfileSwitchLabel)
        self.add_widget(self.WriteDatatoTXTfileSwitch)

        self.add_widget(self.InputNumberOfDecimalLabel)
        self.add_widget(self.InputNumberOfDecimals)

        self.add_widget(self.InputBeltValueLabel)
        self.add_widget(self.InputBeltValue)

        self.add_widget(self.InputBlackValueLabel)
        self.add_widget(self.InputBlackValue)

        self.add_widget(self.InputWhiteValueLabel)
        self.add_widget(self.InputWhiteValue)

        self.add_widget(self.InputMaxSaturationValueLabel)
        self.add_widget(self.InputMaxSaturationValue)

        self.add_widget(self.InputBeltSpeedSettingLabel)
        self.add_widget(self.InputBeltSpeedSetting)

        self.add_widget(self.InputPictureWidthLabel)
        self.add_widget(self.InputPictureWidth)
        
        self.add_widget(self.ReturnToStartScreenButton)

    def GoToStartScreen(self, instance):
        Interface.switch_to(StartScreen())

    def WriteDataToTXTfile(self, instance, value):

        if value == True:
            detection.WriteDataToTXTfile = True

        else:
            detection.WriteDataToTXTfile = False


    def SetPictureWidth(self, instance, value):

        wait.PictureWidth = value
        wait.CalculateWaitingTime()

    def SetBeltSpeedSetting(self, instance, value):

        wait.BeltSpeed = value
        wait.CalculateWaitingTime()

    def SetMaxSaturation(self, instance, value):

        detection.SetMaxSaturation = value
        

    def SetWhiteValue(self, instnace, value):

        detection.WhiteValue = value
        

    def SetBlackValue(self, instance, value):

        detection.BlackValue = value
        

    def SetBeltValue(self, instance, value):

        detection.AmountOfPicturestToBeTaken = value
        

    def SetNumberOfDecimals(self, instance, value):

        detection.NumberOfDecimals = value
        


    def TurnSaveBilateralfilterImageOn(self, instance, value):
        if value == True:
            detection.SaveBilateralfilterImage = True
            print('saving all images with bilateral filter')
        else: 
            detection.SaveBilateralfilterImage = False
            print('deactivated saving all images with bilateral filter')
  
    def TurnSaveDetectedPlasticImageOn(self, instance, value):
        if value == True:
            detection.SaveDetectedPlasticImage = True 
            print('saving all images with detected plastic flakes')
        else:
            detection.SaveBilateralfilterImage = False 
            print('deactivated saving all images with detected plastic flakes')


class ShowPercentages(BoxLayout):

    def __init__(self, **kwargs):
        super(ShowPercentages, self).__init__(**kwargs)

        self.LabelBlack = Label(text = '{}% is black'.format(detection.PercentageBlack))
        self.LabelGrey = Label(text = '{}% is grey'.format(detection.PercentageGrey))
        self.LabelWhite = Label(text = '{}% is white'.format(detection.PercentageWhite))

        self.add_widget(self.LabelBlack)
        self.add_widget(self.LabelGrey)
        self.add_widget(self.LabelWhite)

        for CurrentColor in color.AllColors:
            self.CurrentLabel = Label(text = '{}% is {}'.format(CurrentColor.Percentage, CurrentColor.name))
            self.add_widget(self.CurrentLabel)

      
#-----------------------------------Top level kivy, screenmanager-----------------------------------             
          
Builder.load_file('interface.kv')

Interface = ScreenManager()

Start = StartScreen(name = 'Start')
Configuration = ConfigurationScreen(name = 'Configuration')
TakingPictures = TakingPicturesScreen(name = 'TakingPicturesScreen')
Results = ResultScreen(name = 'Results')
Calculating = CalculationScreen(name = 'Calculating')


Interface.add_widget(Start)
Interface.add_widget(Configuration)
Interface.add_widget(TakingPictures)
Interface.add_widget(Calculating)
Interface.add_widget(Results)


class ColorApp(App):

    def build(self):
       
        return Interface

ColorApp().run()



#----------------------------------------END PROGRAM----------------------------------------

























    





                
               


