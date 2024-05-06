import speech_recognition as sr
import RPi.GPIO as GPIO
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(20, 20, 600, 600)
        self.setWindowTitle("Task 7.2D")
        self.initUI()
        # allLEDsOff()
    
    def initUI(self):
        self.ligthOnLabel = QtWidgets.QLabel(self)
        self.lightOnPixmap = QtGui.QPixmap('./images/lightOnWB.png')
        self.ligthOnLabel.move(200,50)
        self.ligthOnLabel.resize(200,300)
        self.ligthOnLabel.setPixmap(self.lightOnPixmap)
        self.ligthOnLabel.hide()

        self.ligthOffLabel = QtWidgets.QLabel(self)
        self.lightOffPixmap = QtGui.QPixmap('./images/lightOffWB.png')
        self.ligthOffLabel.move(200,50)
        self.ligthOffLabel.resize(200,300)
        self.ligthOffLabel.setPixmap(self.lightOffPixmap)
        self.ligthOffLabel.show()

        self.voiceButton = QtWidgets.QPushButton(self) 
        self.voiceButton.resize(200, 50)
        self.voiceButton.move(200, 400)
        self.voiceButton.setText("Start Voice Recognition")
        self.voiceButton.clicked.connect(self.pressVoiceButton)

        self.voiceOutput = QtWidgets.QLabel(self)
        self.voiceOutput.resize(400, 90)
        self.voiceOutput.move(100, 460)
        self.voiceOutput.wordWrap = True
        # self.voiceOutput.setText("Press the button to start voice recognition.")

        self.voiceModelLbl = QtWidgets.QLabel(self)
        self.voiceModelLbl.resize(200, 25)
        self.voiceModelLbl.move(20, 20)
        self.voiceModelLbl.setText("Select Voice Model:")

        self.radioBtn1 = QtWidgets.QRadioButton(self)
        self.radioBtn1.setText("Goolge")
        self.radioBtn1.resize(150, 25)
        self.radioBtn1.move(20,50)
        self.radioBtn1.setChecked(True)

        

        self.radioBtn2 = QtWidgets.QRadioButton(self)
        self.radioBtn2.setText("Open AI Wisper")
        self.radioBtn2.resize(150, 25)
        self.radioBtn2.move(20,75)
        

        self.radioBtn3 = QtWidgets.QRadioButton(self)
        self.radioBtn3.setText("CMUSphinx")
        self.radioBtn3.resize(150, 25)
        self.radioBtn3.move(20,100)
        

    
    def pressVoiceButton(self):
        # self.voiceOutput.setText("")
        
        command = self.process_voice_command()
        

        if "on" in command:
            self.ligthOnLabel.show()
            self.ligthOffLabel.hide()
            GPIO.output(6, GPIO.HIGH)
        elif "off" in command:
            self.ligthOnLabel.hide()
            self.ligthOffLabel.show()
            GPIO.output(6, GPIO.LOW)
        else:
            print("Command not supported.")

    def process_voice_command(self):
        recognizer = sr.Recognizer()
        
        with sr.Microphone() as source:
            self.voiceOutput.setText("Listening...")
            QApplication.processEvents()
            print("Listening...")
            
            # recognizer.energy_threshold = 4000
            recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
            audio = recognizer.listen(source)

        try:
            # Recognize the audio and convert it to text
            #select voice model
            if self.radioBtn1.isChecked():
                command = recognizer.recognize_google(audio).lower()
            elif self.radioBtn2.isChecked():
                command = recognizer.recognize_whisper(audio).lower()
            elif self.radioBtn3.isChecked():
                command = recognizer.recognize_sphinx(audio).lower()


            self.voiceOutput.setText("You said: " + command)
            print("You said:", command)
            return command
        except sr.UnknownValueError:
            self.voiceOutput.setText("Sorry, I didn't understand that.")
            print("Sorry, I didn't understand that.")
            return ""
        except sr.RequestError:
            self.voiceOutput.setText("Sorry, there was an issue connecting to the service.")
            print("Sorry, there was an issue connecting to the service.")
            return ""

def window():
    app = QApplication(sys.argv)
    win = MainWindow()

    win.show()
    sys.exit(app.exec_())

window()